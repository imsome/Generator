from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
import config
import time
import os
from config import ReportHandler

# link = config.admin_url


class AdsApproval:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        self.browser = webdriver.Chrome(options=chrome_options)
        self.link = config.admin_url
        desktop_url = config.url[0:8] + "test:test@" + config.url[8:]
        self.desktop_url = desktop_url.replace("api", "desktop", 1)

    def start_approve_ads(self):
        ReportHandler.add_log("Approving adds", "Starting approver")
        try:
            self.browser.maximize_window()
            self.browser.get(self.desktop_url)
            self.browser.get(self.link)
            login_field = self.browser.find_element_by_css_selector('[id="loginform-email"]')
            password_field = self.browser.find_element_by_css_selector('[id="loginform-password"]')
            login_button = self.browser.find_element_by_css_selector('button[class="btn btn-success btn-block"]')
            login_field.send_keys("admin@mail.ru")
            password_field.send_keys("admin")
            login_button.click()
            time.sleep(2)
            return True
        finally:
            return False

    def approve_ads(self):
        for ad_id in config.queue:
            try:
                link = config.admin_url + "items/index/edit/{ad_id}".format(ad_id=ad_id)
                self.browser.get(link)
                time.sleep(0.5)
                confirm_button = self.browser.find_element_by_xpath("//button[text()='Confirmed            ']")
                save_button = self.browser.find_element_by_css_selector('input[type="submit"]')
                confirm_button.click()
                save_button.click()
                ReportHandler.add_log("Approving ads", "Ad with id {} approved".format(ad_id))
                config.queue.remove(ad_id)
            except:
                print("Can't do smth for ad {}".format(ad_id))
                config.queue.remove(ad_id)
                ReportHandler.add_error("Approving add", "Failed for id {}".format(ad_id))

    def finish_approval(self):
        self.browser.quit()
        ReportHandler.add_log("Approving add", "Finished")
