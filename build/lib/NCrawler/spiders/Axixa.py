# -*- coding: utf-8 -*-
import scrapy

from NCrawler.items import BiddingItem


class AxixaSpider(scrapy.Spider):
    name = 'Axixa'
    allowed_domains = ['transparencia.axixa.to.gov.br']
    start_urls = ['https://transparencia.axixa.to.gov.br/licitacoes']
    download_delay = 1.5

    def parse(self, response):

        yield scrapy.FormRequest.from_response(
            response=response,
            formdata={
                "exercicio": "2019",
                "entidade": "-1",
                "situacao": "-1",
                "processo": "",
                "modalidade": "-1",
                "objeto": ""
            },

        )

    def parse_item(self, response):
        yield {'response':  response.css('table').get()}


