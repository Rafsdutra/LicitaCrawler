# -*- coding: utf-8 -*-
import scrapy


class AcailandiaSpider(scrapy.Spider):
    name = 'Acailandia'
    allowed_domains = ['acailandia.ma.gov.br']
    start_urls = ['https://acailandia.ma.gov.br/']

    def parse(self, response):

        title = response.css('head title ::text').extrat_first()
        yield {'titulo': title}
