import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
#from test_utils import setup_test_user, teardown_test_user, confirm_email, reset_email
import test_utils
import psycopg2

@pytest.fixture(scope="function")
def setup_user():
    user = setup_test_user()
    confirm_email()
    yield user
    teardown_test_user()

@pytest.fixture(scope="function")
def driver(request):
    options = FirefoxOptions()
    # Uncomment the next line to run Firefox headlessly
    #options.add_argument("--headless")
    service = FirefoxService(executable_path=GeckoDriverManager().install())
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

