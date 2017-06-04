#encoding=utf-8


class LogModule:

    def __init__(self):
        self.init = 0

    @staticmethod
    def log(*args):
        for each in args:
            print "[",
            print each,
            print "]",
        print ""
