import instaloader
import requests
from config import Config

class InstagramBot:
    def __init__(self):
        self.L = instaloader.Instaloader()
        self.session = requests.Session()

    def login(self, username, password):
        try:
            self.L.login(username, password)
            return True
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            return "2FA"

    def get_2fa_code(self):
        return input("Enter 2FA code: ")

    def login_with_2fa(self, code):
        self.L.two_factor_login(code)

    def get_target_list(self, target_username, target_list):
        profile = instaloader.Profile.from_username(self.L.context, target_username)
        if target_list == "followers":
            return profile.get_followers()
        elif target_list == "following":
            return profile.get_followees()

    def send_message(self, recipient_username, message):
        profile = instaloader.Profile.from_username(self.L.context, recipient_username)
        self.session.headers.update({'user-agent': 'Mozilla/5.0'})
        url = f"https://i.instagram.com/api/v1/direct_v2/threads/broadcast/text/"
        data = {
            "recipient_users": f"[{profile.userid}]",
            "text": message,
            "client_context": "1234567890"
        }
        response = self.session.post(url, data=data)
        return response.status_code == 200
