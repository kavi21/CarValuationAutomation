from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ValuationPage:
    def __init__(self, driver):
        self.driver = driver
        self.reg_input = (By.XPATH, "//input[@id='vrm-input']")
        self.submit_button = (By.XPATH, "//button[.//span[text()='Value your car']]")
        self.make_model = (By.XPATH, "//h1[@class='HeroVehicle__title-FAmG']")
        self.vehicle_details = (By.XPATH, "//ul[@class='HeroVehicle__details-XpAI']/li")
        self.error_message = (
            By.XPATH,
            "//div[contains(text(),'Did we get the reg right?') or contains(text(),'is not a valid reg?')]",
        )

    def load(self, url):
        self.driver.get(url)

    def enter_registration(self, reg_number):
        reg_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.reg_input)
        )
        reg_field.clear()
        reg_field.send_keys(reg_number)

        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.submit_button)
        )
        submit_button.click()

    def get_valuation_details(self):
        try:
            # Wait for the make and model to be visible
            make_model_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.make_model)
            )
            make_model = make_model_element.text.strip()

            # Get other vehicle details (year, color, fuel type)
            details_elements = self.driver.find_elements(*self.vehicle_details)
            details = [el.text.strip() for el in details_elements]

            if len(details) < 4:
                return None

            return {
                "make_model": make_model,
                "year": details[0],
                "color": details[1],
                "body_type": details[2],
                "fuel_type": details[3],
            }
        except:
            return None

    def is_error_displayed(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message)
            )
            return True
        except:
            return False
