#encoding=utf-8
import os


class FileUtiles:

    def __init__(self, bool_log = 0):
        self.bool_log = bool_log

    @staticmethod
    def fileNameFilter(name):
        _name = name.replace("/", "") \
            .replace("\\", "") \
            .replace(":", "") \
            .replace("<", "") \
            .replace(">", "") \
            .replace("*", "") \
            .replace("?", "") \
            .replace("\"", "") \
            .replace("|", "")
        return _name

    @staticmethod
    def buildFolder(path_name, folder_name):

        name = FileUtiles().fileNameFilter(name = folder_name)
        path = path_name + name

        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def copyTextFile(from_path, to_path):

        #文本文件读写复制
        from_file = open(from_path, 'r')
        to_path = open(to_path, 'w')
        try:
            text = from_file.read()
            to_path.write(text)
        finally:
            from_file.close()
            to_path.close()