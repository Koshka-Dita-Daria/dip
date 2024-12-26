import time

import requests
from bs4 import BeautifulSoup
import concurrent.futures
import pandas as pd

url = 'https://www.rusplitka.ru/catalog/%s'
results = []
urls = []


def parsing(u):
    response = requests.get(u)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        products = soup.find_all('div', class_='item item__3-col desktop')
        for product in products:
            check = product.find('div', class_='item__in_store')
            a = product.find('a', class_='item__name')
            href = a.get('href')
            if not (check is None):
                title = a.text
                price = product.find('div', class_='item__price').text
                # image = product.find('img').get('src')
                results.append({'Название плитки': title.strip(),
                                'Цена': int(price.strip()[15:-8]),
                                # 'Изображение': 'https://www.rusplitka.ru' + image,
                                'Ссылка': 'https://www.rusplitka.ru' + href})

    else:
        print(f"Ошибка при запросе страницы: {response.status_code}")


start = time.time()


for i in range(1, 5):
    # 311
    if i == 1:
        k = 'https://www.rusplitka.ru/catalog/'
    else:
        k = url % f'/page-{i}'
    urls.append(k)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.map(parsing, urls)


z = pd.DataFrame(results)
data_to_excel = pd.ExcelWriter('Beat.xlsx')
z.to_excel(data_to_excel)
data_to_excel.close()

end = time.time()
print(end-start)
