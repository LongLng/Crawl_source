# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
from items import DrugItem
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SaveDrugToSql(object):
    def __init__(self):
        self.create_connection()
        if self.checkTableExists('drug_info') == False:
            self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database='drug_data'
        )
        self.curr = self.conn.cursor()

    def checkTableExists(self, tableName):
        self.curr.execute(
            """
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_name = '{0}'
                    """.format(tableName.replace('\'', '\'\''))
        )
        if self.curr.fetchone()[0] == 1:
            return True
        return False

    def create_table(self):
        self.curr.execute("DROP TABLE IF EXISTS drug_info")
        self.curr.execute("DROP TABLE IF EXISTS medical_equipment_info")
        self.curr.execute(
            """ CREATE TABLE drug_info (id INT AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(255), 
            source_link VARCHAR(255),
            UNIQUE(name),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)""")
        self.curr.execute(
            """ CREATE TABLE medical_equipment_info (id INT AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(255), 
            source_link VARCHAR(255),
            UNIQUE(name),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)""")

    def process_item(self, item, spider):
        self.store_db(item)
        # return item

    def store_db(self, item):
        if item['type'] == 'drug':
            sql = ("INSERT IGNORE INTO drug_info (name,source_link) VALUES (%s,%s)")
            val = (item['name'], item['source_link'])
            self.curr.execute(sql, val)
        if item['type'] == 'medical_equipment':
            sql = ("INSERT IGNORE INTO medical_equipment_info (name,source_link) VALUES (%s,%s)")
            val = (item['name'], item['source_link'])
            self.curr.execute(sql, val)
        # self.curr.execute("""insert into drug_info values (%s)""",(
        #     item['name_drug']
        # ))
        self.conn.commit()
