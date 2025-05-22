import pyotp 
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from cookies.driver import Driver
import os

class TwoFactorAuthenticator:
    def __init__(self, driver:Driver):
        self.driver = driver
        load_dotenv(override=True)
        self.secret_key = os.getenv('AuthKey')

    def authenticator_number(self):
        if not self.secret_key:
            raise ValueError("Secret key não encontrada nas variáveis de ambiente!") 
        
        totp = pyotp.TOTP(self.secret_key)
        code = totp.now()
        return code

    def check_page(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'buttonSendOtpToken'))
            )
            return True
        except:
            return False

    def place_auth_code(self):
        code = self.authenticator_number()

        input_field = self.driver.find_element(By.ID, 'otpToken')
        input_field.send_keys(code)

    def click_button(self):
        btn = self.driver.find_element(By.ID, 'buttonSendOtpToken')
        btn.click()


    def run_2fa(self):
        if self.check_page():
            self.place_auth_code()
            self.click_button()
