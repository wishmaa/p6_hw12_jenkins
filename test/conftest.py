import pytest
from pathlib import Path
from selene import browser
from selenium import webdriver


def path(file_name):
    import test
    return str(Path(test.__file__).parent.joinpath(f'picture/{file_name}').absolute())

@pytest.fixture(scope='function', autouse=True)
def browser_management():
    browser.config.base_url = 'https://demoqa.com'
    browser.config.window_width = 1620
    browser.config.window_height = 1080
    driver_options = webdriver.ChromeOptions()
    browser.config.driver_options = driver_options

    yield

    browser.quit()