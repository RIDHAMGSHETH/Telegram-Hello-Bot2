import requests

BOT_TOKEN = '7962123741:AAH7S6OqmR89-kHqhtCFPPmIE1oY_nDLG0c'
CHAT_ID = '1114692062'
MESSAGE = 'Hello!'

url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
payload = {
    'chat_id': CHAT_ID,
    'text': MESSAGE
}

response = requests.post(url, json=payload)

if response.status_code != 200:
    raise Exception(f"Error: {response.text}")
