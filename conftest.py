import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from test_utils import follow_user, set_about, sign_in, teardown_test_group, create_group, setup_test_user, teardown_test_user, confirm_email, reset_email
import psycopg2

@pytest.fixture(scope="function")
def setup_user():
    user = setup_test_user()
    confirm_email()
    _, id_user = sign_in(user)
    user['id'] = id_user
    yield user
    teardown_test_user()

@pytest.fixture(scope="function")
def setup_users_profile():
    user_0 = setup_test_user(0)
    confirm_email()
    user_1 = setup_test_user(1)
    confirm_email()
    user_2 = setup_test_user(2)
    confirm_email()
    user_3 = setup_test_user(3)
    confirm_email()

    user_0['token'], user_0['id'] = sign_in(user_0)
    user_1['token'], user_1['id'] = sign_in(user_1)
    user_2['token'], user_2['id'] = sign_in(user_2)
    user_3['token'], user_3['id'] = sign_in(user_3)

    set_about(user_0, "Example about 0")
    follow_user(user_0, user_1)
    follow_user(user_0, user_2)
    follow_user(user_1, user_0)
    follow_user(user_3, user_0)


    yield user_0, user_1, user_2, user_3
    teardown_test_user(0)
    teardown_test_user(1)
    teardown_test_user(2)
    teardown_test_user(3)

@pytest.fixture(scope="function")
def setup_user_group(setup_user):
    user = setup_user
    s_user = setup_test_user(1)
    confirm_email()
    jwt_token, id_user = sign_in(user)
    user['id'] = id_user
    s_group = create_group(token=jwt_token, i=1)
    _, id_user1 = sign_in(s_user)
    s_user['id'] = id_user1
    yield user, s_user, s_group
    teardown_test_user(1)
    teardown_test_group(1)

@pytest.fixture(scope="session")
def driver_setup():
    driver_path = GeckoDriverManager().install()
    return driver_path

@pytest.fixture(scope="function")
def driver(driver_setup):
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

@pytest.fixture(scope="session")
def driver_setup_chrome():
    driver_path = ChromeDriverManager().install()
    return driver_path

@pytest.fixture(scope="function")
def driver_chrome(driver_setup_chrome):
    options = ChromeOptions()
    service = ChromeService(executable_path=driver_setup_chrome)
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()