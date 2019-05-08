# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import envconfig as conf

from scrapy.exceptions import DropItem

from NCrawler.services.filters import relevance


class FilterSimilarityPipeline(object):
    def process_item(self, item, spider):
        print(relevance(item['objetivo']))
        if relevance(item['objetivo']) >= 0.75:
            print("FILTRO DE SIMILARIDADE: OK")
            return item
        else:
            raise DropItem("FILTRO DE SIMILARIDADE: Licitação não é relacionada a marketing")


class FilterDatePipeline(object):
    def process_item(self, item, spider):

        now = datetime.date.today().year
        date_licitacao = int(item['numerocp'].replace(' ', '/').split('/')[-1])
        if int(date_licitacao) == now:
            print("FILTRO DE DATA: OK")
            return item
        else:
            raise DropItem("FILTRO DE DATA: Licitação fora do ano atual")


class FilterModalidade(object):
    def process_item(self, item, spider):
        pregaoEletronico = 'PREGÃO ELETRONICO'
        pregaoPresencial = 'PREGÃO PRESENCIAL'
        modalidade = str(item['modalidade']).upper()
        if pregaoPresencial in modalidade:
            print('FILTRO DE MODALIDADE: Pregão Presencial OK')
            return item
        elif pregaoEletronico in modalidade:
            print('FILTRO DE MODALIDADE: Pregão Eletronico OK')
            return item
        else:
            raise DropItem("FILTRO DE MODALIDADE: Item não é Pregão Presencial ou Pregão Eletronico")


class SendMail(object):

    def open_spider(self, spider):
        print("######### Iniciando o spider... #########")

    def process_item(self, item, spider):
        print("######## Processando pipelines... ############")

        self.modalidade = str(item['modalidade'])
        self.objetivo = str(item['objetivo'])
        self.numerocp = str(item['numerocp'])


        if self.modalidade is None:
            print('NÃO HÁ RETORNO')
        else:
            print('HÁ RETORNO')
            return item


    def close_spider(self, spider):
        nomePrefeitura = spider.name
        linkPrefeitura = spider.start_urls



        from_email = conf.email['login']
        to_email = "to@smtp.mailtrap.io"

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = 'Licitacoes da Prefeitura de ' + nomePrefeitura

        intro = "Licitacoes da Prefeitura de " + nomePrefeitura + '\n'
        linkPage = "Link para a página de licitacões: " + str(linkPrefeitura) + '\n'

        head = '======================================================================================================='
        foot = '======================================================================================================='

        body = intro + '\n' + linkPage + '\n' + '\n\n' + head + '\n' + 'Modalidade: ' + self.modalidade + '\n' + 'Objetivo: ' + " ".join(
            (self.objetivo.split())) + '\n' + 'Numero CP: ' + self.numerocp + '\n' + foot + '\n\n'



        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(conf.email['smtp_server'], conf.email['port'])
        server.starttls()
        server.login(from_email, conf.email['password'])
        text = msg.as_string()
        print("###### Enviando Email...######")
        server.sendmail(from_email, to_email, text)
        print('Email Enviado!!')
        server.quit()
        print('######## Fechando spider...#########')



