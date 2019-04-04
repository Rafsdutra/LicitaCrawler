# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BiddingItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    modalidade = scrapy.Field()
    numerocp = scrapy.Field()
    objetivo = scrapy.Field()
    link = scrapy.Field()