class LiquidityEngine:
    def __init__(self, max_levels=20):
        self.highs = []
        self.lows = []
        self.max_levels = max_levels

    def update(self, candle, structure):
        result = {
            "buy_side_sweep": False,
            "sell_side_sweep": False
        }

        if not candle or not structure:
            return result

        high = candle.get("high")
        low = candle.get("low")

        if high is None or low is None:
            return result

        if structure.get("swing_high"):
            self.highs.append(high)

        if structure.get("swing_low"):
            self.lows.append(low)

        self.highs = self.highs[-self.max_levels:]
        self.lows = self.lows[-self.max_levels:]

        if len(self.highs) > 1:
            prev_high = max(self.highs[:-1])
            if high > prev_high:
                result["buy_side_sweep"] = True

        if len(self.lows) > 1:
            prev_low = min(self.lows[:-1])
            if low < prev_low:
                result["sell_side_sweep"] = True

        return result
