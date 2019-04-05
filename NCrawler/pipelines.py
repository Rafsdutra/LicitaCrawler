# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime

from scrapy.exceptions import DropItem


class FilterDatePipeline(object):
    def process_item(self, item, spider):
        now = datetime.now()
        date_licitacao  = int(item['numerocp'][0].split('/')[-1])
        if int(date_licitacao) == now.year:
            print(date_licitacao)
            return item
        else:
            raise DropItem("Licitação fora do ano atual")
