# -*- coding: utf-8 -*-
import random

import scrapy


class PrefeituraSpider(scrapy.Spider):
    name = 'Prefeitura'
    allowed_domains = ['imperatriz.ma.gov.br']
    start_urls = ['http://servicos.imperatriz.ma.gov.br/licitacoes//']


    def parse(self, response):
        # descricao = response.css('table tbody tr td::text').getall()
        for licitacoes in response.css('table tbody tr td b::text').getall():


            # licitacoes.replace(" ", "")


            yield {'Licitacao: ': licitacoes, 'Descricao: ': ''}

