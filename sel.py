from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import concurrent.futures
url = "https://www.rusplitka.ru/catalog/"
results = []
urls = []


def all_urls(u):
    for i in range(1, 2):
        if i == 1:
            u.append('https://www.rusplitka.ru/catalog/')
        else:
            u.append(url + f'page-{i}')


all_urls(urls)


def parsing(url_part):
    driver = webdriver.Chrome()
    driver.get(url_part)
    time.sleep(10)
    products = driver.find_elements(By.CLASS_NAME, "item.item__3-col.desktop")
    for product in products:
        if product.find_element(By.CLASS_NAME, "item__in_store"):
            results.append({'title': product.find_element(By.XPATH, "//*[@class='item__name']").text,
                            'price': product.find_element(By.CLASS_NAME, "item__price").text[3:7],
                            'href':  product.find_element(By.CLASS_NAME, "item__name").get_attribute('href')})
    driver.quit()


with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    # executor.map(all_urls, urls)
    executor.map(parsing, urls)
print(results)