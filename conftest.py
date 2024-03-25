import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from test_utils import setup_test_user, teardown_test_user, confirm_email

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
    # options.add_argument("--headless")
    service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    yield driver
    driver.quit()
