from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


class LoginTest(LiveServerTestCase):

    def test_01(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('http://127.0.0.1:8000/')
        assert "Bootstrap demo" in driver.title

    def test_02(self):
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('http://127.0.0.1:8000/users/login')
        username = driver.find_element(by='id', value='username')
        password = driver.find_element(by='id', value='password')
        submit = driver.find_element(by='id', value='submit')

        username.send_keys('hp')
        password.send_keys('1234')
        submit.send_keys(Keys.ENTER)
        time.sleep(1)
        assert "login" not in driver.page_source
