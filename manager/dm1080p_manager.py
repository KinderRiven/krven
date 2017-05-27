#encoding=utf-8
from container.dm1080p_container import DM1080Container
from cookie.cookie_module import CookieModule


class DM1080Manager:

    task_queue = []

    #HTTP HEADER
    http_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
    }

    #获取cookie的用户账号和密码
    usr_data = {
        "log": "kinderriven",
        "pwd": "125506"
    }

    #登陆地址
    login_url = "http://dm1080p.com/wp-login.php"

    def __init__(self, bool_log = 0):
        self.bool_log = bool_log

    def start(self):

        cookie = CookieModule().getCookie(
            url = self.login_url,
            headers = self.http_headers,
            data = self.usr_data
        )

        for i in range(1, 2, 1):
            self.task_queue.append(DM1080Container(
                start_page = i,
                end_page = i + 1,
                headers = self.http_headers,
                cookie = cookie
            ))

        for each in self.task_queue:
                each.start()
        for each in self.task_queue:
                each.join()
