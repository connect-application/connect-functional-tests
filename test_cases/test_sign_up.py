# test_sign_up.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup

class TestSignUp:
    def test_SIGNUP_valid_input_submission(self, driver):
        driver.get("http://localhost:3000/signup")
        driver.find_element(By.ID, "firstName").send_keys("New")
        driver.find_element(By.ID, "lastName").send_keys("User")
        driver.find_element(By.ID, "username").send_keys("newuser")
        driver.find_element(By.ID, "email").send_keys("newuser@example.com")
        driver.find_element(By.ID, "password").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "confirmPassword").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "dateOfBirth").send_keys("2000-01-01")
        terms_button = driver.find_element(By.ID, "termsCheck")
        driver.execute_script("arguments[0].click();", terms_button)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/signup-success"))
        assert "/signup-success" in driver.current_url
        response = requests.get('http://localhost:1080/email')
        if response.status_code != 200:
            raise Exception("Failed to fetch emails")
        emails = response.json()
        confirmation_email = emails[-1]
        assert 'newuser@example.com' in confirmation_email['to'][0]['address']
        soup = BeautifulSoup(confirmation_email['html'], 'html.parser')
        p_tag = soup.find(lambda tag : tag.name == 'p' and 'activate your account' in tag.text)
        assert p_tag is not None, "No p tag found with 'activate your account'"

    def test_SIGNUP_invalid_email_format(self, driver):
        driver.get("http://localhost:3000/signup")
        driver.find_element(By.ID, "firstName").send_keys("Test")
        driver.find_element(By.ID, "lastName").send_keys("User")
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "email").send_keys("invalid_email_format")
        driver.find_element(By.ID, "password").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "confirmPassword").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "dateOfBirth").send_keys("2000-01-01")
        terms_button = driver.find_element(By.ID, "termsCheck")
        driver.execute_script("arguments[0].click();", terms_button)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='email_error']")))
        email_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='email_error']")
        assert email_error_message.text == "* Invalid email address"

    def test_SIGNUP_password_confirmation_mismatch(self, driver):
        driver.get("http://localhost:3000/signup")
        driver.find_element(By.ID, "firstName").send_keys("Test")
        driver.find_element(By.ID, "lastName").send_keys("User")
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "email").send_keys("testuser@example.com")
        driver.find_element(By.ID, "password").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "confirmPassword").send_keys("Password2!")
        driver.find_element(By.ID, "dateOfBirth").send_keys("2000-01-01")
        terms_button = driver.find_element(By.ID, "termsCheck")
        driver.execute_script("arguments[0].click();", terms_button)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='confirmPassword_error']")))
        password_mismatch_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='confirmPassword_error']")
        assert password_mismatch_error_message.text == "* The passwords do not match"

    def test_SIGNUP_duplicate_email_address(self, setup_user, driver):
        user = setup_user
        driver.get("http://localhost:3000/signup")
        driver.find_element(By.ID, "firstName").send_keys("Test")
        driver.find_element(By.ID, "lastName").send_keys("User")
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "email").send_keys(user['email'])
        driver.find_element(By.ID, "password").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "confirmPassword").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "dateOfBirth").send_keys("2000-01-01")
        terms_button = driver.find_element(By.ID, "termsCheck")
        driver.execute_script("arguments[0].click();", terms_button)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message[errorMessageId='error_message']")))
        email_duplicate_error_message = driver.find_element(By.CSS_SELECTOR, ".error-message[errorMessageId='error_message']")
        assert email_duplicate_error_message.text == "Email or username is already registered."

    def test_SIGNUP_not_agreeing_terms_privacy_policy(self, driver):
        driver.get("http://localhost:3000/signup")
        driver.find_element(By.ID, "firstName").send_keys("Test")
        driver.find_element(By.ID, "lastName").send_keys("User")
        driver.find_element(By.ID, "username").send_keys("testuser")
        driver.find_element(By.ID, "email").send_keys("newuser@example.com")
        driver.find_element(By.ID, "password").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "confirmPassword").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "dateOfBirth").send_keys("2000-01-01")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message[errorMessageId='checkbox_error']")))
        terms_error_message = driver.find_element(By.CSS_SELECTOR, ".error-message[errorMessageId='checkbox_error']")
        assert terms_error_message.text == "* Must accept the terms and privacy policy"

    def test_SIGNUP_to_sign_in(self, driver):
        driver.get("http://localhost:3000/signup")
        signin_link = driver.find_element(By.XPATH, "//p[contains(@class, 'sign-in-link')]/a[contains(text(), 'Sign In')]")
        driver.execute_script("arguments[0].click();", signin_link)

        WebDriverWait(driver, 10).until(EC.title_is("Sign In"))
        assert "Sign In" in driver.title

    def test_SIGNUP_username_length_validation(self, driver):
        driver.get("http://localhost:3000/signup")
        driver.find_element(By.ID, "firstName").send_keys("New")
        driver.find_element(By.ID, "lastName").send_keys("User")
        # Entering a username longer than 12 characters
        driver.find_element(By.ID, "username").send_keys("thisiswaytoolongusername")
        driver.find_element(By.ID, "email").send_keys("user@example.com")
        driver.find_element(By.ID, "password").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "confirmPassword").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "dateOfBirth").send_keys("2000-01-01")
        terms_button = driver.find_element(By.ID, "termsCheck")
        driver.execute_script("arguments[0].click();", terms_button)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        # Expecting an error message about the username length
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[errorMessageId='username_error']")))
        username_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='username_error']")
        assert "* Username cannot exceed 12 characters" in username_error_message.text


    def test_SIGNUP_length_password_requirement(self, driver):
        driver.get("http://localhost:3000/signup")
        driver.find_element(By.ID, "firstName").send_keys("Secure")
        driver.find_element(By.ID, "lastName").send_keys("PasswordTest")
        driver.find_element(By.ID, "username").send_keys("secureuser")
        driver.find_element(By.ID, "email").send_keys("secureuser@example.com")
        # Entering a password that does not meet security requirements
        driver.find_element(By.ID, "password").send_keys("123")
        driver.find_element(By.ID, "confirmPassword").send_keys("123")
        driver.find_element(By.ID, "dateOfBirth").send_keys("1990-01-01")
        terms_button = driver.find_element(By.ID, "termsCheck")
        driver.execute_script("arguments[0].click();", terms_button)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        # Expecting an error message about the password security
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[errorMessageId='password_error']")))
        password_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='password_error']")
        assert "* Password must have at least 6 characters" in password_error_message.text
    
    def test_SIGNUP_secure_password_requirement(self, driver):
        driver.get("http://localhost:3000/signup")
        driver.find_element(By.ID, "firstName").send_keys("Secure")
        driver.find_element(By.ID, "lastName").send_keys("PasswordTest")
        driver.find_element(By.ID, "username").send_keys("secureuser")
        driver.find_element(By.ID, "email").send_keys("secureuser@example.com")
        # Entering a password that does not meet security requirements
        driver.find_element(By.ID, "password").send_keys("p@ssword1234")
        driver.find_element(By.ID, "confirmPassword").send_keys("p@ssword1234")
        driver.find_element(By.ID, "dateOfBirth").send_keys("1990-01-01")
        terms_button = driver.find_element(By.ID, "termsCheck")
        driver.execute_script("arguments[0].click();", terms_button)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        # Expecting an error message about the password security
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[errorMessageId='password_error']")))
        password_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='password_error']")
        assert "* Password not secure enough" in password_error_message.text

    def test_SIGNUP_date_of_birth_requirement(self, driver):
        driver.get("http://localhost:3000/signup")
        driver.find_element(By.ID, "firstName").send_keys("DateOfBirth")
        driver.find_element(By.ID, "lastName").send_keys("Test")
        driver.find_element(By.ID, "username").send_keys("dobuser")
        driver.find_element(By.ID, "email").send_keys("dobuser@example.com")
        driver.find_element(By.ID, "password").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "confirmPassword").send_keys("P@ssw0rd1!")
        # Not entering a date of birth
        terms_button = driver.find_element(By.ID, "termsCheck")
        driver.execute_script("arguments[0].click();", terms_button)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        # Expecting an error message for missing date of birth
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[errorMessageId='dateOfBirth_error']")))
        dob_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='dateOfBirth_error']")
        assert "* Date of birth is required" in dob_error_message.text


    def test_SIGNUP_email_format_validation_client_side(self, driver):
        driver.get("http://localhost:3000/signup")
        driver.find_element(By.ID, "firstName").send_keys("Email")
        driver.find_element(By.ID, "lastName").send_keys("Format")
        driver.find_element(By.ID, "username").send_keys("emailformatuser")
        driver.find_element(By.ID, "email").send_keys("notanemail")
        driver.find_element(By.ID, "password").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "confirmPassword").send_keys("P@ssw0rd1!")
        driver.find_element(By.ID, "dateOfBirth").send_keys("2000-01-01")
        terms_button = driver.find_element(By.ID, "termsCheck")
        driver.execute_script("arguments[0].click();", terms_button)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[errorMessageId='email_error']")))
        email_error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='email_error']")
        assert "* Invalid email address" in email_error_message.text


    # def test_SIGNUP_terms_privacy_policy_link_functionality(self, driver):
    #     driver.get("http://localhost:3000/signup")
    #     # Note: Adjust the XPath to match the actual structure or add an ID to the terms link for easier selection
    #     terms_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Terms and Privacy Policy')]")
    #     terms_link.click()
        
    #     # Assuming a modal pops up, wait for the modal to be visible
    #     # If it redirects to a new page, adjust the wait condition accordingly
    #     WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.terms-modal")))
        
    #     # Asserting that the modal or the terms page contains specific text
    #     # Adjust the selector and text according to your application
    #     terms_content = driver.find_element(By.CSS_SELECTOR, "div.terms-modal p")
    #     assert "Terms and Conditions" in terms_content.text
