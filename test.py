import menu_scraper as ms
import os
import pytest

@pytest.mark.skip
def test_extract_menu_items_cached():
    ms.extract_menu_items('bad_url', 'elmoose')
    assert True

# @pytest.mark.skip
def test_extract_menu_items_elmoose():
    ms.extract_menu_items('https://www.elmoose.com/dinner', 'elmoose')

    assert True

# @pytest.mark.skip
def test_extract_menu_items_slab():
    ms.extract_menu_items('http://www.slabsandwich.com/', 'slab_sandwich')
    assert True

# @pytest.mark.skip
def test_extract_menu_items_8oz():
    ms.extract_menu_items('https://www.8ozburgerandco.com/', '8ozburger')
    assert True