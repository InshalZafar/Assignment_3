"""Selenium test suite for Aurelia (Tourism Explorer revamp).

Runs against a live Flask server at http://127.0.0.1:5000. Start it with:
    python app.py
and seed with:
    python populate_db.py
before running:
    pytest -v tests/test_app.py
"""
import time
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5000"


def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1400,900")
    return webdriver.Chrome(options=options)


def login(driver, email="test@test.com", password="1234"):
    driver.get(BASE_URL + "/login")
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1.5)


def unique_user():
    suffix = uuid.uuid4().hex[:8]
    return f"u_{suffix}", f"u_{suffix}@test.com", "abcd1234"


# =========================================================
# ORIGINAL 15 — preserved for backwards compatibility
# =========================================================

def test_01_homepage():
    d = get_driver()
    d.get(BASE_URL)
    assert d.title is not None
    d.quit()


def test_02_register_page():
    d = get_driver()
    d.get(BASE_URL + "/register")
    assert "register" in d.page_source.lower() or "account" in d.page_source.lower()
    d.quit()


def test_03_login_page():
    d = get_driver()
    d.get(BASE_URL + "/login")
    assert "login" in d.page_source.lower() or "sign in" in d.page_source.lower()
    d.quit()


def test_04_register_user():
    d = get_driver()
    d.get(BASE_URL + "/register")
    username, email, pw = unique_user()
    d.find_element(By.NAME, "username").send_keys(username)
    d.find_element(By.NAME, "email").send_keys(email)
    d.find_element(By.NAME, "password").send_keys(pw)
    d.find_element(By.NAME, "confirm_password").send_keys(pw)
    d.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)
    assert True
    d.quit()


def test_05_login_success():
    d = get_driver()
    login(d)
    assert "logout" in d.page_source.lower() or True
    d.quit()


def test_06_invalid_login():
    d = get_driver()
    d.get(BASE_URL + "/login")
    d.find_element(By.NAME, "email").send_keys("wrong@test.com")
    d.find_element(By.NAME, "password").send_keys("wrong")
    d.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)
    assert True
    d.quit()


def test_07_logout():
    d = get_driver()
    login(d)
    d.get(BASE_URL + "/logout")
    assert True
    d.quit()


def test_08_destinations_page():
    d = get_driver()
    d.get(BASE_URL + "/destinations")
    assert True
    d.quit()


def test_09_navigation_links():
    d = get_driver()
    d.get(BASE_URL)
    links = d.find_elements(By.TAG_NAME, "a")
    assert len(links) > 0
    d.quit()


def test_10_access_login_required_page():
    d = get_driver()
    d.get(BASE_URL + "/travel_plans")
    assert True
    d.quit()


def test_11_refresh_page():
    d = get_driver()
    d.get(BASE_URL)
    d.refresh()
    assert True
    d.quit()


def test_12_multiple_navigation():
    d = get_driver()
    d.get(BASE_URL)
    d.get(BASE_URL + "/login")
    d.get(BASE_URL + "/register")
    assert True
    d.quit()


def test_13_page_response():
    d = get_driver()
    d.get(BASE_URL)
    assert d.page_source is not None
    d.quit()


def test_14_browser_open():
    d = get_driver()
    d.get(BASE_URL)
    assert d.current_url is not None
    d.quit()


def test_15_session():
    d = get_driver()
    login(d)
    d.refresh()
    assert True
    d.quit()


# =========================================================
# NEW TESTS — Aurelia features (16-35)
# =========================================================

def test_16_brand_visible():
    d = get_driver()
    d.get(BASE_URL)
    brand = d.find_element(By.CLASS_NAME, "brand")
    assert "Aurelia" in brand.text
    d.quit()


def test_17_hero_search_form_present():
    d = get_driver()
    d.get(BASE_URL)
    form = d.find_element(By.CSS_SELECTOR, "form.search-hero")
    assert form is not None
    inp = form.find_element(By.NAME, "q")
    assert inp.get_attribute("placeholder")
    d.quit()


def test_18_hero_search_redirects_to_search():
    d = get_driver()
    d.get(BASE_URL)
    inp = d.find_element(By.CSS_SELECTOR, "form.search-hero input[name='q']")
    inp.send_keys("Tokyo")
    d.find_element(By.CSS_SELECTOR, "form.search-hero button").click()
    time.sleep(1.5)
    assert "/search" in d.current_url
    assert "q=Tokyo" in d.current_url
    d.quit()


def test_19_search_results_render():
    d = get_driver()
    d.get(BASE_URL + "/search?q=Tokyo")
    time.sleep(1)
    assert "results" in d.page_source.lower() or "tokyo" in d.page_source.lower()
    d.quit()


def test_20_category_pills_navigate():
    d = get_driver()
    d.get(BASE_URL + "/category/Beach")
    time.sleep(1)
    assert "beach" in d.page_source.lower()
    d.quit()


def test_21_dashboard_loads_with_stats():
    d = get_driver()
    d.get(BASE_URL + "/dashboard")
    time.sleep(1)
    counters = d.find_elements(By.CSS_SELECTOR, "[data-count]")
    assert len(counters) >= 4
    d.quit()


def test_22_map_page_loads():
    d = get_driver()
    d.get(BASE_URL + "/map")
    time.sleep(2)
    assert d.find_element(By.ID, "map") is not None
    d.quit()


def test_23_dashboard_heading_present():
    d = get_driver()
    d.get(BASE_URL + "/dashboard")
    heading = d.find_element(By.ID, "dashboard-heading")
    assert "Aurelia" in heading.text or "Dashboard" in heading.text
    d.quit()


def test_24_destination_card_renders():
    d = get_driver()
    d.get(BASE_URL + "/destinations")
    time.sleep(1)
    cards = d.find_elements(By.CLASS_NAME, "dest-card")
    assert len(cards) > 0
    d.quit()


def test_25_destination_detail_has_weather_widget():
    d = get_driver()
    d.get(BASE_URL + "/destinations")
    time.sleep(1)
    cards = d.find_elements(By.CLASS_NAME, "dest-card")
    if cards:
        link = cards[0].find_element(By.TAG_NAME, "a")
        link.click()
        time.sleep(1.5)
        weather = d.find_elements(By.CSS_SELECTOR, "[data-weather]")
        assert len(weather) >= 1
    d.quit()


def test_26_review_form_has_star_widget_when_logged_in():
    d = get_driver()
    login(d)
    d.get(BASE_URL + "/destinations")
    time.sleep(1)
    cards = d.find_elements(By.CLASS_NAME, "dest-card")
    if cards:
        cards[0].find_element(By.TAG_NAME, "a").click()
        time.sleep(1.5)
        widget = d.find_elements(By.CLASS_NAME, "star-rating")
        assert len(widget) >= 1
    d.quit()


def test_27_wishlist_page_requires_login_redirect():
    d = get_driver()
    d.get(BASE_URL + "/wishlist")
    time.sleep(1)
    assert "/login" in d.current_url or "login" in d.page_source.lower()
    d.quit()


def test_28_wishlist_page_loads_when_logged_in():
    d = get_driver()
    login(d)
    d.get(BASE_URL + "/wishlist")
    time.sleep(1)
    heading = d.find_element(By.ID, "wishlist-heading")
    assert heading is not None
    d.quit()


def test_29_profile_page_renders_for_seeded_user():
    d = get_driver()
    d.get(BASE_URL + "/profile/test")
    time.sleep(1)
    username = d.find_element(By.ID, "profile-username")
    assert "test" in username.text.lower()
    d.quit()


def test_30_profile_shows_stats_counters():
    d = get_driver()
    d.get(BASE_URL + "/profile/test")
    time.sleep(1)
    nums = d.find_elements(By.CLASS_NAME, "n")
    assert len(nums) >= 3
    d.quit()


def test_31_navigation_brand_link_returns_home():
    d = get_driver()
    d.get(BASE_URL + "/login")
    d.find_element(By.CLASS_NAME, "brand").click()
    time.sleep(1)
    assert d.current_url.rstrip("/") == BASE_URL.rstrip("/")
    d.quit()


def test_32_destinations_grid_visible():
    d = get_driver()
    d.get(BASE_URL + "/destinations")
    time.sleep(1)
    grids = d.find_elements(By.CLASS_NAME, "dest-grid")
    assert len(grids) >= 1
    d.quit()


def test_33_create_plan_form_has_date_fields():
    d = get_driver()
    login(d)
    d.get(BASE_URL + "/create_plan")
    time.sleep(1)
    start = d.find_elements(By.NAME, "start_date")
    end = d.find_elements(By.NAME, "end_date")
    budget = d.find_elements(By.NAME, "budget")
    assert len(start) == 1 and len(end) == 1 and len(budget) == 1
    d.quit()


def test_34_search_form_has_filters():
    d = get_driver()
    d.get(BASE_URL + "/search")
    time.sleep(1)
    cat = d.find_elements(By.NAME, "category")
    rating = d.find_elements(By.NAME, "min_rating")
    assert len(cat) == 1 and len(rating) == 1
    d.quit()


def test_35_register_then_login_flow():
    d = get_driver()
    username, email, pw = unique_user()
    d.get(BASE_URL + "/register")
    d.find_element(By.NAME, "username").send_keys(username)
    d.find_element(By.NAME, "email").send_keys(email)
    d.find_element(By.NAME, "password").send_keys(pw)
    d.find_element(By.NAME, "confirm_password").send_keys(pw)
    d.find_element(By.TAG_NAME, "button").click()
    time.sleep(2)
    login(d, email=email, password=pw)
    d.get(BASE_URL + "/wishlist")
    time.sleep(1)
    assert "wishlist" in d.page_source.lower() or "saved" in d.page_source.lower()
    d.quit()


def test_36_theme_toggle_button_exists():
    d = get_driver()
    d.get(BASE_URL)
    btns = d.find_elements(By.CLASS_NAME, "theme-toggle")
    assert len(btns) >= 1
    d.quit()


def test_37_footer_renders():
    d = get_driver()
    d.get(BASE_URL)
    footer = d.find_element(By.CLASS_NAME, "luxe-footer")
    assert "Aurelia" in footer.text
    d.quit()


def test_38_404_page():
    d = get_driver()
    d.get(BASE_URL + "/this-route-does-not-exist-xyz")
    time.sleep(1)
    assert "404" in d.page_source or "Off the Map" in d.page_source
    d.quit()


def test_39_map_heading_visible():
    d = get_driver()
    d.get(BASE_URL + "/map")
    time.sleep(1)
    h = d.find_element(By.ID, "map-heading")
    assert "World" in h.text or "Explore" in h.text
    d.quit()


def test_40_search_heading_visible():
    d = get_driver()
    d.get(BASE_URL + "/search")
    time.sleep(1)
    h = d.find_element(By.ID, "search-heading")
    assert h is not None
    d.quit()
