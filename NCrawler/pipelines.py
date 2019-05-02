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

from scrapy.exceptions import DropItem


class FilterDatePipeline(object):
    def process_item(self, item, spider):

        now = datetime.date.today().year
        date_licitacao = int(item['numerocp'][0].split('/')[-1])
        if int(date_licitacao) == now:
            print(date_licitacao)
            return item
        else:
            raise DropItem("Licitação fora do ano atual")

class FilterModalidade(object):
    def process_item(self, item, spider):
        pregaoEletronico = 'PREGÃO ELETRONICO'
        pregaoPresencial = 'PREGÃO PRESENCIAL'
        modalidade = str(item['modalidade']).upper()
        if pregaoPresencial in modalidade:
            print('Pregão Presencial em', modalidade)
            return item
        elif pregaoEletronico in modalidade:
            print('Pregão Eletronico em', modalidade)
            return item
        else:
            raise DropItem("Item não é Pregão Presencial ou Pregão Eletronico")



class SendMail(object):

    def open_spider(self, spider):
        print("######### Iniciando o spider... #########")

    def process_item(self, item, spider):


        print("######## Processando pipelines... ##########")

        self.modalidade = str(item['modalidade'])
        self.objetivo = str(item['objetivo'])
        self.numerocp = str(item['numerocp'])

        return item

    def close_spider(self, spider):

        nomePrefeitura = spider.name
        linkPrefeitura = spider.start_urls

        from_email = "b89b239862ecb5"
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

        server = smtplib.SMTP("smtp.mailtrap.io", 2525)
        server.starttls()
        server.login(from_email, "f20851757ed914")
        text = msg.as_string()
        print("###### Enviando Email...######")
        server.sendmail(from_email, to_email, text)
        print('Email Enviado!!')
        server.quit()
        print('######## Fechando spider...#########')
