class TrendFilter:
    def __init__(self, period=50):
        self.period = period
        self._ema   = None

    def get_trend(self, candles):
        if len(candles) < self.period:
            return "neutral"

        self._ema = self._compute_ema([c["close"] for c in candles])

        last_close = candles[-1]["close"]

        if last_close > self._ema:
            return "bullish"
        elif last_close < self._ema:
            return "bearish"
        return "neutral"

    def _compute_ema(self, prices):
        k   = 2 / (self.period + 1)
        ema = sum(prices[:self.period]) / self.period

        for price in prices[self.period:]:
            ema = price * k + ema * (1 - k)

        return ema

    @property
    def ema_value(self):
        return self._ema
