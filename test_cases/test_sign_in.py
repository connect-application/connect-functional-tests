# test_sign_in.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSignIn:
    def test_SIGNIN_successful_user_authentication(self, setup_user, driver):
        user = setup_user
        driver.get("http://localhost:3000/")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(user['email'])
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(user['password'])
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
        assert "/home" in driver.current_url
    
    def test_SIGNIN_password_mismatch_error(self, setup_user, driver):
        user = setup_user
        driver.get("http://localhost:3000/")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(user['email'])
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("invalid_password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='error_message']")))
        error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='error_message']")
        assert error_message.text == "Invalid username or password."

    def test_SIGNIN_required_fields_validation(self, driver):
        driver.get("http://localhost:3000/")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='email_error']")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='password_error']")))
        email_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='email_error']")
        password_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='password_error']")
        assert email_error_message.text == "* Email is required"
        assert password_error_message.text == "* Password is required"

    def test_SIGNIN_invalid_email_format(self, setup_user, driver):
        user = setup_user
        driver.get("http://localhost:3000/")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys("test@")
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(user['password'])
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='email_error']")))
        email_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='email_error']")
        assert email_error_message.text == "* Invalid email address"

    def test_SIGNIN_forgot_password_navigation(self, driver):
        driver.get("http://localhost:3000/")
        forgot_password_link = driver.find_element(By.LINK_TEXT, "Forgot Password?")
        forgot_password_link.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/recover-password"))
        assert "/recover-password" in driver.current_url

    def test_SIGNIN_new_account_navigation(self, driver):
        driver.get("http://localhost:3000/")
        create_account_button = driver.find_element(By.LINK_TEXT, "Create new account")
        create_account_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/signup"))
        assert "/signup" in driver.current_url
    
    def test_SIGNIN_incorrect_email_handling(self, driver):
        driver.get("http://localhost:3000/")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys("unregistered@example.com")
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("validpassword")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='error_message']")))
        error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='error_message']")
        assert error_message.text == "Invalid username or password."
    
    def test_password_visibility_toggle(self, driver):
        driver.get("http://localhost:3000/")
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("test_password")
        show_button = driver.find_element(By.ID, "showPassword")
        show_button.click()
        assert password_field.get_attribute("type") == "text"
        assert show_button.text == "Hide"
        show_button.click()
        assert password_field.get_attribute("type") == "password"