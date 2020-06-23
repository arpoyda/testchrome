# -*- coding: utf-8 -*-

import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import zipfile
from selenium.webdriver.chrome.options import Options


class NikeProfileFiller:
    def __init__(self, task, use_proxy=False, webhooks=''):
        self.webhooks = webhooks
        self.task = task
        if use_proxy:
            self.browser = self.generate_driver()
        else:
            self.browser = webdriver.Chrome(chrome_options=webdriver.ChromeOptions(), desired_capabilities={'unicodeKeyboard': True})
        self.wait = WebDriverWait(self.browser, 20)

    @staticmethod
    def log(msg):
        print("[{}]: {}".format(datetime.now(), msg))

    def _send_to_element_click(self, element, value):
        self.browser.find_element_by_id(element).clear()
        self.browser.find_element_by_id(element).click()
        self.browser.find_element_by_id(element).send_keys(value)

    def _send_to_element(self, element, value):
        self.browser.find_element_by_id(element).clear()
        self.browser.find_element_by_id(element).send_keys(value)

    def _send_to_element_xpath(self, element, value):
        self.browser.find_element_by_xpath(element).clear()
        self.browser.find_element_by_xpath(element).click()
        self.browser.find_element_by_xpath(element).send_keys(value)

    def _send_to_element_delay(self, element, value):
        for c in value:
            self.browser.find_element_by_xpath(element).send_keys(c)
            time.sleep(0.1)

    def _fill_profile(self):
        self.browser.get(self.task["link"])

        soup = BeautifulSoup(self.browser.page_source, 'html5lib')
        pid = soup.findChildren('meta', attrs={'name': 'branch:deeplink:productId'})[0].get('content')
        atc = self.task['link'] + '?productId=' + pid + '&size=' + self.task['size']
        self.log(self.task['link'] + '?productId=' + pid + '&size=' + self.task['size'])

        self.browser.get(atc)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="email"]')))
        self.browser.find_element_by_xpath('//input[@type="email"]').click()
        self.browser.find_element_by_xpath('//input[@type="email"]').send_keys(self.task["email"])
        self.browser.find_element_by_xpath('//input[@type="password"]').click()
        self.browser.find_element_by_xpath('//input[@type="password"]').send_keys(self.task["password"])
        time.sleep(0.1)
        self.browser.find_element_by_class_name('nike-unite-submit-button.loginSubmit.nike-unite-component').click()

        self.wait.until(EC.element_to_be_clickable((By.ID, 'firstName')))
        self._send_to_element_click('firstName', self.task["profile"].firstName)
        self._send_to_element_click('middleName', self.task["profile"].middleName)
        self._send_to_element_click('lastName', self.task["profile"].lastName)
        self._send_to_element_click('addressLine1', self.task["profile"].addressLine)
        self._send_to_element_click('addressLine2', '')  # TODO
        self._send_to_element_click('city', self.task["profile"].city)
        self._send_to_element_click('postCode', self.task["profile"].postCode)
        self._send_to_element_xpath('//input[@placeholder="Номер телефона"]', self.task["profile"].telNumber)
        self._send_to_element_click('email', self.task["email"])
        self.browser.find_element_by_xpath('//button[contains(text(), "Сохранить и продолжить")]').click()

        self.wait.until(EC.element_to_be_clickable((By.ID, 'passportNumber')))
        self._send_to_element_click('passportNumber', self.task["profile"].passportNumber)
        self._send_to_element_click('passportIssueDate', self.task["profile"].passportIssueDate)
        self._send_to_element_click('issuingAuthority', self.task["profile"].issuingAuthority)
        self._send_to_element_click('innNumber', self.task["profile"].innNumber)
        self.browser.find_element_by_xpath('//button[contains(text(), " Продолжить ")]').click()

        time.sleep(1)
        self.browser.switch_to.frame(self.browser.find_element_by_xpath('//iframe[@title="payment"]'))
        self._send_to_element('cardNumber-input', self.task["profile"].cardNumber)
        self._send_to_element('cardExpiry-input', self.task["profile"].cardExpiry)
        self._send_to_element('cardCvc-input', self.task["profile"].cvv)

        self.browser.switch_to.default_content()
        self.browser.find_element_by_xpath('//button[contains(text(), " Продолжить ")]').click()

        if 'isChecked' not in self.browser.find_element_by_xpath(
                '//*[@id="checkout"]/esw-gdpr-consent/div/div/div[1]/label').get_attribute("class"):
            self.browser.find_element_by_xpath('//*[@id="checkout"]/esw-gdpr-consent/div/div/div[1]/label/span').click()
        time.sleep((datetime.strptime(self.task["time"], '%d.%m.%y %H:%M:%S.%f') - datetime.now()).total_seconds())
        self.browser.find_element_by_xpath('//button[contains(text(), " Отправить заказ ")]').click()

    def start(self):
        self._fill_profile()

    def create_proxyauth_extension(self, proxy_host, proxy_port,
                                   proxy_username, proxy_password,
                                   scheme='http', plugin_path=None):
        import string
        import zipfile

        if plugin_path is None:
            plugin_path = 'add_files\\proxy_auth_plugin.zip'

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = string.Template(
            """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                      singleProxy: {
                        scheme: "${scheme}",
                        host: "${host}",
                        port: parseInt(${port})
                      },
                      bypassList: ["foobar.com"]
                    }
                  };
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "${username}",
                        password: "${password}"
                    }
                };
            }
            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """
        ).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme,
        )
        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_path

    def generate_driver(self):
        proxyauth_plugin_path = self.create_proxyauth_extension(
            proxy_host=self.task["proxy"]["host"],
            proxy_port=self.task["proxy"]["port"],
            proxy_username=self.task["proxy"]["user"],
            proxy_password=self.task["proxy"]["pass"][:-1:]
        )

        co = Options()
        co.add_argument("--start-maximized")
        co.add_extension(proxyauth_plugin_path)

        return webdriver.Chrome(chrome_options=co, desired_capabilities={'unicodeKeyboard': True})

