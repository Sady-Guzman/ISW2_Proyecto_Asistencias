import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def browser():
    # Set up the Selenium WebDriver to connect to the remote Selenium server
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options=options
    )
    yield driver
    driver.quit()

def test_user_login(browser):
    browser.get("http://flask_app:5000/login")
    
    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")

    username_input.send_keys("testuser")
    password_input.send_keys("123")
    password_input.send_keys(Keys.RETURN)

    browser.implicitly_wait(5)
    
    assert browser.find_element(By.LINK_TEXT, "Log Out")
    # assert "Welcome" in browser.page_source

def test_invalid_user_login(browser):
    browser.get("http://flask_app:5000/login")

    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")

    username_input.send_keys("wronguser")
    password_input.send_keys("wrongpassword")
    password_input.send_keys(Keys.RETURN)

    browser.implicitly_wait(5)

    # Check that login failed (you might check for an error message or verify the user stays on the login page)
    assert "Invalid credentials" in browser.page_source  # Assuming there's an error message for invalid login
    assert "CleanSys: Login" in browser.title  # Verify still on login page

def test_admin_login(browser):
    browser.get("http://flask_app:5000/adlogin")

    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")

    username_input.send_keys("admin")
    password_input.send_keys("domino")
    password_input.send_keys(Keys.RETURN)

    browser.implicitly_wait(5)
    
    assert browser.find_element(By.LINK_TEXT, "Log Out")
    assert "Crear cuenta" in browser.page_source  # Adjust based on your admin page

def test_invalid_admin_login(browser):
    browser.get("http://flask_app:5000/adlogin")

    username_input = browser.find_element(By.NAME, "usernamtee")
    password_input = browser.find_element(By.NAME, "password")

    username_input.send_keys("notadmin")
    password_input.send_keys("wrongpassword")
    password_input.send_keys(Keys.RETURN)

    browser.implicitly_wait(5)

    # Check that login failed for admin
    assert "Invalid credentials" in browser.page_source  # Assuming there's an error message for admin
    assert "CleanSys: Admin Login" in browser.title  # Verify still on login page