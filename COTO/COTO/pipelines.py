# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from datetime import datetime


class CotoPipeline:

    def __init__(self) -> None:
        self.conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = 'xiku2233',
                database = 'scraping'
            )

        self.cur = self.conn.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS product(
            id int NOT NULL auto_increment, 
            name VARCHAR(255),
            price Float,
            discount VARCHAR(255),
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):

        self.cur.execute(""" insert into product (name, price,discount) values (%s,%s,%s)""", (
            item["name"],
            str(item["price"]),
            item["discount"]
        ))

        ## Execute insert of data into database
        self.conn.commit()


    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()



class CategoryLinkPipeline:

    def __init__(self) -> None:
        self.conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = 'xiku2233',
                database = 'scraping'
            )

        self.cur = self.conn.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS CategoryLink(
            id int NOT NULL auto_increment, 
            name VARCHAR(255),
            link VARCHAR(1055),
            date DATETIME,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):

        self.cur.execute(""" insert into CategoryLink (name, link, date) values (%s,%s,%s)""", (
            item["name"][0],
            item["link"][0],
            str(datetime.now())
        ))

        ## Execute insert of data into database
        self.conn.commit()


    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()



class ProductPipeline:

    def __init__(self) -> None:
        self.conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = 'xiku2233',
                database = 'scraping'
            )

        self.cur = self.conn.cursor()
        


    def process_item(self, item, spider):

        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS """ + spider.category + """(
            id int NOT NULL auto_increment, 
            name VARCHAR(255),
            price Float,
            PRIMARY KEY (id)
        )
        """)

        self.cur.execute(""" insert into """ + spider.category + """ (name, price) values (%s,%s)""", (
            item["name"],
            str(item["price"])
        ))

        ## Execute insert of data into database
        self.conn.commit()


    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
