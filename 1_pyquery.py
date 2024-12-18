import concurrent.futures
from pyquery import PyQuery as pq
import requests

url = "https://www.rusplitka.ru/catalog/"
urls = []


# функция, с помощью которой мы парсим, он принимает переменную - ссылку сайта
def parse_page(url_part):
    results = []
    response = requests.get(url_part)
    doc = pq(response.content)
    products = doc('.item.item__3-col.desktop')
    for i in products:
        if pq(i).find(".item__in_store"):
            title = pq(i).find(".item__name").text()
            price = int(pq(i).find(".item__price").text()[3:7])
            href = pq(i).find(".item__name").attr('href')
            results.append({'Название плитки': title,
                            'Цена': price,
                            'Ссылка': 'https://www.rusplitka.ru' + href})
    for result in results:
        print(result)


# Составление списка ссылок сатов
def all_urls(u):
    for i in range(1, 312):
        if i == 1:
            u.append('https://www.rusplitka.ru/catalog/')
        else:
            u.append(url + f'page-{i}')


all_urls(urls)

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(parse_page, urls)










