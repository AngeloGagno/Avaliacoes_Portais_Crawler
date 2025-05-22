from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cookies.driver import Driver
from dotenv import load_dotenv
import os
import time
class Login:
    def __init__(self, driver: Driver):
        """Instancia a classe para realizar o login no site da avantio"""
        load_dotenv(override=True)
        self.driver = driver
        self.connecting_page()
        self.username()
        self.password()

    def connecting_page(self):
        """Acessa a página da Pineapples"""
        try:
            self.driver.get('https://app.pineapples.com.br/')
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'user_name'))
            )
        except Exception as e:
            raise RuntimeError("Falha ao acessar a página de login.") from e

    def username(self):
        """Fornece a credencial usuário"""
        try:
            username_field = self.driver.find_element(By.ID, 'user_name')
            username_field.send_keys(os.getenv('user_name'))
        except Exception as e:
            raise RuntimeError("Falha ao preencher o usuário.") from e

    def password(self):
        """Fornece as credenciais senha"""
        try:
            password_field = self.driver.find_element(By.ID, 'user_password')
            password_field.send_keys(os.getenv('user_password'))

            self.driver.find_element(By.ID, 'login_button').click()
            WebDriverWait(self.driver, 20).until(
                EC.url_changes("https://app.pineapples.com.br")
            )
            
        except Exception as e:
            raise RuntimeError("Falha ao preencher a senha ou fazer login.") from e

    def get_cookies(self):
        self.driver.get('https://app.pineapples.com.br/channelmanager/dashboard')
        time.sleep(10)
        avantio_cookies = self.driver.get_cookies()
        cookies = {cookie['name']: cookie['value'] for cookie in avantio_cookies}
        self.driver.quit()
        return cookies