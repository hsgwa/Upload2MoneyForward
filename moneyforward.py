# coding: UTF-8

from time import sleep

import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# from selenium.webdriver.common.keys import Keys


class WebController():
    def __init__(self, username, password):
        from selenium import webdriver
        import os

        self.__username = username
        self.__password = password
        chromeOptions = webdriver.ChromeOptions()
        script_path = os.path.dirname(os.path.abspath(__file__))
        prefs = {"download.default_directory": script_path + "/download"}
        chromeOptions.add_experimental_option("prefs", prefs)
        self.__driver = webdriver.Chrome(chrome_options=chromeOptions)
        self.__driver.implicitly_wait(10)

    def __del__(self):
        self.__driver.quit()

    def login(self):
        self.__driver.get("https://moneyforward.com/users/sign_in")
        elem = self.__driver.find_element_by_id(
            "sign_in_session_service_email")
        elem.clear()
        elem.send_keys(self.__username)
        elem = self.__driver.find_element_by_id(
            "sign_in_session_service_password")
        elem.clear()
        elem.send_keys(self.__password)
        elem = self.__driver.find_element_by_id("login-btn-sumit")
        elem.click()

    def open_payment(self):
        self.__driver.get("https://moneyforward.com/cf#cf_new")
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.ID, "submit-button")))

    def open_history(self):
        self.__driver.get("https://moneyforward.com/bs/history")
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.ID, "bs-history")))

    def open_next_payment(self):
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.ID, "confirmation-button")))
        elem = self.__driver.find_element_by_id("confirmation-button")
        elem.click()

    def open_plus_payment(self):
        self.__driver.find_element_by_class_name("plus-payment").click()

    def fill_content(self, content):
        elem = self.__driver.find_element_by_id("js-content-field")
        elem.clear()
        elem.send_keys(content)

    def fill_payment(self, price):
        if price == 0:
            raise ValueError("paiment is zero.")

        if price > 0:
            elem = self.__driver.find_element_by_class_name(
                "plus-payment").click()
        else:
            elem = self.__driver.find_element_by_class_name(
                "minus-payment").click()

        elem = self.__driver.find_element_by_id("appendedPrependedInput")
        elem.clear()
        elem.send_keys(abs(price))

    def save_payment(self):
        self.__driver.find_element_by_id("submit-button").click()

    def fill_date(self, date):
        elem = self.__driver.find_element_by_id("updated-at")
        elem.clear()
        elem.send_keys(date)

    def select_large_category(self, category):
        elem = self.__driver.find_element_by_id(
            "js-large-category-selected").click()
        elem = self.__driver.find_element_by_xpath("//a[text()='" + category +
                                                   "' and @class='l_c_name']")
        elem.click()

    def select_middle_category(self, category):
        elem = self.__driver.find_element_by_id(
            "js-middle-category-selected").click()
        elem = self.__driver.find_element_by_xpath("//a[text()='" + category +
                                                   "' and @class='m_c_name']")
        elem.click()

    def downloadMonthHistory(self):
        download_elem = self.__driver.find_element_by_xpath(
            '//div[@id="main-container"]//a[contains(text(), "CSV")]')
        self.__driver.get(download_elem.get_attribute("href"))

    def getHistoryCSV(self):
        self.open_history()
        self.__driver.get("https://moneyforward.com/bs/history/csv")

        elems = self.__driver.find_elements_by_xpath(
            '//div[@id="bs-history"]//table//a[contains(@href, "monthly")]')
        for elem in elems:
            sleep(1)
            href = elem.get_attribute("href") + "/csv"
            print(href)
            self.__driver.get(href)

    def getPaymentCSV(self):
        self.__driver.get("https://moneyforward.com/cf")
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.ID, "kakeibo")))

        elems = self.__driver.find_elements_by_xpath(
            '//section[@id="kakeibo"]' +
            '//div[@class="year-month-dropdown"]' + '//li[@data-month!=""]')

        for elem in elems:
            sleep(1)
            year = int(elem.get_attribute("data-year"))
            month = int(elem.get_attribute("data-month"))
            href = "https://moneyforward.com/cf/csv" + \
                "?from={0}%2F{1:02}%2F01&month={1}&year={0}".format(year, month)
            self.__driver.get(href)


def doUpload(input_file):
    import os
    from time import sleep
    import pandas as pd
    from dotenv import load_dotenv
    load_dotenv()

    user = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")

    if user is None:
        print('USERNAME is not set.\n'
              'Please create .env file to set login info.')
        return
    else:
        print("USERNAME : {}".format(user))

    if password is None:
        print('PASSWORD is not set.\n'
              'Please create .env file to set login info.')
        return
    else:
        print("PASSWORD : {}".format("*" * len(password)))

    controller = WebController(user, password)
    df = pd.read_csv(input_file)

    controller.login()
    controller.open_payment()

    for count, row in df.iterrows():
        controller.fill_date(row['日付'])
        controller.fill_payment(int(row['金額']))
        controller.select_large_category(row['大分類'])
        controller.select_middle_category(row['中分類'])
        controller.fill_content(row['備考'])
        sleep(2)
        controller.save_payment()

        if count < len(df):
            controller.open_next_payment()

    return 1


def doDownload(input_file):
    import os
    from time import sleep
    # import pandas as pd
    from dotenv import load_dotenv
    load_dotenv()

    user = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")

    if user is None:
        print('USERNAME is not set.\n'
              'Please create .env file to set login info.')
        return
    else:
        print("USERNAME : {}".format(user))

    if password is None:
        print('PASSWORD is not set.\n'
              'Please create .env file to set login info.')
        return
    else:
        print("PASSWORD : {}".format("*" * len(password)))

    controller = WebController(user, password)

    controller.login()
    controller.getHistoryCSV()


def doPaymentDownload(input_file):
    import os
    from time import sleep
    # import pandas as pd
    from dotenv import load_dotenv
    load_dotenv()

    user = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")

    if user is None:
        print('USERNAME is not set.\n'
              'Please create .env file to set login info.')
        return
    else:
        print("USERNAME : {}".format(user))

    if password is None:
        print('PASSWORD is not set.\n'
              'Please create .env file to set login info.')
        return
    else:
        print("PASSWORD : {}".format("*" * len(password)))

    controller = WebController(user, password)

    controller.login()
    controller.getPaymentCSV()


if __name__ == '__main__':
    import sys
    # if len(sys.argv) != 2:
    #     print("No input_file!")
    #     print("usage: python uploadCSVtoMF.py input_data.csv")
    #     sys.exit()
    # input_file = str(sys.argv[1])
    # sys.exit(doUpload(input_file))
    sys.exit(doDownload(""))
    # sys.exit(doPaymentDownload(""))
