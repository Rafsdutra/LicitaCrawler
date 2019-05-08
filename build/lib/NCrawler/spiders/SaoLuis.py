# -*- coding: utf-8 -*-
import scrapy

from NCrawler.items import BiddingItem


class SaoluisSpider(scrapy.Spider):
    name = 'Sao Luis'
    allowed_domains = ['saoluis.ma.gov.br']
    start_urls = ['http://www.saoluis.ma.gov.br/subportal_licitacoes.asp']

    def parse(self, response):
        for licitacao in response.css('div#geral div#caixa_listagem_licitacoes'):
            modalidade = licitacao.css('div.item_lic_titulo::text').extract_first().replace('\r\n\t\t\t\t\t\t\t','')
            objetivo = licitacao.css('div.item_lic_objeto div::text').extract_first()
            numerocp = licitacao.css('div.item_lic_titulo span::text').extract_first()

            yield BiddingItem (modalidade=modalidade,
                               objetivo=objetivo,
                               numerocp=numerocp)

