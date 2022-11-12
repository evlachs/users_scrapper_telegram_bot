from telethon.sync import TelegramClient

phone = '+phone'  # enter your number here starting with +
api_id = 00000000  # enter your api_id from the telegram application configuration
api_hash = 'api_hash'  # enter your api_hash from the telegram application configuration

client = TelegramClient(phone, api_id, api_hash)

client.start()
