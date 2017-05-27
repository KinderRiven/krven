#encoding=utf-8
import threading
from http.http_module import HttpModule
from match.dm1080p_match import DM1080Match
from tools.file_utils import FileUtiles


class DM1080Item:

    def __init__(self, item_name, item_link, download_list):
        self.item_name = item_name
        self.item_link = item_link
        self.download_list = download_list

    def printInfo(self):
        print "[Name] : " + self.item_name
        print "[Link] : " + self.item_link
        print "[List] : "
        for each in self.download_list:
            each.printInfo()

    def save(self):
        FileUtiles.buildFolder("../document/", self.item_name)


class DM1080Container(threading.Thread):

    index_url = "http://dm1080p.com/page/"
    download_url = "http://zzzpan.com/?/file/view-"

    def __init__(self, start_page, end_page, cookie, headers):

        threading.Thread.__init__(self)
        self.start_page = start_page
        self.end_page = end_page
        self.cookie = cookie
        self.headers = headers

    def getDownloadList(self, url):

        html = HttpModule().getPageContent(
            url = url,
            headers = self.headers,
            cookie = self.cookie
        )
        download_list = DM1080Match().getDownloadCode(html)
        return download_list

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

    def run(self):

        for i in range(self.start_page, self.end_page, 1):

            url = self.index_url + str(i)
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

                item_list.append(DM1080Item(
                    item_name = item_name,
                    item_link = item_link,
                    download_list = download_list
                ))

            for each in item_list:
                each.printInfo()
                each.save()

