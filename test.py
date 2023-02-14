import os

import requests
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from utils import get_chrome_driver

restaurant_name = 'elmoose'

f = open('./menus' + '/' + restaurant_name + '.txt', 'r')

html = f.read()
soup = BeautifulSoup(html, 'html.parser')

# body = soup.find('body', {"class": "yext-menu-item-name yext-accentcolor"})
body = soup.find('body')
l = body.find_all(string=True, recursive=False)
print(body.name)
print(body['class'])

# for name in names:
#     print(name.getText() + '\n')