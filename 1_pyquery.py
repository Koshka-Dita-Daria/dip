import concurrent.futures
from pyquery import PyQuery as pq
import requests
from concurrent.futures import ThreadPoolExecutor
url = "https://www.rusplitka.ru/catalog/"
urls = []


def parse_page(url_part):
    results = []
    response = requests.get(url_part)
    doc = pq(response.content)
    products = doc('.item.item__3-col.desktop')
    for i in products:
        if pq(i).find(".item__in_store"):
            results.append({'Название плитки': pq(i).find(".item__name").text(),
                            'Цена': int(pq(i).find(".item__price").text()[3:7]),
                            'Ссылка': 'https://www.rusplitka.ru' + pq(i).find(".item__name").attr('href')})
    for result in results:
        print(result)


def all_urls(u):
    for i in range(1, 312):
        if i == 1:
            u.append('https://www.rusplitka.ru/catalog/')
        else:
            u.append(url + f'page-{i}')


all_urls(urls)

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    # executor.map(all_urls, urls)
    executor.map(parse_page, urls)










