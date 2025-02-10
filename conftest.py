import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def setup_teardown():
    options = webdriver.ChromeOptions()

    # Prevent browser from closing immediately
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    yield driver

    driver.quit()
