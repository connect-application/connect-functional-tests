# test_edit_profile_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import os
import requests
import time
class TestEditProfilePage:
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
        search_button = driver.find_element(By.XPATH, "//span[text()='Profile']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/profile"))
        assert "/profile" in driver.current_url
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-btn")))
        edit_button = driver.find_element(By.ID, "profile-btn")
        assert edit_button.text == "Edit profile"
        edit_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/profile/edit"))
        assert "/profile/edit" in driver.current_url
    
    def test_EDITPROF_edit_about(self, driver, setup_user):
        # Test if the user can edit their about section

        user = setup_user
        self.sign_in(driver, user)
        about_field = driver.find_element(By.NAME, "about")
        about_field.clear()
        about_field.send_keys("New about")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/profile"))
        assert "/profile" in driver.current_url
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-about")))
        about_text = driver.find_element(By.ID, "profile-about")
        assert about_text.text == "New about"
    
    def test_EDITPROF_edit_first_name(self, driver, setup_user):
        # Test if the user can edit their first name

        user = setup_user
        self.sign_in(driver, user)
        first_name_field = driver.find_element(By.NAME, "firstName")
        first_name_field.clear()
        first_name_field.send_keys("Firstname")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/profile"))
        assert "/profile" in driver.current_url
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-name")))
        first_name_text = driver.find_element(By.ID, "profile-name")
        assert first_name_text.text == f"Firstname {user['lastName']}"
    
    def test_EDITPROF_edit_last_name(self, driver, setup_user):
        # Test if the user can edit their last name

        user = setup_user
        self.sign_in(driver, user)
        last_name_field = driver.find_element(By.NAME, "lastName")
        last_name_field.clear()
        last_name_field.send_keys("Lastname")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/profile"))
        assert "/profile" in driver.current_url
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-name")))
        last_name_text = driver.find_element(By.ID, "profile-name")
        assert last_name_text.text == f"{user['firstName']} Lastname"
    
    def test_EDITPROF_edit_date_of_birth(self, driver, setup_user):
        # Test if the user can edit their date of birth

        user = setup_user
        self.sign_in(driver, user)
        date_of_birth_field = driver.find_element(By.NAME, "dateOfBirth")
        date_of_birth_field.clear()
        date_of_birth_field.send_keys("1990-01-01")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/profile"))
        assert "/profile" in driver.current_url
        time.sleep(2)
        url = "http://localhost:8080/api/v1/login"
        user_data = {
            "email": user['email'],
            "password": user['password']
        }
        response = requests.post(url, json=user_data)
        if response.status_code != 200:
            raise Exception("Failed to sign in", response.content)
        assert response.json()['dateOfBirth'] == "1990-01-01"
        
    
    # def test_EDITPROF_edit_profile_picture(self, driver, setup_user):
    #     # Test if the user can edit their profile picture
    #     pass