# -*- coding: utf-8 -*-
import time
from selenium import webdriver

""" Скрипт для проверки наличия мест в вагоне поезда. """

# Обозначение станций, откуда-куда
station_from = u"Київ"
station_till = u"Ковель"
# Дата отправляения #or datetime.year
tr_year = 2017
tr_month_0 = 2     # Где 12 - номер месяца.
tr_month_1 = str(tr_month_0).zfill(2)
tr_month = int(tr_month_0) - 1
tr_day = 3
tr_day_1 = str(tr_day).zfill(2)


# Номер поезда
tr_num_consist = '097'
# Тип места
type_vagon = "Плацкарт"

# екземпляр класса, с указанием пути к файлу драйвера
driver = webdriver.Chrome(executable_path="/home/dmitriy/git/work/selenium/chromedriver")

# Метод get. для ввода запрашиваемой строки в строку браузера
driver.get('http://www.google.com')

# Переменная, которая находит строку поиска на сайте Google. Поиск происходит по названию Класса, и ИД элемента
seqrch_str = driver.find_element_by_xpath("//input[@id='lst-ib']")

# Что будем искать в поисковике
seqrch_element = u"покупка жд билетов"

# Ввод текста в строку через send_keys
seqrch_str.send_keys(seqrch_element)

# Поиск и нажатие кнопки поиска в Гуглле
driver.find_element_by_xpath("//button[@type='submit']").click()

# Поиск элемента в списке ответов google. Задердка на загрузку страници
time.sleep(1)
driver.find_element_by_link_text(u"Онлайн резервування та придбання квиткiв - Укрзалізниця: Покупка").click()


# Поле ввода, откуда.  Запись в поле "откуда", названия станции.
time.sleep(1)
field_from = driver.find_element_by_xpath("//input[@name='station_from']")
field_from.send_keys(station_from)
time.sleep(1)
field_from.find_element_by_xpath("//div[@id='stations_from']/div[1]").click()
# assert город который выбран, совпадает с тем, что надо

# Поле ввода, куда. Запись в поле "куда", названия станции.
time.sleep(1)
field_till = driver.find_element_by_xpath("//input[@name='station_till']")
field_till.send_keys(station_till)
time.sleep(1)
field_from.find_element_by_xpath("//div[@id='stations_till']/div[1]").click()
# assert город который выбран, совпадает с тем, что надо

# Выбор развернутого календаря
driver.find_element_by_xpath("//input[@id='date_dep']").click()

# Выставление даты отправления. Пока-что дата задается в элементе
time.sleep(1)
driver.find_element_by_xpath("//td[@data-month={} and contains (@data-year, {})]/a[text()={}]".
                             format(tr_month, tr_year, tr_day)).click()

# Нажатие кнопки поиска поездов
time.sleep(1)
driver.find_element_by_xpath("//p/button[@name='search']").click()


# Если номер поезда содержит указанные цифры, выбираем "Плацкарт"
time.sleep(1)
pick_train = driver.find_element_by_xpath("//table[@id='ts_res_tbl']/tbody/tr/td/a[contains (text(), {})]"
                                          .format(tr_num_consist))
time.sleep(1)
pick_train.find_elements_by_xpath("../../td[6]/div[@title='{}']/button".format(type_vagon))[0].click()

# Проверка на совпадение заданой даты, с фактической(выбранной)
time.sleep(1)
trains_date_actual = driver.find_elements_by_xpath('html/body/div[7]/div[1]/div[2]')[0].text
trains_date_planned = u"{}.{}.{}".format(tr_day_1, tr_month_1, tr_year)

assert trains_date_planned == trains_date_actual

# Проверка названия поезда.
time.sleep(1)
train_number_full = driver.find_elements_by_xpath("/html/body/div[7]/div[1]/span/span[1]/strong")[0].text
assert tr_num_consist in train_number_full

# Поиск свободных мест в одном вагоне. Запись в список. Вывод по четным и нечетным
list_spaces = []
time.sleep(2)

# Получение списка доступных вагонов
list_cars_obj = driver.find_elements_by_xpath("//span/a[contains (@href, '#')]")   # [@href='#2']
z = len(list_cars_obj)
list_cars_num = []  # список вагонов
# Итерирование списка элементов(вагонов). Получение списка с номерами доступных вагонов
for i in xrange(z):
    # Выбор элемента из списка. Т.к. Элемент - строка, удалил перевод каретки. Убрал юникод
    list_cars_num.append(list_cars_obj[i].text[:2].replace('\n', '').encode('utf-8'))
print list_cars_num

# Словарь, котрый бедет наполнятся номерами вагонов и номерами свободных мест в этих вагонах
total_places = {}

# Итерирование по доступным вагонам, получение списка свободных мест
for vagon in list_cars_num:
    if driver.find_element_by_xpath("//span/a[@href='#{}']".format(vagon)):
        driver.find_element_by_xpath("//span/a[@href='#{}']".format(vagon)).click()
        time.sleep(1)
        list_free_places_obj = driver.find_elements_by_xpath("//div/div[contains (@class, 'place fr')]")
        y = len(list_free_places_obj)
        list_free_places = []

        for place in list_free_places_obj:
            # Выбор элемента из списка. Т.к. Элемент - строка, удалил перевод каретки. Убрал юникод
            list_free_places.append(place.get_attribute('place').encode('utf-8'))
        total_places[vagon] = list_free_places

print total_places
driver.close()
