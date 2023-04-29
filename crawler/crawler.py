import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()


class Crawler:
    """A class that serves as a crawler for Health Declaration."""
    def __init__(self):
        self.chrome_binary = os.environ.get("CHROME_WEB_BINARY")
        self.chrome_webdriver = Service(os.environ.get("CHROME_WEBDRIVER"))
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.binary_location = self.chrome_binary
        self.driver = webdriver.Chrome(service=self.chrome_webdriver,
                                       options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    async def login(self, student_number, password):
        """Handles the authentication to the website."""

        # Get the necessary elements
        self.driver.get(os.environ.get("HD_LINK"))
        student_no_input = self.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "student-no-input")))
        password_input = self.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "student-password-input")))
        search_button = self.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "search-btn")))

        # Input the credentials and submit
        student_no_input.send_keys(student_number)
        password_input.send_keys(password)
        search_button.click()

    async def fillup(self, studID: str, password: str):
        """Answers the health declaration form"""

        # Handle login first
        await self.login(studID, password)

        # Just put the password after login to suppress HTML check
        password_input = self.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "student-password-input")))
        password_input.send_keys(password)

        # find the "Fill-up Health Declaration" button and click it
        health_decl_button = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button.btn.btn-primary.expand-btn')))
        health_decl_button.click()

        # wait for the health declaration modal to appear
        modCont = "div.modal-content"
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, modCont))
        )

        # fill up the form
        q0_yes = self.wait.until(EC.visibility_of_element_located(
            (By.ID, "q0yes")))
        q1_no = self.wait.until(EC.visibility_of_element_located(
            (By.ID, "q1no")))
        q2_no = self.wait.until(EC.visibility_of_element_located(
            (By.ID, "q2no")))
        q3_no = self.wait.until(EC.visibility_of_element_located(
            (By.ID, "q3no")))

        q0_yes.click()
        q1_no.click()
        q2_no.click()
        q3_no.click()

        # submit the form
        submitBtn = "//button[@class='btn btn-primary' and @name='save']"
        submit_button = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, submitBtn)))
        submit_button.click()

        # screenshot the Health Declaration
        WebDriverWait(self.driver, 10)
        self.driver.save_screenshot(f"{studID}_plmhd.png")

    async def quit(self):
        """A function that force quit the webdriver."""
        self.driver.quit()
