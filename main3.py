from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import difflib
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from config import medications, Medication, LINK_ADDRESS
from typing import Optional, Union
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


def find_input_by_label(label_text: str, driver: WebDriver) -> Union[WebElement, None]:
    try:
        # Using XPath to find input by label
        label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//label[contains(text(), '{label_text}')]/following-sibling::div//input"))
        )
        return label
    except TimeoutException:
        print(f"Input field with label '{label_text}' not found.")
        return None


def normalize_text(text: str) -> str:
    """Normalize text. 1177 updates their webpage once a month, i cant keep track with this!!"""
    return "".join(text.lower().split())


def fuzzy_match(driver: WebDriver, expected_text: str, threshold: float = 0.8) -> bool:
    """Lmao Big O notation what is that? computers are fast. BRRRRRRRRRRRRRR check everything at once"""
    elements = driver.find_elements(By.XPATH, "//*")
    normalized_expected_text = normalize_text(expected_text)
    for element in elements:
        try:
            element_text = element.text
            if element_text:  # Ensure the text is not empty
                normalized_element_text = normalize_text(element_text)
                ratio = difflib.SequenceMatcher(None, normalized_expected_text, normalized_element_text).ratio()
                if ratio >= threshold:
                    return True
        except Exception as e:
            continue  # Skip elements that do not have visible text or cause any error when accessing text
    return False


def find_closest_match(label_text: str, driver: WebDriver) -> Union[WebElement, None]:
    """Use fuzzy matching"""
    labels = driver.find_elements(By.TAG_NAME, "label")
    normalized_label_text = normalize_text(label_text)
    closest_label = None
    highest_ratio = 0.8

    for label in labels:
        text = normalize_text(label.text)
        ratio = difflib.SequenceMatcher(None, normalized_label_text, text).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            closest_label = label

    if closest_label:
        return closest_label.find_element(By.XPATH, "following-sibling::div//input")
    else:
        return None


def robust_find_input_by_label(label_text: str, driver: WebDriver) -> Union[None, WebElement]:
    """
    Finds an input element by its label text using both direct and fuzzy matching strategies.

    Parameters:
        label_text (str): The text of the label associated with the input element.
        driver (WebDriver): The WebDriver instance controlling the browser.

    Returns:
        WebElement: The input element found or None if no element is found.
    """
    input_element = find_input_by_label(label_text, driver)
    if input_element is None:
        input_element = find_closest_match(label_text, driver)
    return input_element


def fill_input_field(input_element: Optional[WebElement], value: str) -> None:
    """
    Clears and fills an input field with the specified value if the element is not None.

    Args:
        input_element (Optional[WebElement]): The input field element to fill.
        value (str): The value to enter into the input field.
    """
    if input_element is not None:
        input_element.clear()
        input_element.send_keys(value)
        input_element.send_keys(Keys.TAB)
    else:
        print("Attempted to fill a non-existent input field.")


def click_submit_button(driver: WebDriver):
    """Locate and click the submit button."""
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//ids-button[@role='button'][contains(text(), 'Lägg till detta läkemedel')]"))
        )
        submit_button.click()
    except TimeoutException:
        print("Submit button not clickable or not found.")


def check_terms_checkbox(driver: WebDriver) -> bool:
    """
    Checks the 'terms and conditions' checkbox if it's not already checked.

    Args:
        driver (WebDriver): The WebDriver instance controlling the browser.

    Returns:
        bool: True if the checkbox is successfully checked, False otherwise.
    """
    try:
        checkbox = driver.find_element(By.ID, "terms-accepted")
        if not checkbox.is_selected():
            checkbox.click()
            print("Checkbox has been checked.")
        else:
            print("Checkbox was already checked.")
        return True
    except NoSuchElementException:
        print("Checkbox not found on the page.")
        return False
    except ElementClickInterceptedException:
        print("Checkbox could not be clicked. It might be hidden or obstructed.")
        return False


def wait_for_bankid_authentication(driver: WebDriver, expected_text: str, threshold: float = 0.8) -> bool:
    """
    Waits for the user to complete the BankID authentication process by checking specific elements for a fuzzy text match.

    Args:
        driver (WebDriver): The WebDriver instance controlling the browser.
        expected_text (str): The text expected to be found on the page after successful login.
        threshold (float): The similarity ratio threshold for a match.

    Returns:
        bool: True if the expected text is found within the timeout, False otherwise.
    """
    timeout = 300  # 5 minutes timeout
    check_interval = 5  # check every 5 seconds
    start_time = time.time()

    while time.time() - start_time < timeout:
        # Target specific elements like headers or paragraphs in a specific section
        elements = driver.find_elements(By.XPATH, "//h2 | //h3 | //p | //div[contains(@class,'important-info')]")
        normalized_expected_text = normalize_text(expected_text)

        for element in elements:
            normalized_element_text = normalize_text(element.text)
            ratio = difflib.SequenceMatcher(None, normalized_expected_text, normalized_element_text).ratio()
            if ratio >= threshold:
                print("Login successful, continuing with script.")
                return True

        print("Still waiting for authentication...")
        time.sleep(check_interval)

    print("Timeout waiting for BankID authentication.")
    return False


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    browser = webdriver.Chrome(options=options)
    browser.get(LINK_ADDRESS)

    if wait_for_bankid_authentication(browser, "Läkemedel som du vill förnya"):
        for medication in medications:

            name_input = robust_find_input_by_label("Läkemedlets namn", browser)
            fill_input_field(name_input, medication.name)

            form_input = robust_find_input_by_label("Beredningsform", browser)
            fill_input_field(form_input, medication.form)

            strength_input = robust_find_input_by_label("Styrka", browser)
            fill_input_field(strength_input, medication.strength)

            dosage_input = robust_find_input_by_label("Dosering", browser)
            fill_input_field(dosage_input, medication.dosage)

            prescriber_input = robust_find_input_by_label("Läkaren som utfärdat receptet", browser)
            fill_input_field(prescriber_input, medication.prescriber)

            click_submit_button(browser)
            print(f"Added {medication.name}.")
            time.sleep(0.5)  # dont make this less than 0.3, otherwise 1177 gets very angry
    else:
        print("Could not verify user login, aborting script.")

    input("All medications added. Press Enter to finish and close the browser.")
    browser.quit()


if __name__ == "__main__":
    main()
