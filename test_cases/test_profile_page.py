# test_profile_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import os

class TestProfilePage:
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
        search_button = driver.find_element(By.XPATH, "//span[text()='Profile']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/profile"))
        assert "/profile" in driver.current_url
    
    def test_PROFILE_check_user_information(self, setup_user, driver):
        # Test if the user's username, first name and last name are displayed correctly
        
        user = setup_user
        self.sign_in(driver, user)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-username")))
        username_element = driver.find_element(By.ID, "profile-username")
        assert username_element.text == user['userName']
        name_element = driver.find_element(By.ID, "profile-name")
        assert name_element.text == f"{user['firstName']} {user['lastName']}"
    
    def test_PROFILE_check_about(self, setup_users_profile, driver):
        # Test if the user's about is displayed correctly
        
        user, _, _, _ = setup_users_profile
        self.sign_in(driver, user)
        # find about using WebDriverWait
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-about")))
        about_text = driver.find_element(By.ID, "profile-about")
        assert about_text.text == "Example about 0"

    def test_PROFILE_check_about_default(self, setup_user, driver):
        # Test if the user's about is displayed correctly when the user has not set it
        
        user = setup_user
        self.sign_in(driver, user)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-about")))
        about_text = driver.find_element(By.ID, "profile-about")
        assert about_text.text == "User has not provided an about section."

    # def test_PROFILE_check_profile_picture(self, driver):
    #     # Test if the user's profile picture is displayed correctly
    #     pass

    # def test_PROFILE_check_profile_picture_default(self, setup_user, driver):
    #     # Test if the user's profile picture is displayed correctly when the user has not set it
        
    #     user = setup_user
    #     self.sign_in(driver, user)
    #     print('a')

    def test_PROFILE_followers(self, setup_users_profile, driver):
        # Test if the user's followers is displayed correctly in the count and the list
        
        user, user_1, user_2, user_3 = setup_users_profile
        self.sign_in(driver, user)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-followers-count")))
        WebDriverWait(driver, 10)
        followers_count = driver.find_element(By.ID, "profile-followers-count")
        assert followers_count.text == "2"
        followers_list = driver.find_element(By.ID, "list-Followers")
        follower_username_1 = followers_list.find_element(By.ID, f"follower-{user_1['userName']}")
        assert follower_username_1.text == user_1['userName']
        follower_username_3 = followers_list.find_element(By.ID, f"follower-{user_3['userName']}")
        assert follower_username_3.text == user_3['userName']
        follower_item = follower_username_1.find_element(By.XPATH, "..")
        follower_item.click()
        WebDriverWait(driver, 10).until(EC.url_contains(f"/profile/{user_1['id']}"))
        assert f"/profile/{user_1['id']}" in driver.current_url


    def test_PROFILE_following(self, setup_users_profile, driver):
        # Test if the user's following is displayed correctly in the count and the list
        
        user, user_1, user_2, user_3 = setup_users_profile
        self.sign_in(driver, user)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-following-count")))
        WebDriverWait(driver, 10)
        following_count = driver.find_element(By.ID, "profile-following-count")
        assert following_count.text == "2"
        following_list = driver.find_element(By.ID, "list-Following")
        following_username_1 = following_list.find_element(By.ID, f"follower-{user_1['userName']}")
        assert following_username_1.text == user_1['userName']
        following_username_2 = following_list.find_element(By.ID, f"follower-{user_2['userName']}")
        assert following_username_2.text == user_2['userName']
        following_item = following_username_1.find_element(By.XPATH, "..")
        following_item.click()
        WebDriverWait(driver, 10).until(EC.url_contains(f"/profile/{user_1['id']}"))
        assert f"/profile/{user_1['id']}" in driver.current_url


    def test_PROFILE_posts(self, setup_user, driver):
        # Test if the user's posts are displayed correctly
        
        user = setup_user
        self.sign_in(driver, user)
        # FInd div with id post-list
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "post-list")))
        post_list = driver.find_element(By.ID, "post-list")
        # Find all divs with class post-item and assert that there is 0
        post_items = post_list.find_elements(By.ID, "post-item")
        assert len(post_items) == 0
        # Create a post
        driver.get("http://localhost:3000/create-post")
        driver.find_element(By.TAG_NAME, "textarea").send_keys("This is a test post")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        driver.execute_script("arguments[0].click();", submit_button)
        WebDriverWait(driver, 10).until(EC.url_contains("/create-post/success"))
        assert "/create-post/success" in driver.current_url
        search_button = driver.find_element(By.XPATH, "//span[text()='Profile']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/profile"))
        assert "/profile" in driver.current_url
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "post-list")))
        post_list = driver.find_element(By.ID, "post-list")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "post-item")))
        post_items = post_list.find_elements(By.ID, "post-item")
        assert len(post_items) == 1
        # Verify "This is a test post" is in the post
        post_text = post_items[0].find_element(By.ID, "post-text")
        assert post_text.text == "This is a test post"
        self.remove_post()

    def test_PROFILE_navegate_edit_profile(self, setup_user, driver):
        # Test if the user can navigate to the edit profile page
        
        user = setup_user
        self.sign_in(driver, user)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-btn")))
        edit_button = driver.find_element(By.ID, "profile-btn")
        assert edit_button.text == "Edit profile"
        edit_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/profile/edit"))
        assert "/profile/edit" in driver.current_url


    def test_PROFILE_follow_user(self, setup_users_profile, driver):
        # Test if the user can follow another user from the profile page
        
        user, user_1, user_2, user_3 = setup_users_profile
        self.sign_in(driver, user)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-followers-count")))
        WebDriverWait(driver, 10)
        followers_list = driver.find_element(By.ID, "list-Followers")
        follower_username_3 = followers_list.find_element(By.ID, f"follower-{user_3['userName']}")
        assert follower_username_3.text == user_3['userName']
        div_username_3 = follower_username_3.find_element(By.TAG_NAME, "div")
        div_username_3.click()
        WebDriverWait(driver, 10).until(EC.url_contains(f"/profile/{user_3['id']}"))
        assert f"/profile/{user_3['id']}" in driver.current_url
        follow_button = driver.find_element(By.ID, "profile-btn")
        assert follow_button.text == "Follow"
        follow_button.click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, "profile-btn"), "Unfollow"))
        assert follow_button.text == "Unfollow"
        search_button = driver.find_element(By.XPATH, "//span[text()='Profile']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/profile"))
        assert "/profile" in driver.current_url
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-followers-count")))
        WebDriverWait(driver, 10)
        following_count = driver.find_element(By.ID, "profile-following-count")
        assert following_count.text == "3"
        following_list = driver.find_element(By.ID, "list-Following")
        following_username_3 = following_list.find_element(By.ID, f"follower-{user_3['userName']}")
        assert following_username_3.text == user_3['userName']


    def test_PROFILE_unfollow_user(self, setup_users_profile, driver):
        # Test if the user can unfollow another user from the profile page
        
        user, user_1, user_2, user_3 = setup_users_profile
        self.sign_in(driver, user)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-following-count")))
        WebDriverWait(driver, 10)
        following_list = driver.find_element(By.ID, "list-Following")
        follower_username_2 = following_list.find_element(By.ID, f"follower-{user_2['userName']}")
        assert follower_username_2.text == user_2['userName']
        div_username_2 = follower_username_2.find_element(By.TAG_NAME, "div")
        div_username_2.click()
        WebDriverWait(driver, 10).until(EC.url_contains(f"/profile/{user_2['id']}"))
        assert f"/profile/{user_2['id']}" in driver.current_url
        follow_button = driver.find_element(By.ID, "profile-btn")
        assert follow_button.text == "Unfollow"
        follow_button.click()
        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.ID, "profile-btn"), "Follow"))
        assert follow_button.text == "Follow"
        search_button = driver.find_element(By.XPATH, "//span[text()='Profile']")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/profile"))
        assert "/profile" in driver.current_url
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profile-following-count")))
        WebDriverWait(driver, 10)
        following_count = driver.find_element(By.ID, "profile-following-count")
        assert following_count.text == "1"
        following_list = driver.find_element(By.ID, "list-Following")
        try:
            following_username_2 = following_list.find_element(By.ID, f"follower-{user_2['userName']}")
            assert False
        except:
            assert True

