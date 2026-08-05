from kiteconnect import KiteConnect
from app.core.settings import settings


class KiteBroker:
    def __init__(self):
        self.kite = KiteConnect(api_key=settings.API_KEY)

        if settings.ACCESS_TOKEN:
            self.kite.set_access_token(settings.ACCESS_TOKEN)

    def login_url(self):
        return self.kite.login_url()

    def set_access_token(self, access_token):
        self.kite.set_access_token(access_token)

    def generate_session(self, request_token):
        session = self.kite.generate_session(
            request_token,
            api_secret=settings.API_SECRET
        )

        access_token = session["access_token"]

        self.kite.set_access_token(access_token)

        return access_token

    def profile(self):
        return self.kite.profile()