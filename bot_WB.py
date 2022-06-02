from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import telebot

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")


def scrol():
    """ Пролистать страницу вниз """
    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def pars(drivers, x):
    """ Парсинг нужных комментариев """

    requiredHtml = drivers.page_source
    soup = bs(requiredHtml, "html5lib")
    soup = soup.findAll('li', class_='comments__item feedback')
    for comments in soup:
        temp = []
        if comments.find('span', class_='feedback__rating stars-line star' + str(x)) is not None:
            temp = comments.text
            temp = " ".join(temp.split())
            temp = temp[:temp.find(',') + 7] + ' ' + temp[temp.rfind('Цвет:'):-35]
            if 'Сегодня' in temp:
                send_telegram(temp)

def send_telegram(text: str):
    """ Отправка комментариев в телеграм канал """
    bot = telebot.TeleBot('5301069444:AAFRT7o9Uue5J_BOP8-d6gYac2Cv0TdQKB0')
    CHANNEL_NAME = '@wb_test_sma'
    bot.send_message(CHANNEL_NAME, text)



with open('1.txt', 'r', encoding='utf-8') as f:
    list_product = []
    for i in f:
        list_product.append(i[:8])

driver = webdriver.Chrome()
for i in list_product:
    URL_TEMPLATE = "https://www.wildberries.ru/catalog/" + i + "/detail.aspx"
    driver.get(URL_TEMPLATE)
    scrol()
    for item in range(1, 3):
        pars(driver, item)
