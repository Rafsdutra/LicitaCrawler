import scrapy
from NCrawler.items import BiddingItem
from scrapy.http import Request


class DavinopolisSpider(scrapy.Spider):
    name = 'Davinopolis'
    allowed_domains = ['davinopolis.ma.gov.br']
    start_urls = ['http://davinopolis.ma.gov.br/licitacoes/pregaopresencial']

    def parse(self, response):
        for item in response.css('div.row div.span8 li'):
            link = item.css('a::attr(href)').extract_first()
            yield response.follow(link, self.bidding)

    def bidding(self, response):
            link = response.css('div.row div.span8 li a::attr(href)').get()
            modalidade = response.css('div.row div.span8 div.blog-post h4::text').extract_first()[:18]
            objetivo = ' '.join(response.css('div.row div.span8 div.blog-post p::text').re(r'\w+'))
            numerocp = ' '.join(response.css('div.row div.span8 div.blog-post p::text').re(r'\w+')[:2])

            yield BiddingItem(modalidade=modalidade, objetivo=objetivo, numerocp=numerocp, link=link)
