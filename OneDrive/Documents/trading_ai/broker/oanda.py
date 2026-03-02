import time
from oandapyV20 import API
from oandapyV20.endpoints.pricing import PricingStream


class OandaBroker:
    def __init__(self, api_key, account_id, environment="practice"):
        self.api        = API(access_token=api_key, environment=environment)
        self.account_id = account_id

    def stream_prices(self, instruments, on_tick):
        params = {
            "instruments": ",".join(instruments),
            "snapshot":    "True",
        }

        r = PricingStream(accountID=self.account_id, params=params)

        for response in self.api.request(r):
            msg_type = response.get("type", "")
            if msg_type == "PRICE":
                on_tick(response)
            elif msg_type == "HEARTBEAT":
                pass
            time.sleep(0.005)
