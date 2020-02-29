# coding: UTF-8
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import csv
import chromedriver_binary

def doUpload(input_file):
    from dotenv import load_dotenv
    import os
    load_dotenv()

    surl = "https://moneyforward.com/users/sign_in"
    iurl = "https://moneyforward.com/cf#cf_new"
    user = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    print(user, password)

    if user == None:
      print('USERNAME is not set. Please create .env file to set login info.')
      return

    if password == None:
      print('PASSWORD is not set. Please create .env file to set login info.')
      return

    try:
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        driver.get(surl)

        # login
        elem = driver.find_element_by_id("sign_in_session_service_email")
        elem.clear()
        elem.send_keys(user)
        elem = driver.find_element_by_id("sign_in_session_service_password")
        elem.clear()
        elem.send_keys(password)
        elem = driver.find_element_by_id("login-btn-sumit")
        elem.click()

        # open
        f = open(input_file, mode='r', encoding='utf-8')
        reader = csv.reader(f)
        count = 1
        driver.get(iurl)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "submit-button")))
        for row in reader:

            # header skip
            if count != 1:
                print(row)
                if int(row[4]) > 0:
                    # case of income
                    print("[" + str(count) + "] " + "case of income : ")
                    price = int(row[4])

                    elem = driver.find_element_by_class_name(
                        "plus-payment").click()

                elif int(row[4]) < 0:
                    # case of outgo
                    print("[" + str(count) + "] " + "case of outgo : ")
                    price = int(row[4])

                else:
                    print("[" + str(count) + "] " + "Error format : ")

                #input price info
                elem = driver.find_element_by_id("appendedPrependedInput")
                elem.clear()
                elem.send_keys(abs(int(row[4])))

                #input large-category info
                elem = driver.find_element_by_id(
                    "js-large-category-selected").click()
                sleep(1)
                elem = driver.find_element_by_xpath(
                    "//a[text()='" + row[1] +
                    "' and @class='l_c_name']").click()
                sleep(1)
                #input middle-category info
                elem = driver.find_element_by_id(
                    "js-middle-category-selected").click()
                sleep(1)
                elem = driver.find_element_by_xpath(
                    "//a[text()='" + row[2] +
                    "' and @class='m_c_name']").click()
                sleep(1)
                #input content-field info
                elem = driver.find_element_by_id("js-content-field")
                elem.clear()
                elem.send_keys(row[3])

                #input date info
                elem = driver.find_element_by_id("updated-at")
                elem.clear()
                elem.send_keys(row[0])

                #save
                elem = driver.find_element_by_id("submit-button").click()
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.ID, "confirmation-button")))
                elem = driver.find_element_by_id("confirmation-button").click()
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "submit-button")))
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "plus-payment")))

            count += 1
        f.close()
        print("End procedure of " + input_file)
        driver.quit()

    except ValueError:
        print("Oops! Some Error are occured.")

    return 1


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("No input_file!")
        print("usage: python uploadCSVtoMF.py input_data.csv")
        sys.exit()
    input_file = str(sys.argv[1])
    sys.exit(doUpload(input_file))
