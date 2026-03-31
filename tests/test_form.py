from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select


@pytest.fixture
def driver():
    options = Options()
    options.set_capability("pageLoadStrategy", "normal")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        web_driver = webdriver.Chrome(options=options)
    except InvalidArgumentException as exc:
        if "pageLoadStrategy" not in str(exc):
            raise
        # Some older driver stacks reject this capability key; retry without it.
        options._caps.pop("pageLoadStrategy", None)
        web_driver = webdriver.Chrome(options=options)

    yield web_driver
    web_driver.quit()


def page_url() -> str:
    form_path = Path(__file__).resolve().parents[1] / "index.html"
    return form_path.as_uri()


def open_form(driver):
    driver.get(page_url())


def fill_valid_data(driver):
    driver.find_element(By.ID, "studentName").send_keys("Aarav Sharma")
    driver.find_element(By.ID, "email").send_keys("aarav.sharma@example.com")
    driver.find_element(By.ID, "mobile").send_keys("9876543210")
    Select(driver.find_element(By.ID, "department")).select_by_visible_text("Computer Science")
    driver.find_element(By.CSS_SELECTOR, 'input[name="gender"][value="male"]').click()
    driver.find_element(By.ID, "feedback").send_keys(
        "The teaching quality is excellent and the labs are very practical and engaging for everyone."
    )


def test_page_opens_successfully(driver):
    open_form(driver)
    title = driver.find_element(By.ID, "formTitle").text
    assert "Student Feedback Registration Form" in title


def test_valid_submission_shows_success(driver):
    open_form(driver)
    fill_valid_data(driver)
    driver.find_element(By.ID, "submitBtn").click()

    msg = driver.find_element(By.ID, "formMessage").text
    assert "Feedback submitted successfully." in msg


def test_blank_mandatory_fields_show_errors(driver):
    open_form(driver)
    driver.find_element(By.ID, "submitBtn").click()

    assert "Student Name is required." in driver.find_element(By.ID, "studentNameError").text
    assert "Email ID is required." in driver.find_element(By.ID, "emailError").text
    assert "Mobile Number is required." in driver.find_element(By.ID, "mobileError").text
    assert "Please select a department." in driver.find_element(By.ID, "departmentError").text
    assert "Please select a gender option." in driver.find_element(By.ID, "genderError").text
    assert "Feedback Comments cannot be blank." in driver.find_element(By.ID, "feedbackError").text


def test_invalid_email_validation(driver):
    open_form(driver)
    fill_valid_data(driver)

    email = driver.find_element(By.ID, "email")
    email.clear()
    email.send_keys("invalid-email-format")
    driver.find_element(By.ID, "submitBtn").click()

    assert "Enter a valid email format." in driver.find_element(By.ID, "emailError").text


def test_invalid_mobile_validation(driver):
    open_form(driver)
    fill_valid_data(driver)

    mobile = driver.find_element(By.ID, "mobile")
    mobile.clear()
    mobile.send_keys("98AB21")
    driver.find_element(By.ID, "submitBtn").click()

    assert "exactly 10 digits" in driver.find_element(By.ID, "mobileError").text


def test_department_dropdown_selection(driver):
    open_form(driver)

    dropdown = Select(driver.find_element(By.ID, "department"))
    dropdown.select_by_visible_text("Mechanical")

    assert dropdown.first_selected_option.text == "Mechanical"


def test_submit_and_reset_buttons(driver):
    open_form(driver)
    fill_valid_data(driver)

    driver.find_element(By.ID, "resetBtn").click()

    assert driver.find_element(By.ID, "studentName").get_attribute("value") == ""
    assert driver.find_element(By.ID, "email").get_attribute("value") == ""
    assert driver.find_element(By.ID, "mobile").get_attribute("value") == ""
    assert driver.find_element(By.ID, "department").get_attribute("value") == ""
    assert driver.find_element(By.ID, "feedback").get_attribute("value") == ""
