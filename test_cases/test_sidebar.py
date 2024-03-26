# test_sidebar.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSidebar:
    def test_SIDEBAR_user_profile_navigation(self, setup_user, driver):
        user = setup_user
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
        search_button = driver.find_element(By.XPATH, "//span[text()='search']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/search"))
        assert "/search" in driver.current_url
    
    # Same test as above, but for Chat
    def test_SIDEBAR_chat_navigation(self, setup_user, driver):
        user = setup_user
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
        search_button = driver.find_element(By.XPATH, "//span[text()='Chat']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/chat"))
        assert "/chat" in driver.current_url

        
    # Same test as above, but for Notifications
        
    def test_SIDEBAR_notifications_navigation(self, setup_user, driver):
        user = setup_user
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
        search_button = driver.find_element(By.XPATH, "//span[text()='Notifications']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/notifications"))
        assert "/notifications" in driver.current_url
        
    # Same test as above, but for Profile
        
    def test_SIDEBAR_profile_navigation(self, setup_user, driver):
        user = setup_user
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
        
    # Same test as above, but for Settings
        
    def test_SIDEBAR_settings_navigation(self, setup_user, driver):
        user = setup_user
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
        search_button = driver.find_element(By.XPATH, "//span[text()='Settings']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/settings"))
        assert "/settings" in driver.current_url
        
    # Same test as above, but for Logout
    def test_SIDEBAR_logout_navigation(self, setup_user, driver):
        user = setup_user
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
        search_button = driver.find_element(By.XPATH, "//span[text()='Logout']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.title_is("Sign In"))
        assert "Sign In" in driver.title
    
    def test_SIDEBAR_create_post_navigation(self, setup_user, driver):
        user = setup_user
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
        search_button = driver.find_element(By.XPATH, "//span[text()='create']")
        search_button.click()
        search_button = driver.find_element(By.XPATH, "//span[text()='Post']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/create-post"))
        assert "/create-post" in driver.current_url

    def test_SIDEBAR_create_activity_navigation(self, setup_user, driver):
        user = setup_user
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
        search_button = driver.find_element(By.XPATH, "//span[text()='create']")
        search_button.click()
        search_button = driver.find_element(By.XPATH, "//span[text()='Activity']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/create-activity"))
        assert "/create-activity" in driver.current_url