# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime

class FilterDatePipeline(object):
    def process_item(self, item, spider):
        now = datetime.now()
        print(now.year)
        if item['numerocp'][0].split('/')[-1] == now.year:
            return item
