import requests
import time
import re

BASE_URL = "https://www.ivasms.com"

EMAIL = "asmeralselwi103@gmail.com"
PASSWORD = "Mohammed Saeed 123"

BOT_TOKEN = "8325061391:AAESPAfQ93gf79feMa8YgRMCOgTSHxGnu40"
CHAT_ID = "-1003745034804"

session = requests.Session()


def login():

    r = session.get(BASE_URL + "/login")

    token = ""
    if 'name="_token"' in r.text:
        token = r.text.split('name="_token" value="')[1].split('"')[0]

    payload = {
        "email": EMAIL,
        "password": PASSWORD,
        "_token": token
    }

    r = session.post(BASE_URL + "/login", data=payload)

    return "/portal" in r.url


def get_sms():

    url = BASE_URL + "https://www.ivasms.com/portal/live/my_sms"

    r = session.get(url)

    return r.json()


def extract_otp(text):

    m = re.search(r'\d{4,6}', text)

    if m:
        return m.group()

    return None


def send_telegram(msg):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(url, data=data)


print("IVASMS BOT STARTED")

seen = set()

if login():

    while True:

        data = get_sms()

        for sms in data:

            number = sms.get("number", "")
            message = sms.get("sms", "")

            otp = extract_otp(message)

            if otp and otp not in seen:

                text = f"""
🚀 NEW OTP

📞 Number: {number}
🔑 Code: {otp}
"""

                send_telegram(text)

                print("OTP SENT:", otp)

                seen.add(otp)

        time.sleep(3)