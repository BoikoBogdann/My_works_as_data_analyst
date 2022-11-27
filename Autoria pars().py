import requests
from bs4 import BeautifulSoup
import csv
import os


HOST = 'https://auto.ria.com/uk/'
URL = 'https://auto.ria.com/uk/newauto/marka-mercedes-benz/'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
FILE = 'cars.csv'

def get_html(url, params = ''):
    r = requests.get(url, headers = HEADERS , params = params)
    return r
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1




def get_content(html):
    soup = BeautifulSoup(html , 'html.parser')
    items = soup.find_all('a', class_='proposition_link')

    cars = []
    for item in items:
        cars.append(
            {
                'title': item.find('span', class_='link').get_text(),
                'price in uah': item.find('span', class_='size16').get_text(),
                'price in $': item.find('span', class_='size22').get_text(),
            
             }
        )
    return (cars)

def save_file(items,path):
    with open(path,'w',newline='') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(['Модель', 'Цена в гривне', 'Цена в $'])
        for item in items:
            writer.writerow([item ['title'],item ['price in uah'] , item ['price in $']])



def parse():
    URL = input('Введите URL:')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1,pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print (f'Получено {len(cars)} автомобилей')
        print(os.startfile(FILE))
    else:
        print('error')



parse()





