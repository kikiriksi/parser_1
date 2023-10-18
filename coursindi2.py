from bs4 import BeautifulSoup
import requests

summ_all = 0
url = 'https://parsinger.ru/html/index1_page_1.html'
response = requests.get(url)
response.encoding = 'utf-8'
group_all = [i['href'] for i in
             BeautifulSoup(response.text, 'lxml').find('div', {'class': 'nav_menu'}).find_all('a')]  # Список групп
for group in group_all:
    '''узнаем количество страниц в каждой группе'''
    pages_response = requests.get(f'https://parsinger.ru/html/{group}')
    pages_response.encoding = 'utf-8'
    pages_soup = [i['href'] for i in BeautifulSoup(pages_response.text, 'lxml').find('div', 'pagen').find_all('a')]
    for quantity in pages_soup:
        '''узнаем ссылки на каждый товар на странице'''
        quantity_response = requests.get(f'https://parsinger.ru/html/{quantity}')
        quantity_response.encoding = 'utf-8'
        quantity_soup = [i['href'] for i in
                         BeautifulSoup(quantity_response.text, 'lxml').find_all('a', {'class': 'name_item'})]
        for name in quantity_soup:
            '''находи цену товара и его количество'''
            response_end = requests.get(f'https://parsinger.ru/html/{name}')
            in_stock = BeautifulSoup(response_end.text, 'lxml').find('span', id='in_stock')
            price = BeautifulSoup(response_end.text, 'lxml').find('span', id='price')
            summ_all += int(in_stock.text.split()[-1]) * int(price.text.split()[0])
print(summ_all)
