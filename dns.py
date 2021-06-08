from selenium.webdriver import Chrome, ChromeOptions
import time
from random import randint

# task settings
keys = ['city', 'tel', 'mail', 'shop', 'cardNubmer', 'cardMonth', 'cardYear', 'cardCVV']

options = dict()

file = open('Input/input.txt', 'r', encoding='utf8')

for key in keys:
    options[key] = file.readline().strip()

LINK = 'https://www.dns-shop.ru/'

# browser settings
option = ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
driver = Chrome(r'Driver/chromedriver.exe', options=option)

def smartClick(xpath):
    while True:
        try:
            elem = driver.find_element_by_xpath(xpath)
            elem.click()
            break
        except:
            pass

def enter(xpath, key):
    while True:
        try:
            inp = driver.find_element_by_xpath(xpath)
            break
        except:
            pass
    for char in key:
        inp.send_keys(char)
        time.sleep(randint(1,10)/10)
    return inp

def authorisation():
    pass

def scroll():
    driver.find_element_by_css_selector('body').send_keys(Keys.DOWN)

def startBot():
    driver.get(LINK)
    time.sleep(3)
    # choose town
    driver.execute_script("document.querySelector('.w-choose-city-widget-label').click()")

    while True:
        try:
            enter("//input[@data-role = 'search-city']", options['city']).send_keys('\n')
            break
        except:
            driver.execute_script("document.querySelector('.w-choose-city-widget-label').click()")
            driver.refresh()
    
    # выбор категории комплектующие
    smartClick("//a[contains(text(), 'комплектующие')]")
    
    # выбор категории видеокарты
    smartClick("//span[contains(text(), 'Видеокарты')]")

    # выбор видеокарты
    smartClick("//span[contains(text(), 'GeForce 210')]/../following-sibling::div[@class='product-buy product-buy_one-line catalog-product__buy']/child::button[contains(text(), 'Купить')]")

    # переход в корзину
    driver.get('https://www.dns-shop.ru/order/begin/')

    while True:
        try:
            # нажатие оформить заказ
            confirm = driver.find_element_by_xpath("//button[contains(text(), 'Оформить заказ')]")
            confirm.click()
            break
        except:
            driver.refresh()


    

    # ввод телефона
    enter("//label[contains(text(), 'Телефон')]/preceding-sibling::input", options['tel'])
    
    # ввод почты
    enter("//label[contains(text(), 'E-mail')]/preceding-sibling::input", options['mail'])

    # выбор магазина
    driver.find_element_by_xpath("//div[contains(text(), 'Изменить магазин')]").click()
    enter("//input[contains(@placeholder, 'Поиск')]", 'shop')
    smartClick("//div[contains(text(), 'Выбрать')]")

    time.sleep(0.5)

    # покупка
    smartClick("//div[contains(text(), 'Подтвердить заказ')]")

    # подтверждение телефона
    code = input('Код из смс')
    enter("//label[contains(text(), 'Код')]/preceding-sibling::input", code)
    smartClick("//div[contains(text(), 'Подтвердить')]")

    def cardEnter():
        enter("//input[@id='cardNumber']", options['cardNumber'])   
        enter("//input[@name='skr_month']", options['cardMonth'])   
        enter("//input[@name='skr_year']", options['cardYear'])   
        enter("//input[@name='skr_cardCvc']", options['cardCVV'])   
        smartClick("//span[contains(text(), 'Заплатить')]")

startBot()

