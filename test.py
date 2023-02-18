import menu_scraper as ms
import os
import pytest

@pytest.mark.skip
def test_extract_menu_items_cached():
    ms.extract_menu_items('bad_url', 'elmoose')
    assert True


def test_extract_menu_items_elmoose():
    ms.extract_menu_items('https://www.elmoose.com/dinner', 'elmoose2')
    os.remove("menu_scraper/restaurants/elmoose2_menu.txt")
    assert True

def test_extract_menu_items_slab():
    ms.extract_menu_items('http://www.slabsandwich.com/', 'slab_sandwich')
    assert True