import json
from selenium.webdriver.common.by import By

from menu_scraper.utils import get_chrome_driver

def get_restaurant_menu(url, name):

    filename = 'menu_scraper/restaurants' + '/' + name + '_menu.txt'
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            html = f.read()
        f.close()

    except:
        print(filename + ' not found. Fetching HTML')
        html = fetch_restaurant_html(url)
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(html)
        f.close()

    return html

def get_restaurant_info(name):

    try:
        f = open('menu_scraper/restaurants' + '/' + restaurant_name + '_info.json', 'r')
        return json.load(f)
    except:
        print(f'No info json for {restaurant_name}')
        return None

def fetch_restaurant_html(url):
    driver = get_chrome_driver()
    driver.get(url)
    elements = driver.find_elements(By.TAG_NAME, 'html')
    return elements[0].get_attribute("innerHTML")

