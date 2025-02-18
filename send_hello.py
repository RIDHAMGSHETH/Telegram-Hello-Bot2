import requests
import re
import logging

# Telegram bot credentials
BOT_TOKEN = '7962123741:AAH7S6OqmR89-kHqhtCFPPmIE1oY_nDLG0c'
CHAT_ID = '-1002372608174'

logging.basicConfig(level=logging.INFO)

def get_announcements():
    url = "https://mu.ac.in/distance-open-learning"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error("Failed to fetch URL: %s", e)
        return "Failed to fetch announcements."

    html_text = response.text
    lines = html_text.splitlines()

    start_index = None
    for i, line in enumerate(lines):
        if "Important Announcements" in line:
            start_index = i
            break

    if start_index is None:
        return "No 'Important Announcements' found on the website."

    pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']([^"\']+)["\'][^>]*>(.*?)</a>'
    
    def ordinal(n):
        suffix = "th" if 11 <= n % 100 <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

    announcement_count = 1
    announcements = []
    
    for line in lines[start_index : start_index + 20]:
        matches = re.findall(pattern, line)
        for href, rel, text in matches:
            announcements.append(f"{ordinal(announcement_count)} Announcement:\n{rel} > {text}\n🔗 {href}")
            announcement_count += 1

    return "\n\n".join(announcements) if announcements else "No announcements found."

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }

    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        logging.error(f"Error sending message: {response.text}")

if __name__ == "__main__":
    announcements = get_announcements()
    send_telegram_message(announcements)
