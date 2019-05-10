from jinja2 import Environment, select_autoescape, FileSystemLoader

email = {'smtp_server': 'smtp.mailtrap.io',
         'port': '2525',
         'login': 'login',
         'password': 'password'}

env = Environment(
    loader=FileSystemLoader('./assets/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)