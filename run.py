import menu_scraper as ms

restaurants = [
    {
        "name": "elmoose"
        , "url": "https://www.elmoose.com/dinner"
    }
    , {
        "name": "slab_sandwich"
        , "url": "http://www.slabsandwich.com/"
    }
    , {
        "name": "8ozburger"
        , "url": "https://www.8ozburgerandco.com/"
    }
]

for r in restaurants:
    items = ms.extract_menu_items(r['url'], r['name'])
    ms.write_restuarant_to_db(r['name'], items)