
import requests
from bs4 import BeautifulSoup
import csv

# PROXY = {'https': '127.0.0.1:8080', 'http': '127.0.0.1:8080' }
HOST = 'https://minfin.com.ua'
URL  = 'https://minfin.com.ua/ua/cards/'
HEADERS= {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user_agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Mobile Safari/537.36'
}

CVS = 'cards.cvs'



def get_html(url, params=''):
    r = requests.get(
        url, 
        # proxies=PROXY,
        headers=HEADERS, 
        params=params,
        # verify=False
    )
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sc-182gfyr-0')
    cards = []

    for item in items: 
        cards.append(
            {
                 'title': item.find('div', class_='be80pr-15').find('a', class_='cpshbz-0').get_text(), 
                 'link_product': HOST + item.find('div', class_='be80pr-15').find('a', class_='cpshbz-0').get('href'), 
                 'brand': item.find('span', class_='be80pr-21').get_text(),  
                 'img_source': item.find('div', class_='be80pr-9').find('img').get('src'), 

            }

        )
    return cards

def save_cvs(items, path):
    with open(CVS, 'w', encoding='UTF8', newline='') as cvsfile:
        write = csv.writer(cvsfile, delimiter=';')
        write.writerow(['Название продукта','ссылка на продукт','Банк','ссылка на картинку'])
        for item in items:
             write.writerow([item['title'],item['link_product'],item['brand'],item['img_source']])


def start():
    html = get_html(URL)
    if html.ok:
        print(html.ok)
        cards = get_content(html.text)
        save_cvs(cards,CVS)
    else: 
        print('error web site')
    



start()
