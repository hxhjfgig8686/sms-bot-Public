import requests
import time
import re
import json
import os

BASE_URL = "https://www.ivasms.com"

EMAIL = "asmeralselwi103@gmail.com"
PASSWORD = "Mohammed Saeed 123"

BOT_TOKEN = "8325061391:AAESPAfQ93gf79feMa8YgRMCOgTSHxGnu40"
CHAT_ID = "-1003745034804"

COOKIE_FILE = "session.json"

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
})


def save_session():

    with open(COOKIE_FILE, "w") as f:
        json.dump(session.cookies.get_dict(), f)


def load_session():

    if os.path.exists(COOKIE_FILE):

        with open(COOKIE_FILE, "r") as f:

            cookies = json.load(f)

            session.cookies.update(cookies)

            return True

    return False


def login():

    print("Login...")

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

    if "/portal" in r.url:

        print("Login successful")

        save_session()

        return True

    print("Login failed")

    return False


def get_sms():

    url = BASE_URL + "/portal/live/my_sms"

    r = session.get(url, timeout=20)

    try:
        return r.json()
    except:
        print("Not JSON:", r.text)
        return []


def extract_otp(text):

    m = re.search(r"\d{4,6}", text)

    if m:
        return m.group()

    return None


def send_telegram(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url, data=data)


print("IVASMS BOT STARTED")

if not load_session():

    login()

seen = set()

while True:

    try:

        sms_list = get_sms()

        for sms in sms_list:

            number = sms.get("number", "")
            message = sms.get("sms", "")

            otp = extract_otp(message)

            if otp:

                key = number + otp

                if key not in seen:

                    msg = f"""
🚀 NEW OTP

📞 Number: {number}
🔑 Code: {otp}
"""

                    send_telegram(msg)

                    print("OTP SENT:", otp)

                    seen.add(key)

    except Exception as e:

        print("ERROR:", e)

        login()

    time.sleep(3)