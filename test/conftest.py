from pathlib import Path
import pytest
import os
from selenium import webdriver
from dotenv import load_dotenv
from selene import browser

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
def setup_browser():
    browser.config.base_url = 'https://demoqa.com'

    options = webdriver.ChromeOptions()
    options.browser_version = "100.0"

    selenoid_capabilities = {
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    browser.config.driver_options = options
    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')

    browser.config.driver_remote_url = (
        f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub"
    )
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    yield browser

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_video(browser)

    browser.quit()