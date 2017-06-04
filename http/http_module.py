#encoding=utf-8
import urllib2
from log.log_utils import LogModule


#通信模块
class HttpModule:

    def __init__(self, bool_log = 0):
        self.bool_log = bool_log

    #获取页面源代码
    @staticmethod
    def getPageContent(url, headers, cookie=0):
        try:
            # 如果有cookie
            if cookie:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
                request = urllib2.Request(headers = headers, url = url)
                response = opener.open(request, timeout = 10)
                html = response.read()
                return html
            # 如果没有cookie
            else:
                request = urllib2.Request(headers=headers, url = url)
                response = urllib2.urlopen(request, timeout = 10)
                html = response.read()
                return html
        #捕获异常
        except Exception, e:
            LogModule().log(e, "getPageContent", url)
            return ""

