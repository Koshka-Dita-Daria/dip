import requests
from bs4 import BeautifulSoup

url = 'https://www.rusplitka.ru/catalog/%s'
results = []


def main(response):
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        tiles = soup.find_all('div', class_='item item__3-col desktop')
        for tile in tiles:
            check = tile.find('div', class_='item__in_store')
            if not (check is None):
                a = tile.find('a', class_='item__name')
                title = a.text
                hr = a.get('href')
                price = tile.find('div', class_='item__price').text
                results.append({'title': title.strip(),
                                'price': int(price.strip()[15:-8]),
                                'href': 'https://www.rusplitka.ru' + hr})
    else:
        print(f"Ошибка при запросе страницы: {response.status_code}")


for i in range(1, 2):
    # 311
    if i == 1:
        k = 'https://www.rusplitka.ru/catalog/'
        response = requests.get(k)
    else:
        response = requests.get(url % f'/page-{i}')
    main(response)

