import menu_scraper as ms

restaurants = [
    {
        "name":"fogon_cocina"
        , "url": "https://fogonseattle.com/food-menu/"
    }
]

for r in restaurants:
    r = ms.create_restaurant_object(r['url'], 'elmoose', '123', 'seattle')
    print(r)
    # ms.write_restuarant_to_db(r['name'], items)