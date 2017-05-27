#encoding=utf-8
import cookielib
import urllib2
import urllib


class CookieModule:

    def __init__(self, bool_log=0):
        self.bool_log = bool_log

    @staticmethod
    def getCookie(url, headers, data):

        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        request = urllib2.Request(
            url = url,
            headers = headers,
            data=urllib.urlencode(data)
        )
        opener.open(request)

        return cookie