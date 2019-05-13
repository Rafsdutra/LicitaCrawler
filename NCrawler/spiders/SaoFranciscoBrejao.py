import scrapy
from NCrawler.items import BiddingItem



class SaoFranciscoBrejaoSpider(scrapy.Spider):
    name = 'São Francisco do Brejão'
    allowed_domains = ['saofranciscodobrejao.ma.gov.br']
    start_urls = ['https://www.saofranciscodobrejao.ma.gov.br/Licitacoes/Abertas']

    def parse(self, response):
        for licitacao in response.css('div.container div.bx-resultado'):
            link = SaoFranciscoBrejaoSpider.start_urls
            modalidade = licitacao.css('div h4::text').extract_first()[:-8]
            objetivo = licitacao.css('div div p::text')[5].extract()
            numerocp = licitacao.css('div h4::text').re_first(r'\d+[/|_]+\d*')

            yield BiddingItem(modalidade=modalidade,
                              objetivo=objetivo,
                              numerocp=numerocp,
                              link=link)

