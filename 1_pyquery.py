import concurrent.futures
from pyquery import PyQuery as pq
import requests
import time
import pandas as pd


url = "https://www.rusplitka.ru/catalog/"
urls = []
results = []


def parse_page(url_part):
    response = requests.get(url_part)
    doc = pq(response.content, headers={'user-agent': 'pyquery'})
    products = doc('.item.item__3-col.desktop').items()
    for product in products:
        a = pq(product).find(".item__name")
        href = pq(product).find(".item__name").attr('href')
        if pq(product).find(".item__in_store"):
            title = a.text()
            price = int(pq(product).find(".item__price").text()[3:7])
            # image = pq(product).find('img').attr('src')
            results.append({'Название плитки': title,
                            'Цена': price,
                            # 'Изображение': 'https://www.rusplitka.ru' + image,
                            'Ссылка': 'https://www.rusplitka.ru' + href})


# Составление списка ссылок сатов
def all_urls(u):
    for i in range(1, 5):
        if i == 1:
            u.append('https://www.rusplitka.ru/catalog/')
        else:
            u.append(url + f'page-{i}')


start = time.time()


all_urls(urls)


with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.map(parse_page, urls)

z = pd.DataFrame(results)
data_to_excel = pd.ExcelWriter('pyquery.xlsx')
z.to_excel(data_to_excel)
data_to_excel.close()
end = time.time()
print(end-start)









