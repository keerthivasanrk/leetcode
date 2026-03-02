from collections import deque


class StructureEngine:
    def __init__(self, swing_lookback=3):
        self.swing_lookback = swing_lookback

        self.highs = deque(maxlen=2 * swing_lookback + 1)
        self.lows  = deque(maxlen=2 * swing_lookback + 1)

        self.last_swing_high = None
        self.last_swing_low  = None

        self.trend = None

    def update(self, candle):
        self.highs.append(candle)
        self.lows.append(candle)

        structure = {
            "swing_high": False,
            "swing_low": False,
            "bos": None,
            "choch": None,
            "trend": self.trend
        }

        if len(self.highs) < self.highs.maxlen:
            return structure

        mid = self.swing_lookback
        mid_candle = self.highs[mid]

        if all(mid_candle["high"] > c["high"] for i, c in enumerate(self.highs) if i != mid):
            structure["swing_high"] = True

            if self.last_swing_high is None or mid_candle["high"] > self.last_swing_high["high"]:
                if self.trend == "bearish":
                    structure["choch"] = "bullish"
                else:
                    structure["bos"] = "bullish"

                self.trend = "bullish"

            self.last_swing_high = mid_candle

        if all(mid_candle["low"] < c["low"] for i, c in enumerate(self.lows) if i != mid):
            structure["swing_low"] = True

            if self.last_swing_low is None or mid_candle["low"] < self.last_swing_low["low"]:
                if self.trend == "bullish":
                    structure["choch"] = "bearish"
                else:
                    structure["bos"] = "bearish"

                self.trend = "bearish"

            self.last_swing_low = mid_candle

        structure["trend"] = self.trend
        return structure
