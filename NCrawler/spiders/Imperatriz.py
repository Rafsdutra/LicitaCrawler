# -*- coding: utf-8 -*-
import random

import scrapy
from NCrawler.items import BiddingItem


class ImperatrizSpider(scrapy.Spider):
    name = 'Imperatriz'
    allowed_domains = ['imperatriz.ma.gov.br']
    start_urls = ['http://servicos.imperatriz.ma.gov.br/licitacoes']


    def parse(self, response):

        for licitacao in response.css('div.container table tbody tr'):

            link = ImperatrizSpider.start_urls
            modalidade = licitacao.css('td b::text').extract_first()[:-14].upper()
            objetivo = " ".join(licitacao.css('td::text').re(r'\S+\w*'))
            numerocp = licitacao.css('td b::text').re_first(r'\d+[/|_]+\d*')
            link = licitacao.css('td a::attr(href)').extract_first()

            yield BiddingItem(modalidade=modalidade,
                              objetivo=objetivo,
                              numerocp=numerocp,
                              link=link)


