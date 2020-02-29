# coding: UTF-8

class WebController():
    import chromedriver_binary
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__driver = webdriver.Chrome()
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
        element = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.ID, "submit-button")))

    def open_next_payment(self):
        element = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.ID, "confirmation-button")))
        elem = self.__driver.find_element_by_id("confirmation-button")
        elem.click()

    def open_plus_payment(self):
        elem = self.__driver.find_element_by_class_name("plus-payment").click()

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
        elem = self.__driver.find_element_by_id("submit-button").click()

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


def doUpload(input_file):
    import os
    from time import sleep
    import pandas as pd
    from dotenv import load_dotenv
    load_dotenv()

    user = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")

    print("USERNAME")
    print(user, password)

    if user == None:
        print('USERNAME is not set. Please create .env file to set login info.')
        return
    else:
        print("USERNAME : {}".format(user))

    if password == None:
        print('PASSWORD is not set. Please create .env file to set login info.')
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


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("No input_file!")
        print("usage: python uploadCSVtoMF.py input_data.csv")
        sys.exit()
    input_file = str(sys.argv[1])
    sys.exit(doUpload(input_file))
