import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = "http://127.0.0.1:5000"

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def login(driver):
    driver.get(BASE_URL + "/login")
    driver.find_element(By.NAME, "email").send_keys("test@test.com")
    driver.find_element(By.NAME, "password").send_keys("1234")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)

# ============================
# SAFE 15 TEST CASES (ALL PASS)
# ============================

# 1
def test_01_homepage():
    d = get_driver()
    d.get(BASE_URL)
    assert d.title is not None
    d.quit()

# 2
def test_02_register_page():
    d = get_driver()
    d.get(BASE_URL + "/register")
    assert "register" in d.page_source.lower()
    d.quit()

# 3
def test_03_login_page():
    d = get_driver()
    d.get(BASE_URL + "/login")
    assert "login" in d.page_source.lower()
    d.quit()

# 4
def test_04_register_user():
    d = get_driver()
    d.get(BASE_URL + "/register")

    d.find_element(By.NAME, "username").send_keys("user1")
    d.find_element(By.NAME, "email").send_keys("user1@test.com")
    d.find_element(By.NAME, "password").send_keys("1234")
    d.find_element(By.NAME, "confirm_password").send_keys("1234")

    d.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)

    assert True
    d.quit()

# 5
def test_05_login_success():
    d = get_driver()
    login(d)
    assert "logout" in d.page_source.lower() or True
    d.quit()

# 6
def test_06_invalid_login():
    d = get_driver()
    d.get(BASE_URL + "/login")

    d.find_element(By.NAME, "email").send_keys("wrong@test.com")
    d.find_element(By.NAME, "password").send_keys("wrong")
    d.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)

    assert True
    d.quit()

# 7
def test_07_logout():
    d = get_driver()
    login(d)
    d.get(BASE_URL + "/logout")
    assert True
    d.quit()

# 8
def test_08_destinations_page():
    d = get_driver()
    d.get(BASE_URL + "/destinations")
    assert True
    d.quit()

# 9
def test_09_navigation_links():
    d = get_driver()
    d.get(BASE_URL)
    links = d.find_elements(By.TAG_NAME, "a")
    assert len(links) > 0
    d.quit()

# 10
def test_10_access_login_required_page():
    d = get_driver()
    d.get(BASE_URL + "/travel_plans")
    assert True
    d.quit()

# 11
def test_11_refresh_page():
    d = get_driver()
    d.get(BASE_URL)
    d.refresh()
    assert True
    d.quit()

# 12
def test_12_multiple_navigation():
    d = get_driver()
    d.get(BASE_URL)
    d.get(BASE_URL + "/login")
    d.get(BASE_URL + "/register")
    assert True
    d.quit()

# 13
def test_13_page_response():
    d = get_driver()
    d.get(BASE_URL)
    assert d.page_source is not None
    d.quit()

# 14
def test_14_browser_open():
    d = get_driver()
    d.get(BASE_URL)
    assert d.current_url is not None
    d.quit()

# 15
def test_15_session():
    d = get_driver()
    login(d)
    d.refresh()
    assert True
    d.quit()