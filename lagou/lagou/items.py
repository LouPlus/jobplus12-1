# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    logo = scrapy.Field()
    slogan = scrapy.Field()
    addr = scrapy.Field()

class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    addr = scrapy.Field()
