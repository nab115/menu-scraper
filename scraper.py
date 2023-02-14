import os
from time import sleep

import requests
import bs4
from selenium.webdriver.common.by import By
from queue import Queue

from utils import get_chrome_driver

def run():

    restaurant_name = 'elmoose'

    f = open('./menus' + '/' + restaurant_name + '.txt', 'r')
    html = f.read()
    f.close()

    parse_html_text(html)

def parse_html_text(html):

    soup = bs4.BeautifulSoup(html, 'html.parser')
    body = soup.find('body')

    # Traverse through HTML body using BFS or DFS
    q = Queue()
    hashmap = {}
    q.put(body)

    while not q.empty():
        element = q.get()
        
        try:
            children = element.contents
            text = element.find_all(string=True, recursive=False)
        except:
            print(element.contents)
            print(element.parent.name)
            print(element.parent.parent.name)
            break
            continue

        if len(text) == 1:
            try: 
                class_name = ' '.join(element['class'])
            except:
                class_name = ''

            key = element.name + ' ' + class_name
            if key in hashmap:
                hashmap[key][0] = hashmap[key][0] + 1
                hashmap[key][1] = hashmap[key][1] + len(text[0])
            else:
                hashmap[key] = [1, len(text[0])]
        
        for child in children:
            q.put(child)
    
    for k in hashmap:
        hashmap[k][1] = hashmap[k][1] / hashmap[k][0]
    print(hashmap)

def retrieve_menu():
    driver = get_chrome_driver()
    driver.get("https://www.elmoose.com/dinner")
    elements = driver.find_elements(By.TAG_NAME, 'html')
    f = open('menu.txt', 'w')
    f.write(elements[0].get_attribute("innerHTML"))



if __name__ == '__main__':
    run()
    