import scrapy
from COTO.items import CotoItem
from COTO.itemsloaders import CotoItemLoader


class TarantulaSpider(scrapy.Spider):
    name = 'tarantula'
    custom_settings = {
        'ITEM_PIPELINES': {
            #'COTO.pipelines.CotoPipeline': 300
        }
    }
    allowed_domains = ['cotodigital3.com.ar']
    # start_urls      = ['https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-frescos/_/N-1ewuqo6?Nf=product.endDate%7CGTEQ+1.670976E12%7C%7Cproduct.startDate%7CLTEQ+1.670976E12&Nr=AND%28product.sDisp_200%3A1004%2Cproduct.language%3Aespa%C3%B1ol%2COR%28product.siteId%3ACotoDigital%29%29']
    start_urls = [
        'https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-electro-informatica/_/N-u4pa0j']
    visited_pages = []

    def parse(self, response):
        products = response.css('#products li.clearfix')

        for product in products:
            product_item = CotoItemLoader(item=CotoItem(), selector=product)
            product_item.add_css('name', 'div.descrip_full::text')
            product_item.add_css('price', 'span.atg_store_newPrice::text')
            try:
                product_item.add_css('discount', 'span.price_discount::text')
            except Exception:
                product_item.add_css('discount', 'span.atg_store_newPrice::text')

            yield product_item.load_item()

        pages = response.css('div.atg_store_pagination a ::attr(href)')

        next_page = None

        for page in pages:
            total_page = 'cotodigital3.com.ar' + page.get()
            if total_page not in self.visited_pages:
                next_page = total_page
                self.visited_pages.append(next_page)

        if next_page != None:
            yield response.follow(next_page, callback=self.parse)
