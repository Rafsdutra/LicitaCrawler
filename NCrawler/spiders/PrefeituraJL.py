

import scrapy
from NCrawler.NCrawler.items import BiddingItem

class PrefeituraSpider(scrapy.Spider):
    name = 'Prefeitura'
    allowed_domains = ['joaolisboa.ma.gov.br/']
    start_urls = ['http://joaolisboa.ma.gov.br/modalidades']


    def parse(self, response):
        # descricao = response.css('table tbody tr td::text').getall()
        for licitacoes in response.css('div div div h3 span::text').get():
            link = response.css('div#content div.row li a::attr(href)')


            # licitacoes.replace(" ", "")


            yield response.follow(link, self.parse(licitacoes))


    def parse_licitacoes(self, response):
        link = response.url
        modalidade = response.css('div#content div.row a strong::text').get()
        # titulo = response.css('div#content div.row div.span8 li a strong::text').get()

        resultado = BiddingItem(modalidade = modalidade, link = link)

        yield resultado