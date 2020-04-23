import traceback
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from twilio.rest import Client

from config import *


def print_step(msg):
    print(f'🥕 {msg}')


def notify(msg):
    print_step('Sending text message')
    print(msg)
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_TOKEN)
    twilio_client.messages.create(
        body=msg,
        from_=TWILIO_PHONE_NUMBER,
        to=RECEIVE_NOTIFICATION_PHONE_NUMBER
    )


def get_driver():
    chrome_options = Options()
    if DEBUG:
        chrome_options.add_argument('--headless')
    return webdriver.Chrome(CHROME_DRIVER, options=chrome_options)


def buy_it(driver):
    print(f'=========== {datetime.now()} ===========')

    print_step('Going to product page')
    driver.get(PRODUCT_URL)
    add_to_cart_button = driver.find_element_by_class_name('addToCartButton')

    if add_to_cart_button.is_displayed() & add_to_cart_button.is_enabled():
        
        print_step('Adding and going to cart')
        add_to_cart_button.click()
        basket_icon = driver.find_element_by_class_name('basketIcon_30LAG')
        basket_icon.click()

        print_step('Going to checkout')
        checkout_link = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[data-automation=continue-to-checkout]')
            )
        )
        checkout_link = checkout_link.get_attribute('href')
        driver.get(checkout_link)

        print_step('Using guest checkout')
        guest_continue = driver.find_element_by_class_name('guest-continue-link')
        guest_continue.click()

        print_step('Filling out shipping/billing info')
        email_field = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, 'email'))
        )
        email_field.send_keys(EMAIL)
        firstname_field = driver.find_element_by_id('firstName')
        firstname_field.send_keys(FIRSTNAME)
        lastname_field = driver.find_element_by_id('lastName')
        lastname_field.send_keys(LASTNAME)
        address_field = driver.find_element_by_id('addressLine')
        address_field.send_keys(ADDRESS)
        city_field = driver.find_element_by_id('city')
        city_field.send_keys(CITY)
        province_field = Select(driver.find_element_by_id('regionCode'))
        province_field.select_by_visible_text(PROVINCE)
        postal_field = driver.find_element_by_id('postalCode')
        postal_field.clear()
        postal_field.send_keys(POSTAL)
        phone_field = driver.find_element_by_id('phone')
        phone_field.send_keys(PHONE)

        print_step('Going to payment')
        continue_to_payment = driver.find_element_by_css_selector(
            'button[data-automation=continue-to-payment]'
        )
        continue_to_payment.click()

        print_step('Adding gift card')
        WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located((By.ID, 'shownCardNumber'))
        ).click()
        gift_card = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "//button[@class='toggle with-icon']")
            )
        )
        gift_card.click()
        gift_card_num = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, '//input[@id=\'giftcard_number\']')
            )
        )
        gift_card_num.send_keys(GIFT_CARD_NUMBER)
        gift_card_pin = driver.find_element_by_xpath('//input[@id=\'giftcard_pin\']')
        gift_card_pin.send_keys(GIFT_CARD_PIN)
        apply_gift_card = driver.find_element_by_css_selector(
            'button[data-automation=gift-card-apply]'
        )
        apply_gift_card.click()

        print_step('Reviewing and placing order')
        WebDriverWait(driver, 5).until(
            expected_conditions.invisibility_of_element((By.ID, 'shownCardNumber'))
        )
        review_order = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, 'button[data-automation=review-order]')
            )
        )
        review_order.click()
        place_order = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'order-now'))
        )
        if DEBUG:
            print_step(f'Clicking {place_order.text}')
        else:
            place_order.click()

        notify('🥳 Successfully bought Switch')
        return True

    else:
        print_step('Not available yet')
        return False


if __name__ == '__main__':

    start = """\
 _____________________________
< Animals are crossing !!!!!! >
 -----------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\\
                ||----w |
                ||     ||
"""
    print(start)

    driver = get_driver()

    count = 0
    while True:
        try:
            if buy_it(driver):
                break
        except Exception as e:
            count = count + 1
            msg = f'🤯 {count} times. Error occurred: {e}'
            traceback.print_exc()
            print_step('Restarting')
            notify(msg)
            if count == MAX_RETRY_BACKOFF:
                break

    driver.close()
