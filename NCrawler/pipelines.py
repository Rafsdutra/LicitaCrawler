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
import codecs
import json
from scrapy.exceptions import DropItem

from NCrawler.services.filters import relevance


class FilterSimilarityPipeline(object):
    def process_item(self, item, spider):
        print(relevance(item['objetivo']))
        if relevance(item['objetivo']) >= 0.0:
            print("FILTRO DE SIMILARIDADE: OK")
            return item
        else:
            raise DropItem("FILTRO DE SIMILARIDADE: Licitação não é relacionada a marketing")


class FilterEmailEnviado(object):
    def process_item(self, item, spider):
        # info = []
        numcp = str(item['numerocp']),
        Prefeitura = spider.name

        with open('Emails.txt') as f:
            content = f.read()
            if str(numcp) in content:
                raise DropItem('Email já foi enviado! Cancelando Operação!')
            else:

                f = open('Emails.txt', 'a')
                f.write('Prefeitura: ' + Prefeitura)
                f.write('\n')
                f.write('Numero CP: ' + str(numcp))
                f.write('\n\n')
                f.close()

                return item


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
    def __init__(self):
        self.to_email = "to@smtp.mailtrap.io"
        self.licitacoes = []

    def open_spider(self, spider):
        print("######### Iniciando o spider... #########")

    def process_item(self, item, spider):
        print("######## Processando pipelines... ############")

        self.licitacoes.append({
            'modalidade': str(item['modalidade']),
            'objetivo': str(item['objetivo']),
            'ncp': str(item['numerocp']),
            'link': str(item['link'])
        })

        return item

    def close_spider(self, spider):
        if len(self.licitacoes) <= 0:
            print('sem licitações')
            return

        idMail = 1

        nomePrefeitura = spider.name
        msg = MIMEMultipart()
        msg['From'] = conf.email['login']
        msg['To'] = self.to_email
        msg['Subject'] = 'Licitacoes da Prefeitura de ' + nomePrefeitura

        template = conf.env.get_template('email.html')
        content = template.render(
            cidade=nomePrefeitura,
            licitacoes=self.licitacoes
        )
        msg.attach(MIMEText(content, 'html'))
        server = smtplib.SMTP(conf.email['smtp_server'], conf.email['port'])
        server.starttls()
        server.login(conf.email['login'], conf.email['password'])
        text = msg.as_string()

        print("###### Enviando Email...######")
        server.sendmail(conf.email['login'], self.to_email, text)
        print("Email enviado com sucesso!")
        server.quit()

        print('######## Fechando spider...#########')
