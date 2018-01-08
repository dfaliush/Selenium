#!/usr/bin/env python3
""" Скрипт для удаления недавно добавленных друзей с фейсбука
"""

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.chrome.options import Options
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

# Линк на профиль в ФБ
link = "https://www.facebook.com/profile.php?id=ЗдесьДлинныйНомер"

browser.maximize_window()
browser.get(link)

# Заполнение полей формы регистрации и вход в систему
browser.find_element_by_xpath("//*[@id=\"email\"]").send_keys(login)
browser.find_element_by_xpath("//*[@id=\"pass\"]").send_keys(passwd)
browser.find_element_by_xpath("//*[@id=\"loginbutton\"]").click()

# Переход на вкладку "Профіль"
Wait(browser, 10).until(
    ec.element_to_be_clickable((By.XPATH, "//*/span[contains(@class, '_1vp5')]"))).click()

# Переход на вкладку "Друзі"
Wait(browser, 10).until(
    ec.element_to_be_clickable((By.XPATH, "//*/a[contains(@data-tab-key, 'friends')]"))).click()

# Переход на вкладку "Нещодавно додані"
Wait(browser, 10).until(
    ec.element_to_be_clickable((By.XPATH, "//*/span[contains(text(), 'Нещодавно додані')]"))).click()

# Поиск количества видимых елементов. Кнопка с галочкой  "Друзі". В выборку попадает 20 видимых элементов с
all_users = browser.find_elements_by_xpath("//*/span[contains(text(), 'Друзі')]")
len_all_users = all_users.__len__()


count = 20
removed_friends = 0

while count < len_all_users + 50:

    for i in all_users:
        # Поиск элемента из списка по индексу.
        sleep(1)
        browser.find_elements_by_xpath("//*/span[contains(@class, '_55pe')]/span[contains(text(), 'Друзі')]")[count]\
            .click()
        sleep(2)
        # Нажатие на кнопку "Видалити з друзів"
        browser.find_element_by_xpath("//a/span[contains(text(), 'Видалити із друзів')]").click()

        count += 1
        removed_friends += 1
print(removed_friends)

#  # Поиск элемента из списка по индексу.
# Wait(browser, 10).until(
#     ec.element_to_be_clickable((By.XPATH, "//*/span[contains(text(), 'Друзі')]")))
# # Нажатие на кнопку "Видалити з друзів"
# Wait(browser, 10).until(
#     ec.element_to_be_clickable((By.XPATH, "//a[span[text()[contains(., 'Видалити із друзів')]]]"))).click()
