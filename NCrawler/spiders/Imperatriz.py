# -*- coding: utf-8 -*-
import random

import scrapy
from NCrawler.items import BiddingItem


class PrefeituraSpider(scrapy.Spider):
    name = 'Prefeitura'
    allowed_domains = ['imperatriz.ma.gov.br']
    start_urls = ['http://servicos.imperatriz.ma.gov.br/licitacoes']


    def parse(self, response):

        for licitacao in response.css('div.container table tbody tr'):
            modalidade = licitacao.css('div.container table tbody tr td b::text').extract_first()
            objetivo = licitacao.css('div.container table tbody tr td b::text').extract_first()
            numerocp = licitacao.css('div.container table tbody tr td b::text').re_first(r'\d+[/|_]+\d*')


            yield BiddingItem(modalidade = modalidade,objetivo = objetivo,numerocp = numerocp)


