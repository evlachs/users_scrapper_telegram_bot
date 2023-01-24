import os
from enum import Enum

BOT_TOKEN = os.getenv('BOT_TOKEN')

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

# UsersScrapper settings
ALL_IMPORTED_USERS_FNAME = 'importing_users_hist.csv'  # all 'scrapped' users data csv-fname: users and chat IDs & timestamp
SAVE_HIST_DATA = bool(
    ALL_IMPORTED_USERS_FNAME)  # do save all 'scrapped' users data - True is ALL_IMPORTED_USERS_FNAME is set.


class TG_MSGS(Enum):
    """ Telegram messages for handling them in exceptions and other cases """
    USER_NOT_ALLOWED_TO_ADD = (
        "The user's privacy settings do not allow you to do this (caused by InviteToChannelRequest)",)


# UsersScrapper settings
SETTING_CSV = 'data/scrapping_settings.csv'
