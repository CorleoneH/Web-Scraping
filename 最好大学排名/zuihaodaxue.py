import requests
from lxml import etree
import csv

def getHTMLText(url, encoding='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = encoding
        return r.text
    except:
        return 'Get something wrong!'

def getInfo(html, infoLists):
    selector = etree.HTML(html)
    infos = selector.xpath('//tr[@class="alt"]')
    for info in infos:
        rank = info.xpath('td[1]/text()')[0]
        name = info.xpath('td[2]/div/text()')[0]
        city = info.xpath('td[3]/text()')[0]
        score = info.xpath('td[4]/text()')[0]

        infoLists.append([rank, name, city, score])

def save2csv(infoLists):
    f = open('C:/Users/longh/Desktop/python爬虫/project/zuihaodaxue/zuihaodaxue.csv', 'wt', newline='', encoding='utf-8')
    writer = csv.writer(f)
    for infoList in infoLists:
        writer.writerow(infoList)
    f.close()

def main():
    url = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2019.html'
    uinfo = []
    uinfo.append(['排名', '学校名称', '省市', '总分'])
    html = getHTMLText(url)
    getInfo(html, uinfo)
    save2csv(uinfo)

    print('Success!')

main()
