# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DblpItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    issn = scrapy.Field()
    year = scrapy.Field()

    pass
    # helper
    # fileName = scrapy.Field()
    # pdfDownloadUrl = scrapy.Field()

