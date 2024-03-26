# test_recover_password.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup


class TestRecoverPassword:
    def test_RECOVER_PASSWORD_successful_user_authentication(self, setup_user, driver):
        user = setup_user
        driver.get("http://localhost:3000/recover-password")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(user['email'])
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/recover-password-success"))
        assert "/recover-password-success" in driver.current_url
        response = requests.get('http://localhost:1080/email')
        if response.status_code != 200:
            raise Exception("Failed to fetch emails")
        emails = response.json()
        confirmation_email = emails[-1]
        assert user['email'] in confirmation_email['to'][0]['address']
        soup = BeautifulSoup(confirmation_email['html'], 'html.parser')
        p_tag = soup.find(lambda tag : tag.name == 'p' and 'reset your password' in tag.text)
        assert p_tag is not None, "No p tag found with 'reset your password'"

    def test_RECOVER_PASSWORD_email_not_registered(self, driver):
        driver.get("http://localhost:3000/recover-password")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys("unregistered@example.com")  # Assuming this email is not registered
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[errorMessageId='error_message']")))
        error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='error_message']").text
        assert "Email is not registered." == error_message

    def test_RECOVER_PASSWORD_invalid_email_format(self, driver):
        driver.get("http://localhost:3000/recover-password")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys("invalidemail")  # Invalid email format
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[errorMessageId='email_error']")))
        email_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='email_error']").text
        assert "* Invalid email address" == email_error_message

    def test_RECOVER_PASSWORD_email_field_required_validation(self, driver):
        driver.get("http://localhost:3000/recover-password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[errorMessageId='email_error']")))
        email_required_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='email_error']").text

        assert "* Email is required" == email_required_message
