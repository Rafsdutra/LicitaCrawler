# -*- coding: utf-8 -*-
import scrapy

from NCrawler.items import BiddingItem


class GovEdsonlobaoSpider(scrapy.Spider):
    name = 'Governador Edson Lobão'
    allowed_domains = ['governadoredisonlobao.ma.gov.br']
    start_urls = ['https://www.governadoredisonlobao.ma.gov.br/licitacoes']

    def parse(self, response):

        for modalidade in response.css('div#ListModalidades a'):
            link = modalidade.css('a::attr(href)').extract_first()
            yield response.follow(link, self.parse_binding)

    def parse_binding(self, response):
        for licitacao in response.css('div.buscar_licitacao_anexos div.panel-default'):
            link = licitacao.css('div.panel-body a::attr(href)').extract_first()
            modalidade = ' '.join(licitacao.css('div.panel-heading strong::text').extract_first().split()[:-2])
            numerocp = "".join(licitacao.css('div.panel-heading strong::text').re(r'\d*[/|_]+\d*'))
            objetivo = licitacao.css('div.panel-body::text').extract()[5]

            yield BiddingItem(modalidade=modalidade, numerocp=numerocp, objetivo=objetivo, link=link)

