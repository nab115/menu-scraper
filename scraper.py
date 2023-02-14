import os
from time import sleep

import requests
import bs4
from selenium.webdriver.common.by import By
from queue import Queue

from utils import get_chrome_driver, TopN, Item


def run():

    restaurant_name = 'elmoose'

    f = open('./menus' + '/' + restaurant_name + '.txt', 'r')
    html = f.read()
    f.close()

    soup = bs4.BeautifulSoup(html, 'html.parser')
    body = soup.find('body')

    [item_desc, item_name, item_price] = find_menu_keys(body)

    [tag, class_name] = item_name.split('|')
    names = body.find_all(tag, {'class': class_name})
    for name in names[:5]:
        print(name.getText() + '\n')
    
    [tag, class_name] = item_desc.split('|')
    names = body.find_all(tag, {'class': class_name})
    for name in names[:5]:
        print(name.getText() + '\n')
    
    [tag, class_name] = item_price.split('|')
    names = body.find_all(tag, {'class': class_name})
    for name in names[:5]:
        print(name.getText() + '\n')


def find_menu_keys(body):

    # Traverse through HTML body using BFS or DFS
    q = Queue()
    hashmap = {}
    q.put(body)

    while not q.empty():
        element = q.get()

        if type(element) in [
            bs4.element.NavigableString
            , bs4.element.Comment
            , bs4.element.Stylesheet
            , bs4.element.Script
        ]:
            continue

        text = element.find_all(string=True, recursive=False)

        if len(text) == 1:
            try: 
                class_name = ' '.join(element['class'])
            except:
                class_name = ''

            key = element.name + '|' + class_name
            if key in hashmap:
                hashmap[key][0] = hashmap[key][0] + 1
                hashmap[key][1] = hashmap[key][1] + len(text[0])
            else:
                hashmap[key] = [1, len(text[0])]
        
        for child in element.contents:
            q.put(child)
    
    top3 = TopN(3)
    for k in hashmap:
        hashmap[k][1] = hashmap[k][1] / hashmap[k][0]
        top3.push(Item(k, hashmap[k][0]))

    tags = []
    for item in top3.getTopN():
        tags.append(Item(item.id, hashmap[item.id][1]))
    
    tags.sort(reverse=True)

    return [tag.id for tag in tags]


def retrieve_menu():
    driver = get_chrome_driver()
    driver.get("https://www.elmoose.com/dinner")
    elements = driver.find_elements(By.TAG_NAME, 'html')
    f = open('menu.txt', 'w')
    f.write(elements[0].get_attribute("innerHTML"))


if __name__ == '__main__':
    run()
    