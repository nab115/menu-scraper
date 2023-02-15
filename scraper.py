import os
import json

import requests
import bs4
from selenium.webdriver.common.by import By
from queue import Queue

from utils import get_chrome_driver, TopN, Item, get_db_client


def run():

    restaurant_name = 'elmoose'

    f = open('./restaurants' + '/' + restaurant_name + '_menu.txt', 'r')
    html = f.read()
    f.close()

    soup = bs4.BeautifulSoup(html, 'html.parser')
    body = soup.find('body')

    [desc, name, price] = extract_html_menu_keys(body)
    menu_items = create_menu_items_list(desc, name, price, body)

    for item in menu_items:
        print(str(item) + '\n')

    json_file = open('./restaurants' + '/' + restaurant_name + '_info.json', 'r')
    restaurant_info = json.load(json_file)

    write_restuarant_to_db(restaurant_info, menu_items)


def write_restuarant_to_db(restuarant_info, menu_items):

    col = get_db_client(
        os.environ.get('MONGODB_USERNAME')
        , os.environ.get('MONGODB_PASSWORD')
    )['Restaurants']['restaurants']

    restuarant_info['items'] = menu_items

    col.insert_one(restuarant_info)




def create_menu_items_list(desc, name, price, html_body):

    menu_items = []
    names = html_body.find_all(name.split('|')[0], {'class':  name.split('|')[1]})
    descriptions = html_body.find_all(desc.split('|')[0], {'class':  desc.split('|')[1]})
    prices = html_body.find_all(price.split('|')[0], {'class':  price.split('|')[1]})

    for(n, d, p) in zip(names, descriptions, prices):

        # TODO - better way to extract non numerical characters from price
        # probably should do this upstream
        menu_items.append(
            {
                'name': n.get_text()
                , 'description': d.get_text()
                , 'price': float(p.get_text()[1:])
            }
        )
    
    return menu_items

def extract_html_menu_keys(html_body):

    keys_to_stats = calculate_html_key_stats(html_body)

    # assuming that the top 3 (by frequency) html keys with text
    # will be the menu item name, description, and price, since these
    # should show up the most frequently on a menu
    keys_freq = TopN(3)

    for k in keys_to_stats:
        keys_freq.push(Item(k, keys_to_stats[k][0]))

    menu_keys_average_chars = []
    for item in keys_freq.getTopN():
        menu_keys_average_chars.append(Item(item.id, keys_to_stats[item.id][1]))
    
    menu_keys_average_chars.sort(reverse=True)

    return [key.id for key in menu_keys_average_chars]

def calculate_html_key_stats(html_body):

    # Traverse through HTML body using BFS
    queue = Queue()
    map_ = {}
    queue.put(html_body)

    while not queue.empty():
        element = queue.get()

        # these elements do not have inner text or children
        # and will throw errors if subsequent code is run
        if type(element) in [
            bs4.element.NavigableString
            , bs4.element.Comment
            , bs4.element.Stylesheet
            , bs4.element.Script
        ]:
            continue

        text = element.find_all(string=True, recursive=False)
        
        # assuming that valid menu key candidates will have
        # just 1 direct text element
        if len(text) == 1:
            try: 
                class_name = ' '.join(element['class'])
            except:
                class_name = ''

            key = element.name + '|' + class_name
            # map_ value will be a list of length 2
            # index 0 representing frequency
            # index 1 representing sum of number of chars in text
            if key in map_:
                map_[key][0] = map_[key][0] + 1
                map_[key][1] = map_[key][1] + len(text[0])
            else:
                map_[key] = [1, len(text[0])]
        
        for child in element.contents:
            queue.put(child)
    

    # TODO edge case where, say, a description isn't filled in will cause
    # the corresponding html key to have a lower character average than it should

    # convert total # of chars to average
    for k in map_:
        map_[k][1] = map_[k][1] / map_[k][0]
    
    return map_


def retrieve_menu():
    driver = get_chrome_driver()
    driver.get("https://www.elmoose.com/dinner")
    elements = driver.find_elements(By.TAG_NAME, 'html')
    f = open('menu.txt', 'w')
    f.write(elements[0].get_attribute("innerHTML"))


if __name__ == '__main__':
    run()