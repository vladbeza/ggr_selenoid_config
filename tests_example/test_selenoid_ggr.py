from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


def test_python_jobs_exist(browser):
    browser.get("host.docker.internal:8080")
    # browser.get("localhost:8080")

    city_select = Select(browser.find_element(By.CSS_SELECTOR, "select#city"))
    city_select.select_by_visible_text("Харьков")

    language_select = Select(browser.find_element(By.CSS_SELECTOR,
                                                  "select#language"))
    language_select.select_by_visible_text("Python")

    browser.find_element(By.CSS_SELECTOR, "input[name=submit]").click()

    jobs = browser.find_elements(By.CSS_SELECTOR, "ul#jobs-list li#job-item")

    assert len(jobs) == 18
