
import scrapy
from NCrawler.items import BiddingItem

class PrefeituraSpider(scrapy.Spider):
    name = 'JoaoLisboa'
    allowed_domains = ['joaolisboa.ma.gov.br/']
    start_urls = ['http://joaolisboa.ma.gov.br/modalidades']



    def parse(self, response):

        for modalidade in response.css('div#content div.row div.span8 a').get():
            link = modalidade.css('a::attr(href)').get()
            yield response.follow(link, self.parse_binding)


    def parse_binding(self, response):
        link = response.css('div#content div.row li a::attr(href)').get()
        modalidade = response.css('div#content div.row a strong::text').get()
        # titulo = response.css('div#content div.row div.span8 li a strong::text').get()

        resultado = BiddingItem(modalidade = modalidade, link = link)

        yield resultado