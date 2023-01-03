from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader
from datetime import datetime
from unidecode import unidecode


BASE_LINK = 'https://www.cotodigital3.com.ar'

class CotoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    name_in         = MapCompose(lambda x: x)
    price_in        = MapCompose(lambda x: float(x.replace('\n','').replace(' ','').replace('.','').replace(',','.')[1:]) )
    discount_in     = MapCompose(lambda x : x)



class CategoryLinkLoader(ItemLoader):
    name_in = MapCompose(lambda x : unidecode(x.replace(' ','_')))
    link_in = MapCompose(lambda x : BASE_LINK + x)



class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    name_in         = MapCompose(lambda x: x)
    price_in        = MapCompose(lambda x: float(x.replace('\n','').replace(' ','').replace('.','').replace(',','.')[1:]) )
    discount_in     = MapCompose(lambda x : x)

