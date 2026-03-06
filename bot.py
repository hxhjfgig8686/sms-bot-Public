import requests
import re
import time

BASE_URL = "https://www.ivasms.com"

EMAIL = "asmeralselwi103@gmail.com"
PASSWORD = "Mohammed Saeed 123"

BOT_TOKEN = "8325061391:AAESPAfQ93gf79feMa8YgRMCOgTSHxGnu40"
CHAT_ID = "-1003745034804"


def send_telegram(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    requests.post(url, data=data)


class IvaSMS:

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()

    def login(self):

        login_url = BASE_URL + "/login"

        r = self.session.get(login_url)

        token = ""
        if 'name="_token"' in r.text:
            token = r.text.split('name="_token" value="')[1].split('"')[0]

        payload = {
            "email": self.email,
            "password": self.password,
            "_token": token
        }

        r = self.session.post(login_url, data=payload)

        return "/portal" in r.url

    def get_sms(self):

        url = BASE_URL + "/portal/live/my_sms"

        r = self.session.get(url)

        return r.text


def extract_codes(text):

    return re.findall(r"\b\d{4,6}\b", text)


client = IvaSMS(EMAIL, PASSWORD)

if client.login():

    print("Login OK")

    seen = set()

    while True:

        sms = client.get_sms()

        codes = extract_codes(sms)

        for code in codes:

            if code not in seen:

                msg = f"OTP Code: {code}"

                print(msg)

                send_telegram(msg)

                seen.add(code)

        time.sleep(5)
