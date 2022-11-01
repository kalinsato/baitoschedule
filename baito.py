from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime
import os
import codecs
import re


DRIVER_PATH="<path>"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)


driver.get('https://www.wa-aid.com/login')
time.sleep(3)

username = driver.find_element_by_name("username")
username.send_keys("<userID>")
password = driver.find_element_by_name("password")
password.send_keys("<password>")

def button_click(button_text):
    buttons = driver.find_elements_by_tag_name("button")

    for button in buttons:
        if button.text == button_text:
            button.click()
            break

button_click("ログイン")
time.sleep(5)
button_click("一覧")

D = driver.find_elements_by_class_name('rbc-agenda-content')
for i in D:
    a = i.text

lst = a.splitlines()

lst = [re.sub('\\(.*\\)', "", s) for s in lst]
lst = [re.sub('\\s—', "", s) for s in lst]
lst = [re.sub(':', " ", s) for s in lst]

print(lst)

with open('schedule.txt', encoding='utf-8', mode="w") as f:
    for i in lst:
        if not "休" in i:
            f.write("%s\n" % i[5:-10])

with open('schedule.txt', encoding='utf-8', mode="a") as f:
    f.write(str(datetime.date.today().year) + "." + str(datetime.date.today().month))
time.sleep(5)
