#encoding=utf-8
import os


class FileUtiles:

    def __init__(self, bool_log = 0):
        self.bool_log = bool_log

    @staticmethod
    def buildFolder(path_name, folder_name):

        name = folder_name.replace("/", "")\
                .replace("\\", "")\
                .replace(":", "")\
                .replace("<", "")\
                .replace(">", "")\
                .replace("*", "")\
                .replace("?", "")\
                .replace("\"", "")\
                .replace("|", "")
        path = path_name + name

        if not os.path.exists(path):
            os.mkdir(path)
