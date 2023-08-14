from pathlib import Path
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import Browser, Config, browser
from dotenv import load_dotenv
from utils import attach


DEFAULT_BROWSER_VERSION = "100.0"


# @pytest.fixture(scope='function', autouse=True)
# def browser_management():
#     browser.config.base_url = 'https://demoqa.com'
#     browser.config.window_width = 1620
#     browser.config.window_height = 1080
#     driver_options = webdriver.ChromeOptions()
#     browser.config.driver_options = driver_options
#
#     yield
#
#     browser.quit()


def path(file_name):
    import test
    return str(Path(test.__file__).parent.joinpath(f'picture/{file_name}').absolute())


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='100.0'
    )


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function')
def setup_browser(request):
    browser.config.base_url = 'https://demoqa.com'
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')

    driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
        options=options
    )
    browser2 = Browser(Config(driver=driver))

    yield browser

    attach.add_html(browser2)
    attach.add_screenshot(browser2)
    attach.add_logs(browser2)
    attach.add_video(browser2)
    browser.quit()
