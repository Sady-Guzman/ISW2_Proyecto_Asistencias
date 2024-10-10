import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def browser():
    # Set up the Selenium WebDriver to connect to the remote Selenium server
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless mode (no browser UI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options=options
    )
    yield driver
    driver.quit()

def test_login(browser):
    # Navigate to the login page
    browser.get("http://flask_app:5000/login")
    
    # Locate the username and password fields by their "name" attributes
    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")

    # Enter the username and password
    username_input.send_keys("testuser")  # Replace with an actual test user
    password_input.send_keys("123")  # Replace with the correct password
    
    # Submit the form (either via the return key or clicking the button)
    password_input.send_keys(Keys.RETURN)
    
    # Wait for the page to load after login
    browser.implicitly_wait(5)  # Waits up to 5 seconds for elements to load

    # Check that the login was successful (check for "Log Out" in the navbar)
    assert browser.find_element(By.LINK_TEXT, "Log Out")  # Verifies if "Log Out" link appears
    # You can also verify welcome messages or other indicators of successful login
    #assert "Welcome" in browser.page_source  # Adjust based on your app's behavior