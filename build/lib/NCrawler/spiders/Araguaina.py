# -*- coding: utf-8 -*-
import scrapy

from NCrawler.items import BiddingItem


class AraguainaSpider(scrapy.Spider):
    name = 'Araguaina'
    allowed_domains = ['cpl.araguaina.to.gov.br/']
    start_urls = ['http://www.cpl.araguaina.to.gov.br/']

    def parse(self, response):
        for licitacao in response.css('div.TudoGeral div#Meio'):
            modalidade = licitacao.css('h2::text').extract_first()
            objetivo = licitacao.css('span::text').extract_first()
            numerocp = licitacao.css('b::text').re_first(r'\d+[/|_]+\d*')
            link = 'cpl.araguaina.to.gov.br' + licitacao.css('div.Leis div.Lei a::attr(href)').get()

            yield BiddingItem (
                modalidade=modalidade,
                objetivo=objetivo,
                numerocp=numerocp,
                link=link
            )
