import json
import queue

import scrapy
from scrapy.crawler import CrawlerProcess

# from ..pipelines import DblpPipeline
# import pymysql
# from bs4 import BeautifulSoup
# from scrapy.crawler import CrawlerProcess
from Dblp.items import DblpItem

PAPER_PERPAGE = 500
KEYWORD_NUM = 50


class DblpSpider(scrapy.Spider):
    name = 'Dblp'

    # allowed_domains = ['Dblp.com']
    # start_urls = ['http://dblp.com/']
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.issn = queue.Queue()
        self.journal = queue.Queue()
        self.maxNum =queue.Queue()

    def start_requests(self):
        url = 'https://dblp.org/db/journals/biaa/index.html'
        # url += keyword
        # url += '&h=' + str(PAPER_PERPAGE) + '&format=json'
        self.journal.put("biaa")
        # 创建 scrapy.Request 实例
        req = scrapy.Request(url=url, callback=self.parse)
        yield req

    def parse(self, response):
        # response_dict = json.loads(response.text)
        # print(response_dict)
        # a = response.css("ul").xpath('//span[@class="title"]/text()').getall()

        # issn
        issn = response.xpath('//div[@id="info-section"]//ul//li/text()').getall()

        # year
        yearPre = response.xpath('//ul//li').css('a').xpath('@href').getall()
        year = []
        for it in yearPre:
            if 'https://dblp.org/db/journals/'+self.journal.get() in it:
                year.append(it)

        self.maxNum.put(len(year))
        # name
        name = response.xpath('//header[@id="headline"]//h1/text()').getall()
        # a = list(set(a))
        # print(issn)
        # print(year)
        # print(name)
        self.item['name'] = name
        self.item['issn'] = issn
        self.item['year'] = []

        print(year)
        for yearUlr in year:
            req = scrapy.Request(url=yearUlr, callback=self.yearParser)
            print("new Request:", yearUlr)
            yield req
        print("--------over--------")
        print(self.item['year'])
        yield self.item

    def yearParser(self, response):
        year = response.xpath('//header//h2/text()').getall()
        self.item['year'] = year


# process = CrawlerProcess(settings={
#     "FEEDS": {
#         "items.json": {"format": "json"},
#     },
# })
#
# process.crawl(DblpSpider)
# process.start()  # the script will block here until the crawling is finished
