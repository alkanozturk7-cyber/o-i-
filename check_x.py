import os
import requests

# KONTROL EDİLECEK X HESABI
USERNAME = "yorgunmermi53"
URL = f"https://x.com/{USERNAME}"

TWILIO_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_FROM = os.environ["TWILIO_FROM"]
TWILIO_TO = os.environ["TWILIO_TO"]

FLAG = "notified.txt"

def is_active():
    r = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
        allow_redirects=True
    )

    if r.status_code != 200:
        return False

    t = r.text.lower()

    if "this account doesn’t exist" in t or "this account doesn't exist" in t:
        return False
    if "account suspended" in t:
        return False

    return True

def send_sms(body):
    api = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    data = {
        "To": TWILIO_TO,
        "From": TWILIO_FROM,
        "Body": body
    }
    r = requests.post(api, data=data, auth=(TWILIO_SID, TWILIO_TOKEN))
    r.raise_for_status()

def main():
    if os.path.exists(FLAG):
        print("SMS already sent.")
        return

    if is_active():
        send_sms(f"X hesabı aktif oldu: @{USERNAME} ({URL})")
        with open(FLAG, "w") as f:
            f.write("sent\n")
        print("SMS sent.")
    else:
        print("Hesap hala kapalı.")

if __name__ == "__main__":
    main()
