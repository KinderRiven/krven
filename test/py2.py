#encoding=utf-8

from http.http_module import HttpModule
from cookie.cookie_module import CookieModule

headers = {
 "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) "
               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
}

data = {
    "log" : "kinderriven",
    "pwd" : "125506"
}
cookie = CookieModule().getCookie(url="http://dm1080p.com/wp-login.php", headers=headers, data=data)
html = HttpModule().getPageContent(url="http://dm1080p.com/", headers=headers, cookie=cookie)

print html