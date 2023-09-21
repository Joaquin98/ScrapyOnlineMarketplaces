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
            host='localhost',
            user='root',
            password='xiku2233',
            database='galle'  # 'scraping-lagallega'
        )

        self.cur = self.conn.cursor()

        # Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Items(
            id int NOT NULL auto_increment, 
            name VARCHAR(255),
            price Float,
            category VARCHAR(255),
            image VARCHAR(512),
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):

        category = item["cat1"]
        if "cat2" in item.keys() and item["cat2"] != None:
            category += "_" + item["cat2"]
        if "cat3" in item.keys() and item["cat3"] != None:
            category += "_" + item["cat3"]
        if "cat4" in item.keys() and item["cat4"] != None:
            category += "_" + item["cat4"]

        self.cur.execute(""" insert into Items (name, price, category,image) values (%s,%s,%s,%s)""", (
            item["name"],
            float(item["price"].replace(".", "").replace(",", ".")),
            category,
            item['image']
        ))

        # Execute insert of data into database
        self.conn.commit()

    def close_spider(self, spider):

        # Close cursor & connection to database
        self.cur.close()
        self.conn.close()
