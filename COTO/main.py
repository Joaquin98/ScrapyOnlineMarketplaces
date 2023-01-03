import json
from scrapy.crawler import CrawlerProcess
from COTO.spiders.product import ProductSpider

file_obj = open('links.json')
links_data = json.load(file_obj)

links = []

for link in links_data:
    process = CrawlerProcess({'AUTOTHROTTLE_ENABLED': True,'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})

    process.crawl(ProductSpider,category = link['name'],link = link['link'])

process.start() 

