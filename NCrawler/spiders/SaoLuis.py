# -*- coding: utf-8 -*-
import scrapy

from NCrawler.items import BiddingItem


class SaoluisSpider(scrapy.Spider):
    name = 'Sao Luis'
    allowed_domains = ['saoluis.ma.gov.br']
    start_urls = ['http://www.saoluis.ma.gov.br/subportal_licitacoes.asp']
    download_delay = 4.0

    def parse(self, response):
        yield scrapy.FormRequest.from_response(response=response,
                                               formdata={'modalidade': '4',
                                                         'situacao': ' ',
                                                         'orgao': ' ',
                                                         'num_licitacao': ' ',
                                                         'exercicio': ' ',
                                                         'periodo': '1',
                                                         'dataini': '',
                                                         'datafim': '',
                                                         'objeto': '',
                                                         'order': '2',
                                                         'go': 'Buscar',
                                                         'bt_buscar': 'buscar'},
                                               callback=self.parse_binding)

    def parse_binding(self, response):
        for licitacao in response.css('div#geral div#caixa_listagem_licitacoes'):
            modalidade = licitacao.css('div.item_lic_titulo::text').extract_first().replace('\r\n\t\t\t\t\t\t\t', '')
            objetivo = licitacao.css('div.item_lic_objeto div::text').extract_first()
            numerocp = licitacao.css('div.item_lic_titulo span::text').extract_first()
            link = str(self.allowed_domains[0]) + '/licitacoes' + \
                   licitacao.css('div.item_lic_anexos div a::attr(href)').extract()[1]

            yield BiddingItem(modalidade=modalidade,
                              objetivo=objetivo,
                              numerocp=numerocp,
                              link=link)
