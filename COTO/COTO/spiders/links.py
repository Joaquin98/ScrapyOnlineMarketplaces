import scrapy
from COTO.items import CategoryLinkItem
from COTO.itemsloaders import CategoryLinkLoader

class LinksSpider(scrapy.Spider):
    name = 'links'
    custom_settings = {
        'ITEM_PIPELINES': {
            'COTO.pipelines.CategoryLinkPipeline': 300
        }
    }
    allowed_domains = ['cotodigital3.com.ar']
    start_urls = [
        'https://www.cotodigital3.com.ar/sitios/cdigi/browse?Nf=product.startDate%7CLTEQ+1.6717536E12%7C%7Cproduct.endDate%7CGTEQ+1.6717536E12&Nr=AND%28product.sDisp_200%3A1004%2Cproduct.language%3Aespa%C3%B1ol%2COR%28product.siteId%3ACotoDigital%29%29']
    visited_pages = []

    def parse(self, response):
        first_list = response.css('div.atg_store_facetsGroup_options_catsub')
        links = first_list[0].css('ul.atg_store_facetOptions li')

        for link in links:
            link_item = CategoryLinkLoader(item=CategoryLinkItem(), selector=link)
            link_item.add_css('name', 'a ::attr(title)')
            link_item.add_css('link', 'a ::attr(href)')
            yield link_item.load_item()
    


