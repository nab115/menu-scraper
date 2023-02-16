import menu_scraper as ms
import os

def test_extract_menu_items_cached():
    ms.extract_menu_items('bad_url', 'elmoose')
    assert True

def test_extract_menu_items_noncached():
    ms.extract_menu_items('https://www.elmoose.com/dinner', 'elmoose2')
    os.remove("menu_scraper/restaurants/elmoose2_menu.txt")
    assert True