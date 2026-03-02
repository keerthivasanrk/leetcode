from collections import deque
from datetime import datetime


class CandleBuilder:
    def __init__(self, timeframe_seconds=60, history_size=100):
        self.timeframe  = timeframe_seconds
        self.current    = None
        self.candles    = deque(maxlen=history_size)

    def update(self, timestamp, price):
        ts = self._to_epoch(timestamp)

        if self.current is None:
            self._open_candle(ts, price)
            return None

        if ts - self.current["start"] < self.timeframe:
            self.current["high"]   = max(self.current["high"], price)
            self.current["low"]    = min(self.current["low"], price)
            self.current["close"]  = price
            self.current["volume"] += 1
            return None

        finished = dict(self.current)
        self.candles.append(finished)

        self._open_candle(ts, price)

        return finished

    def _open_candle(self, ts, price):
        self.current = {
            "open":   price,
            "high":   price,
            "low":    price,
            "close":  price,
            "start":  ts,
            "volume": 1,
        }

    def get_history(self):
        return list(self.candles)

    @staticmethod
    def _to_epoch(t):
        if isinstance(t, str):
            t = t.rstrip("Z").split(".")[0]
            return int(datetime.fromisoformat(t).timestamp())
        return int(t)
