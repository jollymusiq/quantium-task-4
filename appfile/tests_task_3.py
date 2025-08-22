# tests_task_3.py
import os
import certifi
import pytest
from dash.testing.application_runners import import_app
from selenium import webdriver

# Optional: auto-install drivers
import geckodriver_autoinstaller
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

# Fix SSL CA issues
os.environ["SSL_CERT_FILE"] = certifi.where()
geckodriver_autoinstaller.install()  # auto-install geckodriver

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox",
                     choices=["firefox", "chrome"], help="Browser to run tests")

@pytest.fixture
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture
def app():
    return import_app("task_3")  # replace with your Dash app filename

@pytest.fixture
def dash_duo(app, browser):
    from dash.testing.browser import DashComposite

    if browser == "firefox":
        options = FirefoxOptions()
        options.headless = True
        service = FirefoxService()
        driver = webdriver.Firefox(service=service, options=options)
    else:  # chrome
        options = ChromeOptions()
        options.headless = True
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    with DashComposite(server=app, browser=driver) as dc:
        yield dc

# Example tests
def test_headers_exist(dash_duo):
    dash_duo.wait_for_element("#header-h1")
    dash_duo.wait_for_element("#header-h2")

def test_radioitems_exist(dash_duo):
    dash_duo.wait_for_element("#region-selector")
