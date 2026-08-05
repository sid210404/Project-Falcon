from datetime import datetime, timedelta

from app.broker.kite_client import KiteBroker


class MarketData:
    def __init__(self):
        self.broker = KiteBroker()

    def historical_data(self, instrument_token, interval="5minute", days=30):
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days)

        return self.broker.kite.historical_data(
            instrument_token=instrument_token,
            from_date=from_date,
            to_date=to_date,
            interval=interval,
        )