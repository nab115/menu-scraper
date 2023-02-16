import json
from selenium.webdriver.common.by import By

from menu_scraper.utils import get_chrome_driver

def get_restaurant_menu(url, name):

    filename = 'menu_scraper/restaurants' + '/' + name + '_menu.txt'
    try:
        with open(filename, 'r') as f:
            html = f.read()

    except:
        print(filename + ' not found')
        driver = get_chrome_driver()
        driver.get(url)
        elements = driver.find_elements(By.TAG_NAME, 'html')
        f = open(filename, 'w')
        html = elements[0].get_attribute("innerHTML")
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

