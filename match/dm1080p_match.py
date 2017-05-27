#encoding=utf-8
from bs4 import BeautifulSoup
from download.dm1080p_download import DM1080DownFile
import re


class DM1080Match:

    def __init__(self, bool_log = 0):
        self.bool_log = bool_log

    #拉取一个页面的帖子列表
    #return type : list
    @staticmethod
    def getArticleList(page_content):

        soup = BeautifulSoup(page_content, "html.parser")
        article_list = soup.select("article .entry-title a")
        return article_list

    #返回下载名称
    #return type : string
    @staticmethod
    def getDownloadFile(page_content):

        soup = BeautifulSoup(page_content, "html.parser")
        f_info = soup.select("div.fileinfo_l p")
        f_name = f_info[0].text
        #下载文件名称
        download_name = f_name[5 : len(f_name)]
        #下载文件类型
        download_type = f_info[2].text
        #下载链接
        down_site = soup.find(class_="downSite")
        link_hidden = down_site.find(class_="linkHidden")
        download_link = link_hidden.find("a")["href"]
        #下载文件
        download_file = DM1080DownFile(
            download_name = download_name,
            download_type = download_type,
            download_link = download_link
        )
        return download_file

    #返回下载码列表
    #return type : list
    @staticmethod
    def getDownloadCode(page_content):

        soup = BeautifulSoup(page_content, "html.parser")
        entry_content = str(soup.find(class_="entry-content"))
        #print entry_content
        download_list = []

        pattern1 = re.compile('资料编号：(.*?)-')
        match1 = pattern1.findall(entry_content)
        for each in match1:
            download_list.append(each.replace(" ", ""))

        pattern2 = re.compile('资料编码：(.*?)-')
        match2 = pattern2.findall(entry_content)
        for each in match2:
            download_list.append(each.replace(" ", ""))

        return download_list

