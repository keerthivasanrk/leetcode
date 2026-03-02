import requests
from datetime import datetime, timezone


class OandaCandleFetcher:
    def __init__(self, account_id, api_key, practice=True):
        self.account_id = account_id
        self.api_key    = api_key
        self.base_url   = (
            "https://api-fxpractice.oanda.com"
            if practice else
            "https://api-fxtrade.oanda.com"
        )

    def get_candles(self, instrument, timeframe, count=100):
        url = f"{self.base_url}/v3/instruments/{instrument}/candles"

        headers = {"Authorization": f"Bearer {self.api_key}"}
        params  = {"granularity": timeframe, "count": count, "price": "M"}

        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()

        candles = []
        for c in r.json().get("candles", []):
            if not c.get("complete", False):
                continue

            ts_raw = c["time"].replace("Z", "+00:00")
            try:
                ts = datetime.fromisoformat(ts_raw).replace(tzinfo=None)
            except ValueError:
                ts = datetime.fromisoformat(c["time"].rstrip("Z"))

            candles.append({
                "time":   ts,
                "open":   float(c["mid"]["o"]),
                "high":   float(c["mid"]["h"]),
                "low":    float(c["mid"]["l"]),
                "close":  float(c["mid"]["c"]),
                "volume": int(c.get("volume", 1)),
            })

        return candles
