import json
from requests_html import HTMLSession


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
        f = open('menu_scraper/restaurants' + '/' + name + '_info.json', 'r')
        return json.load(f)
    except:
        print(f'No info json for {name}')
        return None

def fetch_restaurant_html(url):

    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    html = r.html.html

    return html

