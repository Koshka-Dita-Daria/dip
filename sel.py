import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import pandas as pd


url = "https://www.rusplitka.ru/catalog/"
results = []
urls = []
new_href = ''


def check(obj):
    try:
        elem = obj.find_element(By.CLASS_NAME, "item__in_store")
        return True
    except NoSuchElementException:
        return False


def parsing():
    products = driver.find_elements(By.CLASS_NAME, 'item.item__3-col.desktop')
    for product in products:
        a = product.find_element(By.CLASS_NAME, "item__name")
        href = product.find_element(By.CLASS_NAME, "item__name").get_attribute('href')
        have = check(product)
        if have is True:
            title = a.text
            price = product.find_element(By.CLASS_NAME, "item__price").text[3:7]
            # image = product.find_element(By.CLASS_NAME, 'img').get_attribute('src')
            results.append({'Название плитки': title,
                            'Цена': int(price),
                            # 'Изображение': 'https://www.rusplitka.ru' + image,
                            'Ссылка': 'https://www.rusplitka.ru' + href})
        else:
            continue


start = time.time()

driver = webdriver.Chrome()

try:
    # Открываем сайт
    driver.get(url)
    # button = driver.find_element(By.XPATH, "//label[contains(text(), 'Плитка')]")

    # ActionChains(driver).move_to_element(button).click(button).perform()
    # time.sleep(4)
    # button_all = driver.find_element(By.CSS_SELECTOR, "#modef")
    # time.sleep(4)
    # ActionChains(driver).move_to_element(button_all).click(button_all).perform()
    # driver.implicitly_wait(10)
    # time.sleep(4)

    for i in range(1, 4):
        time.sleep(4)
        parsing()
        time.sleep(4)
        next_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Далее >')]")
        ActionChains(driver).move_to_element(next_button).click(next_button).perform()
        driver.get(driver.current_url)
        driver.implicitly_wait(10)
        time.sleep(4)
finally:
    driver.quit()


z = pd.DataFrame(results)
data_to_excel = pd.ExcelWriter('selenium.xlsx')
z.to_excel(data_to_excel)
data_to_excel.close()


end = time.time()
print(end-start)

# Закрываем браузер


# driver.get(new_href)
