# -*- coding: utf-8 -*-
import scrapy


class PrefeituraSpider(scrapy.Spider):
    name = 'Prefeitura'
    allowed_domains = ['http://servicos.imperatriz.ma.gov.br/licitacoes/']
    start_urls = ['http://http://servicos.imperatriz.ma.gov.br/licitacoes//']

    def parse(self, response):
        for licitacoes in response.xpath('//td/b'):
            licitacao = licitacoes.css.extract_first()

            yield {'Licitacao' : licitacao}
