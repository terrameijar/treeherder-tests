import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
import time


from pages.treeherder import TreeherderPage

def test_move_to_top_of_range(base_url, selenium):
    page = TreeherderPage(base_url, selenium).open()
    time.sleep(10)
    action_menu_drop_down_element = (By.CSS_SELECTOR, ".th-view-content > ng-view:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3) > th-action-button:nth-child(4) > span:nth-child(1) > button:nth-child(1)")
    page.find_element(action_menu_drop_down_element).click()
    top_of_range_element = (By.CSS_SELECTOR,".th-view-content > ng-view:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3) > th-action-button:nth-child(4) > span:nth-child(1) > ul:nth-child(2) > li:nth-child(7) > a:nth-child(1)")
    page.find_element(top_of_range_element).click()
    time.sleep(10)
    assert "&tochange=" in page.selenium.current_url
    time.sleep(10)

def test_move_to_bottom_of_range(base_url, selenium):
    page = TreeherderPage(base_url, selenium).open()
    time.sleep(10)
    action_menu_drop_down_element = (By.CSS_SELECTOR, ".th-view-content > ng-view:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3) > th-action-button:nth-child(4) > span:nth-child(1) > button:nth-child(1)")
    bottom_of_range_element= (By.CSS_SELECTOR, ".th-view-content > ng-view:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3) > th-action-button:nth-child(4) > span:nth-child(1) > ul:nth-child(2) > li:nth-child(8) > a:nth-child(1)")
    page.find_element(action_menu_drop_down_element).click()
    page.find_element(bottom_of_range_element).click()
    time.sleep(10)
    assert "fromchange=" in page.selenium.current_url