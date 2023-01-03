# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from datetime import datetime

class ProductPipeline:

    def __init__(self) -> None:
        self.conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = 'xiku2233',
                database = 'scraping-lagallega'
            )

        self.cur = self.conn.cursor()
        


    def process_item(self, item, spider):

        category = item["cat1"] + "_" 
        if item["cat2"] != None:
            category += "_" + item["cat2"] 

        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS """ + category + """(
            id int NOT NULL auto_increment, 
            name VARCHAR(255),
            price Float,
            PRIMARY KEY (id)
        )
        """)

        self.cur.execute(""" insert into """ + category + """ (name, price) values (%s,%s)""", (
            item["name"],
            str(item["price"])
        ))

        ## Execute insert of data into database
        self.conn.commit()


    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
