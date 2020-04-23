# Buy Nintendo Switch on BestBuy Canada

Scrappy (no pun intended) code to scrape and buy Nintendo Switch on Bestbuy using a BestBuy gift
card (reduced financial risk). Send notifications on success or failure via Twilio.

Install dependencies:

```sh
pip install selenium twilio
```

Add a `config.py` file:

```python
DEBUG = True # or False. If True, won't click buy.

CHROME_DRIVER = 'path/to/chromedriver'
MAX_RETRY_BACKOFF = 3 # Number of retries on exception

PRODUCT_URL = 'https://www.bestbuy.ca/en-ca/product/nintendo-switch-console-with-neon-red-blue-joy-con/13817625'

TWILIO_ACCOUNT_SID = 'TWILIO_ACCOUNT_SID'
TWILIO_TOKEN = 'TWILIO_TOKEN'
TWILIO_PHONE_NUMBER = 'TWILIO_PHONE_NUMBER'
RECEIVE_NOTIFICATION_PHONE_NUMBER = 'YOUR_PHONE_NUMBER'

EMAIL = ''
FIRSTNAME = ''
LASTNAME = ''
ADDRESS = ''
CITY = ''
PROVINCE = ''
POSTAL = ''
PHONE = ''

GIFT_CARD_NUMBER = '' # BestBuy gift card number
GIFT_CARD_PIN = '' # BestBuy gift card pin
```


Wait for your new Nintendo Switch:

```sh
python buy.py
```
