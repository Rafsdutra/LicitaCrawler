# -*- coding: utf-8 -*-
import random

import scrapy


class PrefeituraSpider(scrapy.Spider):
    name = 'Prefeitura'
    allowed_domains = ['imperatriz.ma.gov.br']
    start_urls = ['http://servicos.imperatriz.ma.gov.br/licitacoes//']


    def parse(self, response):
        for licitacoes in response.xpath('//td/b').getall():
            # licitacao = licitacoes.css

            yield {'Licitacao' : licitacoes}

