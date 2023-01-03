from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader
from datetime import datetime
from unidecode import unidecode
import re

class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    name_in                  = MapCompose(lambda x: x)
    price_in                 = MapCompose(lambda x: x[1:-1])
    cat1_in                  = MapCompose(lambda x:  re.sub(r'\W+', '', x))
    cat2_in                  = MapCompose(lambda x:  re.sub(r'\W+', '', x))
    cat3_in                  = MapCompose(lambda x:  re.sub(r'\W+', '', x))
    cat4_in                  = MapCompose(lambda x:  re.sub(r'\W+', '', x))