import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from test_utils import setup_test_user, teardown_test_user, confirm_email, reset_email
# import test_utils
import psycopg2

import requests
import psycopg2
from bs4 import BeautifulSoup



def setup_test_user(i=0):
    url = "http://localhost:8080/api/v1/signup" 
    user_data = {
        "firstName": "User_" + str(i),
        "lastName": "Lastname_" + str(i),
        "userName": "testuser_" + str(i),
        "email": "test."+str(i)+"@example.com",
        "password": "1234",
        "dateOfBirth": "2000-01-01"
    }
    response = requests.post(url, json=user_data)
    if response.status_code != 200:
        raise Exception("Failed to create test user", response.content)
    return user_data

def reset_email(email):
    url = "http://localhost:8080/api/v1/login/reset/token" 
    user_data = {
    "email": email
    }
    response_password = requests.post(url, json=user_data)
    if response_password.status_code != 200:
        raise Exception("Failed to create test user", response_password.content)
    response = requests.get('http://localhost:1080/email')
    if response.status_code != 200:
        raise Exception("Failed to fetch emails")

    emails = response.json()

    # Find the confirmation email (assuming it's the latest email)
    confirmation_email = emails[-1]

    confirmation_link = parse_confirmation_link(confirmation_email['html'])
    return confirmation_link

def confirm_email():
    # Get all emails
    response = requests.get('http://localhost:1080/email')
    if response.status_code != 200:
        raise Exception("Failed to fetch emails")

    emails = response.json()

    # Find the confirmation email (assuming it's the latest email)
    confirmation_email = emails[-1]

    confirmation_link = parse_confirmation_link(confirmation_email['html'])

    response = requests.get(confirmation_link)
    if response.status_code != 200:
        raise Exception("Failed to confirm email")

def parse_confirmation_link(raw_email):
    soup = BeautifulSoup(raw_email, 'html.parser')
    link = soup.find('a')['href']

    return link


def teardown_test_user(i=0):
    # Connect to your postgres DB
    conn = psycopg2.connect(
        dbname="connect",
        user="postgres",
        password="connect",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE email = '"+"test."+str(i)+"@example.com';")
    user_id = cur.fetchone()[0]

    cur.execute("DELETE FROM token WHERE user_id = %s;", (user_id,))

    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))

    conn.commit()

    cur.close()
    conn.close()



@pytest.fixture(scope="function")
def setup_user():
    user = setup_test_user()
    confirm_email()
    yield user
    teardown_test_user()

@pytest.fixture(scope="session")
def driver_setup():
    """
    This fixture checks for the GeckoDriver's existence and downloads it if necessary.
    It then provides the path to the driver.
    """
    driver_path = GeckoDriverManager().install()
    return driver_path

@pytest.fixture(scope="function")
def driver(driver_setup):
    """
    Modified driver fixture to use the `driver_setup` fixture.
    This ensures the driver is downloaded if necessary and initializes the WebDriver.
    """
    options = FirefoxOptions()
    # Uncomment the next line to run Firefox headlessly
    # options.add_argument("--headless")
    service = FirefoxService(executable_path=driver_setup)
    driver = webdriver.Firefox(service=service, options=options)

    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def reset_password_setup(setup_user):
    user = setup_user
    link = reset_email(user['email'])
    yield user, link

@pytest.fixture(scope="function")
def db_connection():
    conn = psycopg2.connect(
        dbname="connect",
        user="postgres",
        password="connect",
        host="localhost",
        port="5432"
    )
    yield conn
    conn.close()

@pytest.fixture(scope="function")
def remove_activity():
    conn = psycopg2.connect(
        dbname="connect",
        user="postgres",
        password="connect",
        host="localhost",
        port="5432"
    )
    yield conn
    try:
        if conn.status != 0:
            conn = psycopg2.connect(
            dbname="connect",
            user="postgres",
            password="connect",
            host="localhost",
            port="5432"
            )
        with conn.cursor() as cur:
            cur.execute("SELECT postid FROM post WHERE posttext = 'Morning Yoga Session';")
            post_id = cur.fetchone()[0]
            cur.execute("DELETE FROM post WHERE postid = %s;", (post_id,))
            cur.execute("DELETE FROM activities WHERE postid = %s;", (post_id,))
            # Check in the attachments table if there exist a row that has the postid, if there is, delete it
            cur.execute("SELECT * FROM attachments WHERE postid = %s;", (post_id,))
            if cur.rowcount > 0:
                cur.execute("DELETE FROM attachments WHERE postid = %s;", (post_id,))
            conn.commit()
    except Exception as e:
        raise e

