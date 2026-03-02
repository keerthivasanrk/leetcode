class VolumeFilter:
    def __init__(self, lookback=20, multiplier=1.2):
        self.lookback    = lookback
        self.multiplier  = multiplier

    def is_volume_confirmed(self, candle, history):
        if not history or len(history) < 3:
            return True

        recent   = history[-self.lookback:] if len(history) >= self.lookback else history
        avg_vol  = sum(c.get("volume", 1) for c in recent) / len(recent)

        if avg_vol <= 0:
            return True

        current_vol = candle.get("volume", 1)
        return current_vol >= (avg_vol * self.multiplier)

    def volume_ratio(self, candle, history):
        if not history:
            return 1.0

        recent  = history[-self.lookback:] if len(history) >= self.lookback else history
        avg_vol = sum(c.get("volume", 1) for c in recent) / len(recent)

        if avg_vol <= 0:
            return 1.0

        return round(candle.get("volume", 1) / avg_vol, 2)
