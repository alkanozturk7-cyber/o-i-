import os
import requests

USERNAME = "yorgunmermi53"
URL = f"https://x.com/{USERNAME}"

TWILIO_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_FROM = os.environ["TWILIO_FROM"]
TWILIO_TO = os.environ["TWILIO_TO"]

FLAG = "notified.txt"

BAD_PHRASES = [
    # EN
    "this account doesn’t exist", "this account doesn't exist",
    "account suspended", "suspended",
    # TR (yaklaşık)
    "bu hesap mevcut değil",
    "hesap askıya alındı", "askıya alındı",
    "hesap donduruldu", "donduruldu",
    # Genel duvarlar / giriş
    "/i/flow/login", "log in", "sign in", "giriş yap", "oturum aç",
    "something went wrong", "bir şeyler ters gitti",
]

def is_active():
    r = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
        allow_redirects=True
    )

    # Redirect ile login'e gitti mi?
    final_url = str(r.url).lower()
    if "/i/flow/login" in final_url or "login" in final_url:
        return False

    if r.status_code != 200:
        return False

    t = (r.text or "").lower()

    # kötü sinyaller
    for p in BAD_PHRASES:
        if p in t:
            return False

    # ekstra güvenlik: profil sayfasında genelde @username geçer
    if f"@{USERNAME.lower()}" not in t:
        return False

    return True

def send_sms(body):
    api = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"
    data = {"To": TWILIO_TO, "From": TWILIO_FROM, "Body": body}
    r = requests.post(api, data=data, auth=(TWILIO_SID, TWILIO_TOKEN))
    r.raise_for_status()

def main():
    if os.path.exists(FLAG):
        print("SMS already sent.")
        return

    if is_active():
        send_sms(f"X hesabı aktif görünüyor: @{USERNAME} ({URL})")
        with open(FLAG, "w") as f:
            f.write("sent\n")
        print("SMS sent.")
    else:
        print("Hesap aktif görünmüyor.")

if __name__ == "__main__":
    main()
