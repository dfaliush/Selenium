# -*- coding: utf-8 -*-
# import os
from selenium import webdriver
import time
# екземпляр класса, с указанием пути к файлу драйвера
driver = webdriver.Chrome(executable_path="/home/dmitriy/git/work/selenium/chromedriver")

# Метод get. для ввода запрашиваемой строки в строку браузера
driver.get('http://www.google.com')

# Переменная, которая находит строку поиска на сайте Google. Поиск происходит по названию Класса, и ИД элемента
seqrch_str = driver.find_element_by_xpath("//input[@id='lst-ib']")

# Что будем искать в поисковике
seqrch_element = "xpath"

# Ввод текста в строку через send_keys
seqrch_str.send_keys(seqrch_element)

# Поиск и нажатие кнопки поиска
driver.find_element_by_xpath("//button[@type='submit']").click()

# Поиск элемента в списке ответов google. Задердка на загрузку страници
time.sleep(1)
driver.find_element_by_link_text("XPath Tutorial - W3Schools").click()
print driver.title

