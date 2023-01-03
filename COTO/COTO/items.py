# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime

class CotoItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()



class CategoryLinkItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()