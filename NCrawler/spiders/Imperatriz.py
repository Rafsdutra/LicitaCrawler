# -*- coding: utf-8 -*-
import random

import scrapy
from NCrawler.items import BiddingItem


class PrefeituraSpider(scrapy.Spider):
    name = 'Imperatriz'
    allowed_domains = ['imperatriz.ma.gov.br']
    start_urls = ['http://servicos.imperatriz.ma.gov.br/licitacoes']


    def parse(self, response):

        for licitacao in response.css('div.container table tbody tr'):

            modalidade = licitacao.css('td b::text').extract_first()[:-14]
            objetivo = licitacao.css('td::text').extract()
            numerocp = licitacao.css('td b::text').re_first(r'\d+[/|_]+\d*')


            yield BiddingItem(modalidade = modalidade,
                              objetivo = objetivo,
                              numerocp = numerocp)


