#encoding=utf-8
from bs4 import BeautifulSoup

#读取测试文件内容
input_stream = open('index.xml', 'r')
text = input_stream.read()

soup = BeautifulSoup(text, "html.parser")

#find_all
#通过标签名找
article_list = soup.find_all(name="article")
for each in article_list:
    print each

print '--------------------------------------'

#通过class查找
article_list = soup.find_all(class_="article_content")
for each in article_list:
    print each

print '--------------------------------------'

#find
article = soup.find(id='article_1')
print article

print '--------------------------------------'

article = soup.find(class_='article_content')
print article
print article['href']

print '--------------------------------------'