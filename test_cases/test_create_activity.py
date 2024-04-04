# test_create_activity.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import os


class TestCreateActivity:
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

    def remove_post(self, private=False):
        conn = psycopg2.connect(
            dbname="connect",
            user="postgres",
            password="connect",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM post WHERE posttext='Morning Yoga Session'")
        activity_count = cur.fetchone()[0]
        assert activity_count == 1
        if private:
            # assert that the post is private in the 'ispublic' column from the post table
            cur.execute("SELECT ispublic FROM post WHERE posttext='Morning Yoga Session'")
            is_public = cur.fetchone()[0]
            assert not is_public

        cur.execute("SELECT postid FROM post WHERE posttext='Morning Yoga Session'")
        post_id = cur.fetchone()[0]
        cur.execute("DELETE FROM post WHERE postid = %s;", (post_id,))
        cur.execute("DELETE FROM activities WHERE postid = %s;", (post_id,))
        conn.commit()
        conn.close()
        return post_id

    def remove_attachment(self, post_id):
        conn = psycopg2.connect(
            dbname="connect",
            user="postgres",
            password="connect",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM attachments WHERE postid=%s", (post_id,))
        attachment_count = cur.fetchone()[0]
        assert attachment_count == 1
        cur.execute("DELETE FROM attachments WHERE postid=%s", (post_id,))
        conn.commit()
        conn.close()

    def test_CREATE_ACTIVITY_no_attachement(self, setup_user, driver):
        # Test if the user can create an activity without an attachment
        user = setup_user
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/create-activity")
        category_select = driver.find_element(By.ID, "category")
        category_select.click()
        fitness_option = driver.find_element(By.XPATH, "//div[text()='Fitness']")
        fitness_option.click()
        start_date_field = driver.find_element(By.ID, "startDate")
        start_date_field.send_keys("2023-01-01")
        end_date_field = driver.find_element(By.ID, "endDate")
        end_date_field.send_keys("2023-01-01")
        post_text_field = driver.find_element(By.ID, "postText")
        post_text_field.send_keys("Morning Yoga Session")
        visibility_public = driver.find_element(By.ID, "public")
        driver.execute_script("arguments[0].click();", visibility_public)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/create-activity/success"))
        assert "/create-activity/success" in driver.current_url
        self.remove_post()
        
    def test_CREATE_ACTIVITY_with_attachment(self, setup_user,driver):
        # Test if the user can create an activity with an attachment
        user = setup_user
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/create-activity")
        file_input_ref = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'resources', 'meditate.jpg')
        file_input_ref.send_keys(file_path)
        category_select = driver.find_element(By.ID, "category")
        category_select.click()
        fitness_option = driver.find_element(By.XPATH, "//div[text()='Fitness']")
        fitness_option.click()
        start_date_field = driver.find_element(By.ID, "startDate")
        start_date_field.send_keys("2023-01-01")
        end_date_field = driver.find_element(By.ID, "endDate")
        end_date_field.send_keys("2023-01-01")

        post_text_field = driver.find_element(By.ID, "postText")
        post_text_field.send_keys("Morning Yoga Session")
        visibility_public = driver.find_element(By.ID, "public")
        driver.execute_script("arguments[0].click();", visibility_public)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/create-activity/success"))
        assert "/create-activity/success" in driver.current_url
        post_id = self.remove_post()
        self.remove_attachment(post_id)
 
    def test_CREATE_ACTIVITY_without_category(self, setup_user, driver):
        # Test if the user can create an activity without a category
        user = setup_user
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/create-activity")
        
        start_date_field = driver.find_element(By.ID, "startDate")
        start_date_field.send_keys("2023-01-01")
        end_date_field = driver.find_element(By.ID, "endDate")
        end_date_field.send_keys("2023-01-01")

        post_text_field = driver.find_element(By.ID, "postText")
        post_text_field.send_keys("Morning Yoga Session")
        visibility_public = driver.find_element(By.ID, "public")
        driver.execute_script("arguments[0].click();", visibility_public)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='category_error']")))
        error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='category_error']")
        assert error_message.text == "Required"
    
    def test_CREATE_ACTIVITY_without_start_date(self, setup_user, driver):
        # Test if the user can create an activity without a start date
        user = setup_user
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/create-activity")
        category_select = driver.find_element(By.ID, "category")
        category_select.click()
        fitness_option = driver.find_element(By.XPATH, "//div[text()='Fitness']")
        fitness_option.click()
        end_date_field = driver.find_element(By.ID, "endDate")
        end_date_field.send_keys("2023-01-01")
        post_text_field = driver.find_element(By.ID, "postText")
        post_text_field.send_keys("Morning Yoga Session")
        visibility_public = driver.find_element(By.ID, "public")
        driver.execute_script("arguments[0].click();", visibility_public)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='startDate_error']")))
        error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='startDate_error']")
        assert error_message.text == "Required"
    
    def test_CREATE_ACTIVITY_without_end_date(self, setup_user, driver):
        # Test if the user can create an activity without an end date
        user = setup_user
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/create-activity")
        category_select = driver.find_element(By.ID, "category")
        category_select.click()
        fitness_option = driver.find_element(By.XPATH, "//div[text()='Fitness']")
        fitness_option.click()
        start_date_field = driver.find_element(By.ID, "startDate")
        start_date_field.send_keys("2023-01-01")
        post_text_field = driver.find_element(By.ID, "postText")
        post_text_field.send_keys("Morning Yoga Session")
        visibility_public = driver.find_element(By.ID, "public")
        driver.execute_script("arguments[0].click();", visibility_public)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='endDate_error']")))
        error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='endDate_error']")
        assert error_message.text == "Required"

    def test_CREATE_ACTIVITY_without_post_text(self, setup_user, driver):
        # Test if the user can create an activity without a post text
        user = setup_user
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/create-activity")
        category_select = driver.find_element(By.ID, "category")
        category_select.click()
        fitness_option = driver.find_element(By.XPATH, "//div[text()='Fitness']")
        fitness_option.click()
        start_date_field = driver.find_element(By.ID, "startDate")
        start_date_field.send_keys("2023-01-01")
        end_date_field = driver.find_element(By.ID, "endDate")
        end_date_field.send_keys("2023-01-01")
        visibility_public = driver.find_element(By.ID, "public")
        driver.execute_script("arguments[0].click();", visibility_public)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='postText_error']")))
        error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='postText_error']")
        assert error_message.text == "Required"
    
    def test_CREATE_ACTIVITY_private(self, setup_user, driver):
        user = setup_user
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/create-activity")
        category_select = driver.find_element(By.ID, "category")
        category_select.click()
        fitness_option = driver.find_element(By.XPATH, "//div[text()='Fitness']")
        fitness_option.click()
        start_date_field = driver.find_element(By.ID, "startDate")
        start_date_field.send_keys("2023-01-01")
        end_date_field = driver.find_element(By.ID, "endDate")
        end_date_field.send_keys("2023-01-01")
        post_text_field = driver.find_element(By.ID, "postText")
        post_text_field.send_keys("Morning Yoga Session")
        visibility_public = driver.find_element(By.ID, "private")
        driver.execute_script("arguments[0].click();", visibility_public)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/create-activity/success"))
        assert "/create-activity/success" in driver.current_url
        self.remove_post(private=True)

    # def test_CREATE_ACTIVITY_recurrent(self, setup_user, driver):
    #     pass