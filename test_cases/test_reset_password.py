from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup

class TestRecoverPassword:
    def test_RESET_PASSWORD_successful_user_authentication(self, reset_password_setup, driver):
        # Test if the user can reset their password

        user, link = reset_password_setup
        driver.get(link)
        driver.find_element(By.ID, "password").send_keys("NEWP@ssw0rd1!")
        driver.find_element(By.ID, "confirmPassword").send_keys("NEWP@ssw0rd1!")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/reset-password-success"))
        assert "/reset-password-success" in driver.current_url

    def test_RESET_PASSWORD_mismatched_passwords(self, reset_password_setup, driver):
        # Test that the user cannot reset their password if the passwords do not match
        
        user, link = reset_password_setup
        driver.get(link)
        driver.find_element(By.ID, "password").send_keys("NEWP@ssw0rd1!")
        driver.find_element(By.ID, "confirmPassword").send_keys("MismatchP@ssw0rd")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='confirmPassword_error']")))
        mismatch_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='confirmPassword_error']").text
        assert "* The passwords do not match" in mismatch_error_message

    def test_RESET_PASSWORD_no_input(self, reset_password_setup, driver):
        # Test that the user cannot reset their password if no input is provided
        
        user, link = reset_password_setup
        driver.get(link)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='password_error']")))
        password_required_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='password_error']").text
        assert "* Password is required" in password_required_message

    def test_RESET_PASSWORD_password_too_long(self, reset_password_setup, driver):
        # Test that the user cannot reset their password if the password is too long
        
        user, link = reset_password_setup
        driver.get(link)
        long_password = "P@ssw0rd1!" * 5  # Assuming a max length is set
        driver.find_element(By.ID, "password").send_keys(long_password)
        driver.find_element(By.ID, "confirmPassword").send_keys(long_password)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='password_error']")))
        length_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='password_error']").text
        assert "* Password cannot exceed 20 characters" in length_error_message

    def test_RESET_PASSWORD_password_not_secure_enough(self, reset_password_setup, driver):
        # Test that the user cannot reset their password if the password is not secure enough
        
        user, link = reset_password_setup
        driver.get(link)
        insecure_password = "password"  # Example of a weak password
        driver.find_element(By.ID, "password").send_keys(insecure_password)
        driver.find_element(By.ID, "confirmPassword").send_keys(insecure_password)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='password_error']")))
        security_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='password_error']").text
        assert "* Password not secure enough" in security_error_message