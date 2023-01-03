import scrapy
from scrapy.shell import inspect_response 
from time import sleep
from gallega.items import Product
from gallega.itemsloader import ProductLoader
from unidecode import unidecode
import re

class ProductSpider(scrapy.Spider):
    name = 'product'
    custom_settings = {
        'ITEM_PIPELINES': {
            'gallega.pipelines.ProductPipeline': 300
        }
    }
    allowed_domains = ['www.lagallega.com.ar']
    start_urls = ['https://www.lagallega.com.ar/Menu-1.asp']


    def start_requests(self):
        init_url = 'https://www.lagallega.com.ar/'
        yield scrapy.Request(url=init_url,callback=self.login)
        
    def login(self,response):
        yield scrapy.Request(url=self.start_urls[0], callback=self.action_manager)


    def action_manager(self,response):

        categories = response.xpath('//body/div/span/parent::div')
        for category in categories:
            try:
                function_text = category.xpath('@onclick').get()
                action_name, action_parameters = function_text.split("(")
                action_parameters = action_parameters.replace(")","").replace("'","").replace(";","").split(",")

                if action_name == "Dispara":
                    next_url = 'https://www.lagallega.com.ar/Menu-2.asp?Niv1=' + action_parameters[0]
                    yield scrapy.Request(url=next_url, callback=self.action_manager)
                elif action_name == "Dispara2":
                    next_url = 'https://www.lagallega.com.ar/Menu-3.asp?Niv1=' + action_parameters[0]+'&Niv2=' + action_parameters[1]
                    yield scrapy.Request(url=next_url, callback=self.action_manager)
                elif action_name == "Dispara3":
                    next_url = 'https://www.lagallega.com.ar/Menu-4.asp?Niv1=' + action_parameters[0]+'&Niv2=' + action_parameters[1] + '&Niv3=' + action_parameters[2]
                    yield scrapy.Request(url=next_url, callback=self.action_manager)
                elif action_name == "EnvioForm":
                    n1 = '00'
                    n2 = '00'
                    n3 = '00'
                    n4 = '00'
                    n1 = action_parameters[1]
                    n2 = action_parameters[2]
                    n3 = action_parameters[3]
                    n4 = action_parameters[4]
                    next_url = 'https://www.lagallega.com.ar/Productos.asp?N1=' + n1 + '&N2=' + n2 + '&N3=' + n3 + '&N4=' + n4
                    yield scrapy.Request(url=next_url, callback=self.parse_products)

            except Exception:
                print(Exception)

   
    def parse_products(self,response):
        products = response.xpath('//div[@id="Resultados"]//li[contains(@class,"cuadProd")]')

        try: 
            self.category = re.sub(r'\W+', '',  response.xpath('//div[@class="categ1"]/text()').get())
            cat2 = response.xpath('//div[@class="categ2"]/text()').get()
            cat3 = response.xpath('//div[@class="categ3"]/text()').get()
            cat4 = response.xpath('//div[@class="categ4"]/text()').get()
            if cat2 != None:
                self.category += "_" + re.sub(r'\W+', '', cat2)
            if cat3 != None:
                self.category += "_" + re.sub(r'\W+', '', cat3)
            if cat4 != None:
                self.category += "_" + re.sub(r'\W+', '', cat4)
            print(self.category,"----------------------------------------")
        except Exception:
            self.category = "pepe2"
        
        for product in products:
            try:

                product_item = ProductLoader(item=Product(), selector=product)
                product_item.add_xpath('name','div[@class = "InfoProd"]/div[@class = "InfoProdDet"]/div[@class = "desc"]/text()')
                product_item.add_xpath('price','div[@class = "InfoProd"]/div[@class = "precio"]/div[@class = "izq"]/text()')
                product_item.add_xpath('cat1','//div[@class="categ1"]/text()')
                product_item.add_xpath('cat2','//div[@class="categ2"]/text()')
                yield product_item.load_item()

            except Exception:
                print(Exception) 
        
        try:
            new_page = response.xpath('//input[@type = "button" and @value = "Siguiente"]/@onclick').get()
            new_page = new_page.split(',')[1][2:]
            new_page = new_page.replace("'","").replace(")","").replace(";","")
            new_page = 'https://www.lagallega.com.ar' + new_page
            #yield{'dsfsdfdsfsdfsdfsdffffffffffffff' : new_page}
            yield response.follow(new_page, callback=self.parse_products)
            
        except Exception:
            pass