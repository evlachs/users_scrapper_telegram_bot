from telethon.sync import TelegramClient

phone = '+79287510802'  # enter your number here starting with +
api_id = 23902878  # enter your api_id from the telegram application configuration
api_hash = 'e801976015e40a922180114cfaa664f9'  # enter your api_hash from the telegram application configuration

client = TelegramClient(phone, api_id, api_hash)

client.start()
