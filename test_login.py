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

    username_input.send_keys("testuser") # usuario creado a mano para test
    password_input.send_keys("123") # contrasena creada a mano para test
    password_input.send_keys(Keys.RETURN)

    browser.implicitly_wait(5)
    
    # Check that login was successful (e.g., "Log Out" appears in the navbar)
    # assert browser.find_element(By.LINK_TEXT, "Log Out")
    # assert "Welcome" in browser.page_source

def test_admin_login(browser):
    # Navigate to the admin login page
    browser.get("http://flask_app:5000/adlogin")

    # Locate the username and password fields by their "name" attributes
    username_input = browser.find_element(By.NAME, "username")
    password_input = browser.find_element(By.NAME, "password")

    # Enter the admin credentials
    username_input.send_keys("admin") # Cuenta unica de admin
    password_input.send_keys("domino")
    password_input.send_keys(Keys.RETURN)

    # Wait for the page to load after login
    browser.implicitly_wait(5)
    
    # Check that admin login was successful (e.g., "Log Out" appears in the navbar)
    assert browser.find_element(By.LINK_TEXT, "Log Out")
    # Optionally check if there is any admin-specific message or functionality
    # assert "Admin Panel" in browser.page_source  # Adjust this based on the admin page content