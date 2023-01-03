import scrapy
from COTO.items import ProductItem
from COTO.itemsloaders import ProductLoader

class ProductSpider(scrapy.Spider):
    name = 'product'
    custom_settings = {
        'ITEM_PIPELINES': {
            'COTO.pipelines.ProductPipeline': 300
        }
    }
    allowed_domains = ['cotodigital3.com.ar']
    visited_pages = []

    def __init__(self, category, link, name=None, **kwargs):
        self.start_urls = [link]
        self.category = category
        self.name = 'product'

        super().__init__(name, **kwargs)

    def parse(self, response):
        #products = response.css('#products li.clearfix')
        products = response.xpath('//ul[@id = "products"]//li[contains(@class,"clearfix")]')
        for product in products:
            try:
                product_item = ProductLoader(item=ProductItem(), selector=product)
                product_item.add_css('name', 'div.descrip_full::text')
                product_item.add_css('price', 'span.atg_store_newPrice::text')
                try:
                    product_item.add_css('discount', 'span.price_discount::text')
                except Exception:
                    product_item.add_css('discount', 'span.atg_store_newPrice::text')
                    
                yield product_item.load_item()
            except Exception:
                print(Exception)

        relative_link = response.xpath('//*[@id="atg_store_pagination"]/li[contains(@class,"active")]/following-sibling::li/a/@href').extract_first()

        if relative_link != None:
            next_page = 'https://www.cotodigital3.com.ar' + relative_link
            yield response.follow(next_page, callback=self.parse)


