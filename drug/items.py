# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DrugItem(scrapy.Item):
    # define the fields for your item here like:
    name_drug = scrapy.Field()
    source_link = scrapy.Field()
    pass


class MedicalEquipment(scrapy.Item):
    name_medical_equipment = scrapy.Field()
    source_link = scrapy.Field()
