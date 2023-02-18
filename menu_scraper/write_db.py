import os

from menu_scraper.utils import get_db_client
from menu_scraper.load import get_restaurant_info

def write_restuarant_to_db(restaurant_name, menu_items):
    
    restaurant_info = get_restaurant_info(restaurant_name)

    col = get_db_client(
        os.environ.get('MONGODB_USERNAME')
        , os.environ.get('MONGODB_PASSWORD')
    )['Restaurants']['restaurants']

    restaurant_info['items'] = menu_items

    col.insert_one(restaurant_info)