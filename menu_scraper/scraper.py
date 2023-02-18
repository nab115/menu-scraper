import os
import re

import requests
import bs4
from queue import Queue

from menu_scraper.utils import TopN, Item
from menu_scraper.load import get_restaurant_menu


def extract_menu_items(url, restaurant_name):

    html = get_restaurant_menu(url, restaurant_name)

    soup = bs4.BeautifulSoup(html, 'html.parser')
    body = soup.find('body')

    [desc_key, name_key] = extract_html_menu_keys(body, 2, re.compile('[A-Za-z]+'))
    [price_key] = extract_html_menu_keys(body, 1, re.compile('[$]*[0-9]+[.]?[0-9]*'))
    
    menu_items = create_menu_items_list(
        body
        , name_key
        , desc_key
        , price_key
    )

    for item in menu_items:
        print(str(item) + '\n')

    return menu_items

def convert_price_text(text):
    price = []
    for c in text:
        if (c.isdigit() or c == '.'):
            price.append(c)
    
    return ''.join(price)

def key_from_element(e):
    try:
        class_name = ' '.join(e['class'])
    except:
        class_name = ''

    return e.name + '|' + class_name

def create_menu_items_list(body, name_key, desc_key, price_key):
    
    # TODO - modify MongoDB collection so that it can accept items
    # without a description or price, and just fill them in with '' or None
    # That way we can just create an empty dictionary here

    menu_items = []
    def empty_menu_item_json():
        return  {
        'name': ''
        , 'description': ''
        , 'price': None
    }

    item = empty_menu_item_json()

    for element in body.find_all():
        key = key_from_element(element)
        text = element.get_text()
        if key == name_key:
            if(item['name']):
                menu_items.append(item)
                item = empty_menu_item_json()
            item['name'] = text
        elif key == desc_key:
            if(item['description']):
                menu_items.append(item)
                item = empty_menu_item_json()
            item['description'] = text
        elif key == price_key:
            if(item['price']):
                menu_items.append(item)
                item = empty_menu_item_json()
            item['price'] = convert_price_text(text)
    
    menu_items.append(item)

    return menu_items

# TODO - need additional logic to target price field
# hitting edge case where there are multiple equal frequency keys with text
# bc of poor HTML structure.
def extract_html_menu_keys(html_body, n, pattern=None):

    keys_to_stats = calculate_html_key_stats(html_body, pattern)

    keys_freq = TopN(n)

    for k in keys_to_stats:
        keys_freq.push(Item(k, keys_to_stats[k][0]))

    menu_keys_average_chars = []
    for item in keys_freq.getTopN():
        menu_keys_average_chars.append(Item(item.id, keys_to_stats[item.id][1]))
    
    menu_keys_average_chars.sort(reverse=True)

    print(menu_keys_average_chars)

    return [key.id for key in menu_keys_average_chars]

def calculate_html_key_stats(html_body, pattern):

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

        try:
            class_name = ' '.join(element['class'])
        except:
            class_name = ''
        key = element.name + '|' + class_name
        
        strings = element.find_all(string=True, recursive=False)
        text = ''.join([s.strip() for s in strings])

        if (not pattern or pattern.search(''.join(text).strip())):

            # map_ value will be a list of length 2
            # index 0 representing frequency
            # index 1 representing sum of number of chars in text
            if key in map_:
                map_[key][0] = map_[key][0] + 1
                map_[key][1] = map_[key][1] + len(text)
            else:
                map_[key] = [1, len(text)]
            
        for child in element.contents:
            queue.put(child)
    

    # TODO edge case where, say, a description isn't filled in will cause
    # the corresponding html key to have a lower character average than it should

    # convert total # of chars to average
    for k in map_:
        map_[k][1] = map_[k][1] / map_[k][0]
    
    return map_