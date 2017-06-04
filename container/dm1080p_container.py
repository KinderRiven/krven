#encoding=utf-8
import threading
from bs4 import BeautifulSoup
from http.http_module import HttpModule
from match.dm1080p_match import DM1080Match
from tools.file_utils import FileUtiles
from log.log_utils import LogModule
import MySQLdb


class DM1080Item:

    #XML
    XML_FILE_EXAMPLE_ROOT = "document/dm1080p/"
    XML_FILE_EXAMPLE_PATH = "document/dm1080p/example.xml"

    def __init__(self, item_name, item_link, download_list):
        self.item_name = item_name
        self.item_link = item_link
        self.item_update_time = 0
        self.download_list = download_list

    def printInfo(self):
        print "[Name] : " + self.item_name
        print "[Link] : " + self.item_link
        print "[List] : "
        for each in self.download_list:
            each.printInfo()

    def saveAsXML(self):

        #拷贝
        name = FileUtiles().fileNameFilter(self.item_name)
        path = self.XML_FILE_EXAMPLE_ROOT + name + ".xml"
        FileUtiles().copyTextFile(self.XML_FILE_EXAMPLE_PATH, path)

        #插入关键信息
        fs = open(path, 'r')
        xml = fs.read()
        fs.close()
        item = BeautifulSoup(xml, "html.parser")
        #item_name
        item.find(name = "item_name").string = self.item_name
        #item_link
        item.find(name = "item_link").string = self.item_link
        #item_list
        download_list = item.find(name = "download_list")
        print type(download_list)
        for each in self.download_list:
            download_item = item.new_tag("download_item")
            #download_name
            download_name = item.new_tag("download_name")
            download_name.string = each.download_name
            #download_type
            download_type = item.new_tag("download_type")
            download_type.string = each.download_type
            #download_link
            download_link = item.new_tag("download_link")
            download_link.string = each.download_link
            #append
            download_item.append(download_name)
            download_item.append(download_type)
            download_item.append(download_link)
            download_list.append(download_item)
        print item
        fs = open(path, 'w')
        fs.write(str(item))
        fs.close()


class DM1080Container(threading.Thread):

    index_url = "http://dm1080p.com/page/"
    download_url = "http://zzzpan.com/?/file/view-"

    def __init__(self, start_page, end_page, cookie, headers, queue):

        threading.Thread.__init__(self)
        self.start_page = start_page
        self.end_page = end_page
        self.cookie = cookie
        self.headers = headers
        self.queue = queue

    #获得下载列表
    def getDownloadList(self, url):
        html = HttpModule().getPageContent(
            url = url,
            headers = self.headers,
            cookie = self.cookie
        )
        download_list = DM1080Match().getDownloadCode(html)
        return download_list

    #获得下载链接
    def getDownloadLink(self, code_list):
        download_list = []
        for each in code_list:
            html = HttpModule().getPageContent(
                url = self.download_url + each + ".html",
                headers = self.headers,
                cookie = self.cookie
            )
            download_list.append(DM1080Match().getDownloadFile(html))
        return download_list

    #线程启动入口
    def run(self):

        for i in range(self.start_page, self.end_page, 1):

            url = self.index_url + str(i)
            #获得页面列表
            html = HttpModule().getPageContent(
                url = url,
                headers = self.headers,
                cookie = self.cookie
            )
            #拉取帖子列表
            article_list = DM1080Match().getArticleList(html)
            item_list = []
            #对每一个帖子详细信息进行提取
            for j in range(0, len(article_list), 1):

                item_name = article_list[j].string
                item_link = article_list[j]["href"]
                code_list = self.getDownloadList(item_link)
                download_list = self.getDownloadLink(code_list)

                LogModule().log("Getting resource", item_name, item_link, code_list, download_list)

                item_list.append(DM1080Item(
                    item_name = item_name,
                    item_link = item_link,
                    download_list = download_list
                ))
            for each in item_list:
                self.queue.put([each.item_name.encode("utf-8"), each.item_link, each.item_update_time])


