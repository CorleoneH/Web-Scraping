import requests
from lxml import etree
import csv

def getHTMLText(url, encoding='utf-8'):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)  \
               AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"}
    try:
        r = requests.get(url, headers=headers)
        r.encoding = encoding
        r.raise_for_status()
        return r.text
    except:
        return "Get something wrong!"

def getInfo(html, bookInfos):
    selector = etree.HTML(html)
    infos = selector.xpath('//tr[@class="item"]')
    #print(type(infos))
    #print(len(infos))
    for info in infos:
        name = info.xpath('td/div/a/@title')[0]
        url = info.xpath('td/div/a/@href')[0]

        book_infos = info.xpath('td/p/text()')[0]
        author = book_infos.split('/')[0]
        publisher = book_infos.split('/')[-3]
        date = book_infos.split('/')[-2]
        price = book_infos.split('/')[-1]

        mark = info.xpath('td/div/span[2]/text()')[0]
        comments = info.xpath('td/p/span/text()')
        comment = comments[0] if len(comments) != 0 else '空'

        bookInfos.append([name, url, author, publisher, date, price, mark, comment])
        
def save2csv(bookInfos):
    f = open('C:/Users/longh/Desktop/python爬虫/project/douban/doubanbook.csv', 'wt', newline='', encoding='utf-8')
    writer = csv.writer(f)
    for bookInfo in bookInfos:
        writer.writerow(bookInfo)
    f.close()

def main():
    #构建url链接列表
    urls = ['https://book.douban.com/top250?start={}'.format(str(i)) for i in range(0, 250, 25)]
    bookLists = []
    bookLists.append(['name', 'url', 'author', 'publisher', 'date', 'price', 'mark', 'comment'])
    for url in urls:
        html = getHTMLText(url)
        getInfo(html, bookLists)
        #print(len(bookLists))
        save2csv(bookLists)
        
    print('Success!')

main()
