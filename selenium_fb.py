#!/usr/bin/env python3
""" Скрипт для удаления отправленых запросов в друзья с фейсбука
"""

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from time import sleep

# Отключение всплывающих уведомлений
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-notifications")

# Экземпляр класса, с задаными параметрами
browser = webdriver.Chrome("/home/df/PycharmProjects/test_home/Selenium/chromedriver",
                           chrome_options=chrome_options)

# Данные для входа в учетную запись фб
login = "e-mail"
passwd = "password"

# Список отправленых запросов в друзья
browser.get('https://www.facebook.com/friends/requests/?fcref=none&outgoing=1')

# Заполнение полей формы регистрации и вход в систему
browser.find_element_by_xpath("//*[@id=\"email\"]").send_keys(login)
browser.find_element_by_xpath("//*[@id=\"pass\"]").send_keys(passwd)
browser.find_element_by_xpath("//*[@id=\"loginbutton\"]").click()

# Получение списка отправленых запросов. Изначальное количество = 10
all_users = browser.find_elements_by_xpath("//*/button[contains(@data-cancelref, 'outgoing_requests')]")

# Количество удаленных запросов в друзья. количество нажатий на "Переглянути більше запитів"
deleted_requests = 0
expand = 0

while expand < 20:

    # Если количество удаленных запросов = 10, нажать "Переглянути більше запитів"(expand)
    if deleted_requests > 9:

        # Обновить значение переменной all_users. После 10 удалений и експанда, количество отображаемых запросов + 10
        all_users = browser.find_elements_by_xpath("//*/button[contains(@data-cancelref, 'outgoing_requests')]")

        try:
            Wait(browser, 10).until(
                ec.element_to_be_clickable((By.XPATH, "//*/a[contains(text(), 'Переглянути більше запитів')]"))).click()
            expand += 1
            print("Количество получений большего количества запросов" + str(expand))
        except exceptions.TimeoutException:
            expand += 1
            print("Error" + str(expand))
            continue

    # Удаление запросов в друзья. Итерирование по списку елементов all_users
    for i in all_users:

        # Нажать на кнопку "Запит дружби надіслано"
        sleep(2)
        browser.find_elements_by_xpath("//*/button[contains(@data-cancelref, 'outgoing_requests')]")[deleted_requests]\
            .click()

        # Выбрать элемент из всплывающего списка, а именно "Скасувати запит".
        sleep(1)
        Wait(browser, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//a[span[text()[contains(., 'Скасувати запит')]]]"))).click()

        # Нажать на кнопку "Скасувати запит"(Подтверждение удаления)
        sleep(1)
        Wait(browser, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Скасувати запит')]"))).click()
        deleted_requests += 1

        # Стратегический слип =) Для избежания двойного прокликивания кнопки
        sleep(2)

print(deleted_requests)
