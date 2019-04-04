# -*- coding: utf-8 -*-
import scrapy
from NCrawler.items import BiddingItem


class AcailandiaSpider(scrapy.Spider):
    name = 'Acailandia'
    allowed_domains = ['acailandia.ma.gov.br']
    start_urls = ['https://www.acailandia.ma.gov.br/licitacoes']

    def parse(self, response):

        for modalidade in response.css('div#ListModalidades a'):
            link = modalidade.css('a::attr(href)').extract_first()
            yield response.follow(link, self.parse_binding)

    def parse_binding(self, response):
        for licitacao in response.css('div.buscar_licitacao_anexos div.panel-default'):
            link = licitacao.css('div.painel-body a::attr(href)').extract_first()
            modalidade = licitacao.css('div.panel-heading strong::text').extract_first()
            numerocp = licitacao.css('div.panel-heading strong::text').extract_first()
            objetivo = licitacao.css('div.painel-body::text').get()
            yield {'objetivo': objetivo, 'link': link}


