import json
from scrapy.crawler import CrawlerProcess
from COTO.spiders.product import ProductSpider
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


file_obj = open('links.json')
links_data = json.load(file_obj)

links = []

configure_logging()
settings = get_project_settings()


for link in links_data:
    process = CrawlerProcess(settings)
    process.crawl(ProductSpider,category = link['name'],link = link['link'])
process.start(stop_after_crawl=False)
