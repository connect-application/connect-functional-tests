import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from test_utils import sign_in, teardown_test_group, create_group, setup_test_user, teardown_test_user, confirm_email, reset_email
import psycopg2

@pytest.fixture(scope="function")
def setup_user():
    user = setup_test_user()
    confirm_email()
    yield user
    teardown_test_user()

@pytest.fixture(scope="function")
def setup_user_group(setup_user):
    user = setup_user
    s_user = setup_test_user(1)
    confirm_email()
    jwt_token = sign_in(user)
    s_group = create_group(token=jwt_token, i=1)
    yield user, s_user, s_group
    teardown_test_user(1)
    teardown_test_group(1)

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

# @pytest.fixture(scope="function")
# def remove_activity():
#     conn = psycopg2.connect(
#         dbname="connect",
#         user="postgres",
#         password="connect",
#         host="localhost",
#         port="5432"
#     )
#     yield conn
#     try:
#         if conn.status != 0:
#             conn = psycopg2.connect(
#             dbname="connect",
#             user="postgres",
#             password="connect",
#             host="localhost",
#             port="5432"
#             )
#         with conn.cursor() as cur:
#             cur.execute("SELECT postid FROM post WHERE posttext = 'Morning Yoga Session';")
#             post_id = cur.fetchone()[0]
#             cur.execute("DELETE FROM post WHERE postid = %s;", (post_id,))
#             cur.execute("DELETE FROM activities WHERE postid = %s;", (post_id,))
#             # Check in the attachments table if there exist a row that has the postid, if there is, delete it
#             cur.execute("SELECT * FROM attachments WHERE postid = %s;", (post_id,))
#             if cur.rowcount > 0:
#                 cur.execute("DELETE FROM attachments WHERE postid = %s;", (post_id,))
#             conn.commit()
#     except Exception as e:
#         raise e

