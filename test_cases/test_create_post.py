# test_create_post.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import os


class TestCreatePost:
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
        cur.execute("SELECT COUNT(*) FROM post WHERE posttext='This is a test post'")
        post_count = cur.fetchone()[0]
        assert post_count == 1
        if private:
            # assert that the post is private in the 'ispublic' column from the post table
            cur.execute("SELECT ispublic FROM post WHERE posttext='This is a test post'")
            is_public = cur.fetchone()[0]
            assert not is_public
        cur.execute("SELECT postid FROM post WHERE posttext='This is a test post'")
        post_id = cur.fetchone()[0]
        cur.execute("DELETE FROM post WHERE postid=%s", (post_id,))
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
    
    def test_CREATE_POST_no_attachement(self, driver, setup_user):
        # Test if the user can create a post without an attachment
        user = setup_user
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/create-post")
        driver.find_element(By.TAG_NAME, "textarea").send_keys("This is a test post")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/create-post/success"))
        assert "/create-post/success" in driver.current_url
        self.remove_post()

    def test_CREATE_POST_with_attachement(self, driver, setup_user):
        # Test if the user can create a post with an attachment
        user = setup_user
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/create-post")
        file_input_ref = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'resources', 'meditate.jpg')
        file_input_ref.send_keys(file_path)
        driver.find_element(By.TAG_NAME, "textarea").send_keys("This is a test post")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/create-post/success"))
        assert "/create-post/success" in driver.current_url
        post_id = self.remove_post()
        self.remove_attachment(post_id)

    def test_CREATE_POST_without_caption(self, driver, setup_user):
        # Test if the user can create a post without a caption
        user = setup_user
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/create-post")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "p.error-message")))
        assert error_message.text == "Required"

    def test_CREATE_POST_private(self, driver, setup_user):
        # Test if the user can create a private post
        user = setup_user
        self.sign_in(driver, user)
        driver.get("http://localhost:3000/create-post")
        driver.find_element(By.TAG_NAME, "textarea").send_keys("This is a test post")
        # find element input with name "visibility and set its value to "private, it is a radio button"
        driver.execute_script("document.querySelector('input[name=\"visibility\"][value=\"private\"]').click()")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/create-post/success"))
        assert "/create-post/success" in driver.current_url
        self.remove_post(private=True)

    # def test_CREATE_POST_group(self, driver, setup_user):
    #     # Test if the user can create a post for a group
    #     user = setup_user
    #     self.sign_in(driver, user)
    #     driver.get("http://localhost:3000/create-post")
    #     driver.find_element(By.TAG_NAME, "textarea").send_keys("This is a test post")
    #     submit_button = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    #     driver.execute_script("arguments[0].click();", submit_button)
    #     WebDriverWait(driver, 10).until(EC.url_contains("/create-post/success"))
    #     assert "/create-post/success" in driver.current_url
    #     self.remove_post()