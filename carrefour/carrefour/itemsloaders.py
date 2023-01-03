from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader
from datetime import datetime
from unidecode import unidecode



class CarrefourItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    name_in         = MapCompose(lambda x: x)
    price_in        = MapCompose(lambda x: float(x.replace('\n','').replace(' ','').replace('.','').replace(',','.')[1:]) )