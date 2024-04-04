# test_sidebar.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSidebar:
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

    def test_SIDEBAR_search_navigation(self, setup_user, driver):
        user = setup_user
        self.sign_in(driver, user)
        search_button = driver.find_element(By.XPATH, "//span[text()='search']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/search"))
        assert "/search" in driver.current_url
    
    def test_SIDEBAR_home_navigation(self, setup_user, driver):
        user = setup_user
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/create-activity")
        search_button = driver.find_element(By.XPATH, "//span[text()='Home']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
        assert "/home" in driver.current_url
    
    def test_SIDEBAR_chat_navigation(self, setup_user, driver):
        user = setup_user
        self.sign_in(driver, user)
        search_button = driver.find_element(By.XPATH, "//span[text()='Chat']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/chat"))
        assert "/chat" in driver.current_url
 
    def test_SIDEBAR_notifications_navigation(self, setup_user, driver):
        user = setup_user
        self.sign_in(driver, user)
        search_button = driver.find_element(By.XPATH, "//span[text()='Notifications']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/notifications"))
        assert "/notifications" in driver.current_url
                
    def test_SIDEBAR_profile_navigation(self, setup_user, driver):
        user = setup_user
        self.sign_in(driver, user)
        search_button = driver.find_element(By.XPATH, "//span[text()='Profile']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/profile"))
        assert "/profile" in driver.current_url
                
    def test_SIDEBAR_groups_navigation(self, setup_user, driver):
        user = setup_user
        self.sign_in(driver, user)
        search_button = driver.find_element(By.XPATH, "//span[text()='Groups']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/groups"))
        assert "/groups" in driver.current_url
        
    def test_SIDEBAR_logout_navigation(self, setup_user, driver):
        user = setup_user
        self.sign_in(driver, user)
        search_button = driver.find_element(By.XPATH, "//span[text()='Logout']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.title_is("Sign In"))
        assert "Sign In" in driver.title
    
    def test_SIDEBAR_create_post_navigation(self, setup_user, driver):
        user = setup_user
        self.sign_in(driver, user)
        search_button = driver.find_element(By.XPATH, "//span[text()='create']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/create-post"))
        search_button = driver.find_element(By.XPATH, "//span[text()='create']")
        search_button.click()
        search_button = driver.find_element(By.XPATH, "//span[text()='Post']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/create-post"))
        assert "/create-post" in driver.current_url

    def test_SIDEBAR_create_activity_navigation(self, setup_user, driver):
        user = setup_user
        self.sign_in(driver, user)
        search_button = driver.find_element(By.XPATH, "//span[text()='create']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/create-post"))
        search_button = driver.find_element(By.XPATH, "//span[text()='create']")
        search_button.click()
        search_button = driver.find_element(By.XPATH, "//span[text()='Activity']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/create-activity"))
        assert "/create-activity" in driver.current_url