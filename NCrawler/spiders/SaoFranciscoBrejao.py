import scrapy
from NCrawler.items import BiddingItem



class PrefeituraSpider(scrapy.Spider):
    name = 'São Francisco do Brejão'
    allowed_domains = ['saofranciscodobrejao.ma.gov.br']
    start_urls = ['https://www.saofranciscodobrejao.ma.gov.br/Licitacoes/Todas?page=16']

    def parse(self, response):
        for licitacao in response.css('div.container div.bx-resultado'):
            modalidade = licitacao.css('div h4::text').extract_first()
            objetivo = licitacao.css('div div p::text')[5].extract()
            numerocp = licitacao.css('div h4::text').re_first(r'\d+[/|_]+\d*')

            yield BiddingItem(modalidade=modalidade,
                              objetivo=objetivo,
                              numerocp=numerocp)


# sendMail()

