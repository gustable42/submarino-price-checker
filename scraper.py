import requests
import os
from bs4 import BeautifulSoup
import smtplib

def check_prices(url, max_price, headers):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    product_title = soup.find(id="product-name-default").get_text()
    prices = soup.findAll("span", {"class": "sales-price"})
    lowest_price = 9999999.99

    for idx, price in enumerate(prices):
        price = price.get_text()
        price = float((price[0: 0:] + price[2 + 1::]).replace(',', '.'))
        if(price < lowest_price):
            lowest_price = price

    if(lowest_price <= max_price):
        return True
    else:
        return False


def parse_mail_body(headers):
    urls_file = open("data/urls.txt", "r")
    urls = []
    prices = []

    body = "Alguns produtos estão abaixo do valor desejado!\n"

    for line in urls_file:
        splitted_line = line.split(' ')
        url = splitted_line[0]
        price = splitted_line[1]
        if(price[-1] == '\n'):
            price = price[:-1]
        urls.append(url)
        prices.append(price)

    below_max_price = 0

    for url, price in zip(urls, prices):
        if(check_prices(url, float(price), headers)):
            below_max_price += 1
            body += url + "\n"

    if(below_max_price > 0):
        return body
    else:
        return None


def send_mail(mail_body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    mail = password = ""
    mail_credentials = open('./data/mail.txt', 'r')

    for line in mail_credentials:
        splitted_line = line.split(' ')
        mail = splitted_line[0]
        password = splitted_line[1]

    server.login(mail, password)

    subject = 'Alerta de preços SUBMARINO'
    body = mail_body
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        mail,
        mail,
        msg.encode('utf-8')
    )
    print("Email enviado")


def create_urls_file():
    use_file = 'n'
    if(os.path.isfile("./data/urls.txt")):
        while True:
            use_file = input("Deseja utilizar as URLs já cadastradas? (S/n)")
            if(use_file == 'n' or use_file == 'S'):
                break

    if(use_file == 'n'):
        number_of_urls = int(input("Insira o número de links que deseja cadastrar:"))
        URLs = []

        for x in range(number_of_urls):
            temp_url = input("URL do produto Submarino: ")
            max_price = input("Valor máximo que você pagaria pelo produto: ")
            identation = "\n"
            if(x == number_of_urls - 1):
                identation = ''
            URLs.append(temp_url + ' ' + max_price + identation)

        file_to_write = open("data/urls.txt", "w")
        file_to_write.writelines(URLs)
        file_to_write.close()


def create_mail_file():
    use_file = 'S'
    if(os.path.isfile("./data/mail.txt")):
        while True:
            use_file = input("Deseja utilizar o email já cadastrado? (S/n)")
            if(use_file == 'n' or use_file == 'S'):
                break

    if(use_file == 'n' or not os.path.isfile("./data/mail.txt")):
        mail = input("Insira o email que deseja receber as notificações ")
        print("Insira a senha do seu email: ")
        print("Gere uma senha apenas para esse uso, caso não saiba acesse o link abaixo")
        print("https://support.google.com/accounts/answer/185833?hl=pt-BR&authuser=1")
        password = input()

        file_to_write = open("data/mail.txt", "w")
        file_to_write.write(mail + ' ')
        file_to_write.write(password)
        file_to_write.close()


headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

create_mail_file()
create_urls_file()
body = parse_mail_body(headers)
if(body):
    send_mail(body)
