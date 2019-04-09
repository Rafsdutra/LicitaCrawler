# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from scrapy.exceptions import DropItem
import smtplib





class FilterDatePipeline(object):
    def process_item(self, item, spider):
        now = datetime.now()
        date_licitacao = int(item['numerocp'][0].split('/')[-1])
        if int(date_licitacao) == now.year:
            print(date_licitacao)
            return item
        else:
            raise DropItem("Licitação fora do ano atual")


class sendMail(object):

    def close_spider(self, spider):

        print('Enviando Email com as informações de Licitação...')
        from_email = "b89b239862ecb5"
        to_email = "to@smtp.mailtrap.io"

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = 'Licitacoes '

        intro = "Licitacoes: \n\n"

        body = 'Oi'
        body = intro + body
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP("smtp.mailtrap.io", 2525)
        server.starttls()
        server.login(from_email, "f20851757ed914")
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()

        print('Email enviado! ')



