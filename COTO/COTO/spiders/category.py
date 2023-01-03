import scrapy


class CategorySpider(scrapy.Spider):
    name = 'category'
    custom_settings = {
        'ITEM_PIPELINES': {
        }
    }
    allowed_domains = ['cotodigital3.com.ar']
    visited_pages = []

    def __init__(self, name=None, **kwargs):
        self.start_urls = ["https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-bebidas/_/N-1c1jy9y?Nf=product.endDate%7CGTEQ+1.6717536E12%7C%7Cproduct.startDate%7CLTEQ+1.6717536E12%7C%7Cproduct.endDate%7CGTEQ+1.6720128E12%7C%7Cproduct.startDate%7CLTEQ+1.6720128E12&Nr=AND%28product.sDisp_200%3A1004%2Cproduct.language%3Aespa%C3%B1ol%2COR%28product.siteId%3ACotoDigital%29%29&Nrpp=72"]
        self.name = 'category'

        super().__init__(name, **kwargs)




    def parse(self, response):
        relative_link = response.xpath('//*[@id="atg_store_pagination"]/li[contains(@class,"active")]/following-sibling::li/a/@href').extract_first()
        total_link = 'cotodigital3.com.ar' + relative_link
        name = response.xpath('//*[@id="atg_store_pagination"]/li[contains(@class,"active")]/following-sibling::li/a/@title').extract_first()

        yield {name : total_link}

        next_page = total_link

        if next_page != None:
            yield response.follow(next_page, callback=self.parse)


