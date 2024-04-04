# test_search.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import os

class TestSearch:
    def sign_in(self, driver, user):
        # Sign in
        driver.get("http://localhost:3000/")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(user['email'])
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(user['password'])
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
        assert "/home" in driver.current_url
    
    def test_SEARCH_user(self, setup_user, driver, setup_user_group):
        # Test if the user can search for a user
        user, sUser, sGroup = setup_user_group
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/search")
        driver.find_element(By.XPATH, "//div[text()='Select Type']").click()
        driver.find_element(By.CSS_SELECTOR, "li[data-value='users']").click()
        search_field = driver.find_element(By.CSS_SELECTOR, "textarea")
        search_field.send_keys(sUser['userName'])
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        print()

    def test_SEARCH_group(self, setup_user_group, driver):
        # Test if the user can search for a group
        user, sUser, sGroup = setup_user_group
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/search")
        driver.find_element(By.XPATH, "//div[text()='Select Type']").click()
        driver.find_element(By.CSS_SELECTOR, "li[data-value='groups']").click()
        search_field = driver.find_element(By.CSS_SELECTOR, "textarea")
        search_field.send_keys(sGroup['groupName'])
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        print()