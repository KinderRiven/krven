import MySQLdb


class MySQLUtils:

    def __init__(self, mysql_ip, mysql_db, mysql_usr, mysql_pwd):
        self.mysql_ip = mysql_ip
        self.mysql_db = mysql_db
        self.mysql_user = mysql_usr
        self.mysql_pwd = mysql_pwd

    def execute(self, sql):
        db = MySQLdb.connect(
            self.mysql_ip, self.mysql_user, self.mysql_pwd, self.mysql_db)
        cursor = db.cursor()
        # noinspection PyBroadException
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        db.close()