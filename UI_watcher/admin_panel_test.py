import time
import json
from selenium import webdriver


def get_links():
    with open("link.json") as json_file:
        data = json.load(json_file)
        return data


def selenium_worker(data):
    mistake = False
    driver = webdriver.Chrome()
    for i in range(len(data)):
        driver.get(str(data[i]))
        time.sleep(1)
        if driver.current_url != "https://admin.test.swapix.com/auth/login":
            print("Found hole", data[i])
            mistake = True
    if not mistake:
        print("Test passed with 0 errors")
        time.sleep(10)
    driver.quit()


selenium_worker(get_links())
