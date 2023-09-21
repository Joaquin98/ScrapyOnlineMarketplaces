# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    cat1 = scrapy.Field()
    cat2 = scrapy.Field()
    cat3 = scrapy.Field()
    cat4 = scrapy.Field()
