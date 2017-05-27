
class DM1080DownFile:

    def __init__(self, download_name, download_link, download_type):
        self.download_name = download_name
        self.download_link = download_link
        self.download_type = download_type

    def printInfo(self):
        print '[Name] : ' + self.download_name
        print '[Type] : ' + self.download_type
        print '[Link] : ' + self.download_link