# test_create_activity.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import os


class TestCreateActivity:
    def test_CREATE_ACTIVITY_create_activity_no_attachement(self, setup_user, remove_activity, driver):
        user = setup_user
        # Sign in
        driver.get("http://localhost:3000/")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(user['email'])
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(user['password'])
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
        assert "/home" in driver.current_url
        driver.get("http://localhost:3000/create-activity")
        # Create activity
        category_select = driver.find_element(By.ID, "category")
        category_select.click()
        fitness_option = driver.find_element(By.XPATH, "//div[text()='Fitness']")
        fitness_option.click()
        start_date_field = driver.find_element(By.ID, "startDate")
        start_date_field.send_keys("2023-01-01")
        end_date_field = driver.find_element(By.ID, "endDate")
        end_date_field.send_keys("2023-01-02")
        start_time_field = driver.find_element(By.ID, "startTime")
        start_time_field.send_keys("09:00")
        end_time_field = driver.find_element(By.ID, "endTime")
        end_time_field.send_keys("17:00")
        is_recurring_checkbox = driver.find_element(By.ID, "isRecurring")
        is_recurring_checkbox.click()
        post_text_field = driver.find_element(By.ID, "postText")
        post_text_field.send_keys("Morning Yoga Session")
        visibility_public = driver.find_element(By.ID, "public")
        visibility_public.click()
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/create-activity/success"))
        assert "/create-activity/success" in driver.current_url
        
        # Check user in DB
        with remove_activity.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM post WHERE posttext = 'Morning Yoga Session';")
            activity_count = cur.fetchone()[0]
            assert activity_count == 1, "Activity was not created in the database"
            
    def test_CREATE_ACTIVITY_create_activity_with_attachment(self, setup_user, remove_activity, driver):
        user = setup_user
        # Sign in
        driver.get("http://localhost:3000/")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(user['email'])
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(user['password'])
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
        assert "/home" in driver.current_url
        driver.get("http://localhost:3000/create-activity")
        # Create activity
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
        end_date_field.send_keys("2023-01-02")
        start_time_field = driver.find_element(By.ID, "startTime")
        start_time_field.send_keys("09:00")
        end_time_field = driver.find_element(By.ID, "endTime")
        end_time_field.send_keys("17:00")
        is_recurring_checkbox = driver.find_element(By.ID, "isRecurring")
        is_recurring_checkbox.click()
        post_text_field = driver.find_element(By.ID, "postText")
        post_text_field.send_keys("Morning Yoga Session")
        visibility_public = driver.find_element(By.ID, "public")
        visibility_public.click()
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/create-activity/success"))
        assert "/create-activity/success" in driver.current_url
         # Check user in DB
        conn = remove_activity
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM post WHERE posttext = 'Morning Yoga Session';")
            activity_count = cur.fetchone()[0]
            cur.execute("SELECT postid FROM post WHERE posttext = 'Morning Yoga Session';")
            post_id = cur.fetchone()[0]
            # Check in the attachment table if element with postid exists and assert
            cur.execute(f"SELECT COUNT(*) FROM attachments WHERE postid = {post_id};")
            attachment_count = cur.fetchone()[0]
            assert activity_count == 1, "Activity was not created in the database"
 

    def test_CREATE_ACTIVITY_submit_without_category(self, setup_user, driver):
        user = setup_user
        # Sign in
        driver.get("http://localhost:3000/")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(user['email'])
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(user['password'])
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
        assert "/home" in driver.current_url
        driver.get("http://localhost:3000/create-activity")
        
        # Create activity
        start_date_field = driver.find_element(By.ID, "startDate")
        start_date_field.send_keys("2023-01-01")
        end_date_field = driver.find_element(By.ID, "endDate")
        end_date_field.send_keys("2023-01-02")
        start_time_field = driver.find_element(By.ID, "startTime")
        start_time_field.send_keys("09:00")
        end_time_field = driver.find_element(By.ID, "endTime")
        end_time_field.send_keys("17:00")
        is_recurring_checkbox = driver.find_element(By.ID, "isRecurring")
        is_recurring_checkbox.click()
        post_text_field = driver.find_element(By.ID, "postText")
        post_text_field.send_keys("Morning Yoga Session")
        visibility_public = driver.find_element(By.ID, "public")
        visibility_public.click()
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='category_error']")))
        error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='category_error']")
        assert error_message.text == "Required"
    
    def test_CREATE_ACTIVITY_submit_without_start_date(self, setup_user, driver):
        user = setup_user
        # Sign in
        driver.get("http://localhost:3000/")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(user['email'])
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(user['password'])
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
        assert "/home" in driver.current_url
        driver.get("http://localhost:3000/create-activity")
        # Create activity
        category_select = driver.find_element(By.ID, "category")
        category_select.click()
        fitness_option = driver.find_element(By.XPATH, "//div[text()='Fitness']")
        fitness_option.click()
        # start_date_field = driver.find_element(By.ID, "startDate")
        # start_date_field.send_keys("2023-01-01")
        end_date_field = driver.find_element(By.ID, "endDate")
        end_date_field.send_keys("2023-01-02")
        is_recurring_checkbox = driver.find_element(By.ID, "isRecurring")
        is_recurring_checkbox.click()
        post_text_field = driver.find_element(By.ID, "postText")
        post_text_field.send_keys("Morning Yoga Session")
        visibility_public = driver.find_element(By.ID, "public")
        visibility_public.click()
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='startDate_error']")))
        error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='startDate_error']")
        assert error_message.text == "Required"
    
    def test_CREATE_ACTIVITY_submit_without_end_date(self, setup_user, driver):
        user = setup_user
        # Sign in
        driver.get("http://localhost:3000/")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(user['email'])
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(user['password'])
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
        assert "/home" in driver.current_url
        driver.get("http://localhost:3000/create-activity")
        # Create activity
        category_select = driver.find_element(By.ID, "category")
        category_select.click()
        fitness_option = driver.find_element(By.XPATH, "//div[text()='Fitness']")
        fitness_option.click()
        start_date_field = driver.find_element(By.ID, "startDate")
        start_date_field.send_keys("2023-01-01")
        # end_date_field = driver.find_element(By.ID, "endDate")
        # end_date_field.send_keys("2023-01-02")
        is_recurring_checkbox = driver.find_element(By.ID, "isRecurring")
        is_recurring_checkbox.click()
        post_text_field = driver.find_element(By.ID, "postText")
        post_text_field.send_keys("Morning Yoga Session")
        visibility_public = driver.find_element(By.ID, "public")
        visibility_public.click()
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='endDate_error']")))
        error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='endDate_error']")
        assert error_message.text == "Required"

    def test_CREATE_ACTIVITY_submit_without_post_text(self, setup_user, driver):
        user = setup_user
        # Sign in
        driver.get("http://localhost:3000/")
        email_field = driver.find_element(By.ID, "email")
        email_field.send_keys(user['email'])
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(user['password'])
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
        assert "/home" in driver.current_url
        driver.get("http://localhost:3000/create-activity")
        # Create activity
        category_select = driver.find_element(By.ID, "category")
        category_select.click()
        fitness_option = driver.find_element(By.XPATH, "//div[text()='Fitness']")
        fitness_option.click()
        start_date_field = driver.find_element(By.ID, "startDate")
        start_date_field.send_keys("2023-01-01")
        end_date_field = driver.find_element(By.ID, "endDate")
        end_date_field.send_keys("2023-01-02")
        is_recurring_checkbox = driver.find_element(By.ID, "isRecurring")
        is_recurring_checkbox.click()
        # post_text_field = driver.find_element(By.ID, "postText")
        # post_text_field.send_keys("Morning Yoga Session")
        visibility_public = driver.find_element(By.ID, "public")
        visibility_public.click()
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[errorMessageId='postText_error']")))
        error_message = driver.find_element(By.CSS_SELECTOR, "[errorMessageId='postText_error']")
        assert error_message.text == "Required"