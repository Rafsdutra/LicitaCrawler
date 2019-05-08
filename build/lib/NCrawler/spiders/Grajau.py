# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


def process_value():
    api_pattern = 'http://www.transparencia.grajau.ma.gov.br/acessoInformacao/licitacao/tce/listarLicitacoes/0?_=1556281505286'
    return api_pattern


class GrajauSpider(scrapy.Spider):
    name = 'Grajau'
    allowed_domains = ['www.transparencia.grajau.ma.gov.br']
    start_urls = ['http://www.transparencia.grajau.ma.gov.br/']

    rules = (
        Rule(
            LinkExtractor(
                allow_domains=allowed_domains,
                process_value=process_value
            ),
            callback='parse_item'
        ),
    )

    def parse_item(self, response):
        licitacoes = {}
        return licitacoes
