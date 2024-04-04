# test_e2e.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import psycopg2


class TestE2E:
    def test_E2E_account_creation_and_initial_login(self, driver):
        # Sign up
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
        response_email = requests.get('http://localhost:1080/email')
        if response_email.status_code != 200:
            raise Exception("Failed to fetch emails")
        emails = response_email.json()
        confirmation_email = emails[-1]
        soup = BeautifulSoup(confirmation_email['html'], 'html.parser')
        confirmation_link = soup.find('a')['href']
        response_confirmation = requests.get(confirmation_link)
        if response_confirmation.status_code != 200:
            raise Exception("Failed to confirm email")
        
        # Check user in DB
        conn = psycopg2.connect(
            dbname="connect",
            user="postgres",
            password="connect",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE email = 'newuser@example.com';")
        user_count = cur.fetchone()[0]
        assert user_count == 1, "User was not created in the database"
        cur.close()
        conn.close()
        try:
            # Log in
            driver.get("http://localhost:3000/")
            email_field = driver.find_element(By.ID, "email")
            email_field.send_keys('newuser@example.com')
            password_field = driver.find_element(By.ID, "password")
            password_field.send_keys('P@ssw0rd1!')
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            WebDriverWait(driver, 10).until(EC.url_contains("/home"))
            assert "/home" in driver.current_url
        except:
            # Tear down
            conn = psycopg2.connect(
            dbname="connect",
            user="postgres",
            password="connect",
            host="localhost",
            port="5432"
            )
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE email = 'newuser@example.com';")
            user_id = cur.fetchone()[0]
            cur.execute("DELETE FROM token WHERE user_id = %s;", (user_id,))
            cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            conn.commit()
            cur.close()
            conn.close()
            raise Exception("Failed to log in")
        finally:
            # Tear down
            conn = psycopg2.connect(
            dbname="connect",
            user="postgres",
            password="connect",
            host="localhost",
            port="5432"
            )
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE email = 'newuser@example.com';")
            user_id = cur.fetchone()[0]
            cur.execute("DELETE FROM token WHERE user_id = %s;", (user_id,))
            cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            conn.commit()
            cur.close()
            conn.close()

    def test_E2E_password_reset_and_access_restriction(self,setup_user, driver):
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
        soup = BeautifulSoup(confirmation_email['html'], 'html.parser')
        link = soup.find('a')['href']
        driver.get(link)
        driver.find_element(By.ID, "password").send_keys("NEWP@ssw0rd1!")
        driver.find_element(By.ID, "confirmPassword").send_keys("NEWP@ssw0rd1!")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/reset-password-success"))
        assert "/reset-password-success" in driver.current_url
        driver.get("http://localhost:3000/")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(user['email'])
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(user['password'])
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='error_message']")))
        error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='error_message']")
        assert error_message.text == "Invalid username or password."
        password_field.clear()
        password_field.send_keys('NEWP@ssw0rd1!')
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
        assert "/home" in driver.current_url