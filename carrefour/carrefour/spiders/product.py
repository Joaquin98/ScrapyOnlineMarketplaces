import scrapy
from carrefour.items import CarrefourItem
from carrefour.itemsloaders import CarrefourItemLoader
from time import sleep

class ProductSpider(scrapy.Spider):
    name = 'product'
    custom_settings = {
        'ITEM_PIPELINES': {
        }
    }
    allowed_domains = ['carrefour.com.ar']

    def __init__(self, name=None, **kwargs):
        self.start_urls = ["https://www.carrefour.com.ar/Electro-y-tecnologia/Smart-TV-y-soportes/Smart-TV?order="]

        super().__init__(name, **kwargs)

    def parse(self, response):
        products = response.xpath('//div[contains(@class,"lyracons-search-result-1-x-galleryItem")]')
        print(products, "-----------------------------------------")

        for product in products:
            print(product, " -----")
            try:
                
                '''
                product_item = CarrefourItemLoader(item = CarrefourItem(), selector=product)
                product_item.add_xpath('price', '//div[contains(@class,"vtex-flex-layout-0-x-flexColChild--wrapPrice")]//span[contains(@class,"lyracons-carrefourarg-product-price-1-x-sellingPrice")]//span[contains(@class,"lyracons-carrefourarg-product-price-1-x-currencyInteger")][1]/text()')
                product_item.add_xpath('name', '//span[contains(@class,"vtex-product-summary-2-x-productBrand")]/text()')
                yield product_item.load_item()
                '''
                yield{
                'name' : product.xpath( '//span[contains(@class,"vtex-product-summary-2-x-productBrand")]/text()'),
                'price': product.xpath('//div[contains(@class,"vtex-flex-layout-0-x-flexColChild--wrapPrice")]//span[contains(@class,"lyracons-carrefourarg-product-price-1-x-sellingPrice")]//span[contains(@class,"lyracons-carrefourarg-product-price-1-x-currencyInteger")][1]/text()').get(),
                }
            except Exception:
                print(Exception)



