#encoding=utf-8
from container.dm1080p_container import DM1080Container
from cookie.cookie_module import CookieModule
from log.log_utils import LogModule
import Queue
import MySQLdb


class DM1080Manager:

    task_queue = []
    start_page = 10
    end_page = 20
    item_queue = Queue.Queue()

    #DATABASE
    DB_TABLE_NAME = "dm1080p_item"
    DB_HOST = "localhost"
    DB_NAME = "krven"
    DB_USR = "root"
    DB_PWD = "125506"

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

        LogModule().log("Get cookie", "start")

        for i in range(self.start_page, self.end_page, 1):
            self.task_queue.append(DM1080Container(
                start_page = i,
                end_page = i + 1,
                headers = self.http_headers,
                cookie = cookie,
                queue = self.item_queue
            ))
        for each in self.task_queue:
            each.start()
        for each in self.task_queue:
            each.join()
        #整合参数
        params = []
        while True:
            if self.item_queue.empty():
                break
            param = self.item_queue.get()
            params.append(param)
        LogModule().log(params)
        #插入到数据库中
        db_connect = MySQLdb.connect(
            host=self.DB_HOST,
            user=self.DB_USR,
            passwd=self.DB_PWD,
            db=self.DB_NAME,
            use_unicode=True,
            charset="utf8"
        )
        sql = "INSERT INTO krven.dm1080p_item (name, link, update_date) VALUES(%s, %s, %s)"
        cursor = db_connect.cursor()
        cursor.executemany(sql, params)
        db_connect.commit()
        cursor.close()
        db_connect.close()
