import scrapy
from COTO.items import ProductItem
from COTO.itemsloaders import ProductLoader


class ProductSpider(scrapy.Spider):
    name = 'producti'
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
        products = response.css('#products li.clearfix')

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
                pass

        pages = response.css('div.atg_store_pagination a')

        next_page = None

        for page in pages:
            #total_page = 'cotodigital3.com.ar' + page.get()
            link = 'cotodigital3.com.ar' + page.css('::attr(href)')
            name = page.css('::first-line')
            if name not in self.visited_pages:
                next_page = link
                self.visited_pages.append(next_page)
        
        if next_page != None:
            yield response.follow(next_page, callback=self.parse)


