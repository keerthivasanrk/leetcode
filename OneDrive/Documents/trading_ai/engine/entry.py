from config.settings import RR_RATIO


class EntryEngine:
    def check(
        self,
        candle,
        structure,
        liquidity,
        trend="neutral",
        volume_ok=False,
        mtf_bias="neutral"
    ):
        if mtf_bias not in ("bullish", "bearish"):
            return None

        bos   = structure.get("bos")
        choch = structure.get("choch")
        if not bos and not choch:
            return None

        structural_dir = bos or choch
        if structural_dir != mtf_bias:
            return None

        if mtf_bias == "bullish":
            swept = liquidity.get("sell_side_sweep", False)
        else:
            swept = liquidity.get("buy_side_sweep", False)

        if not swept:
            return None

        if trend != mtf_bias:
            return None

        if not volume_ok:
            return None

        entry = candle["close"]

        if mtf_bias == "bullish":
            sl = candle["low"]
            risk = entry - sl
            if risk <= 0:
                return None
            tp = entry + risk * RR_RATIO
            direction = "BUY"
        else:
            sl = candle["high"]
            risk = sl - entry
            if risk <= 0:
                return None
            tp = entry - risk * RR_RATIO
            direction = "SELL"

        rr = round(abs(tp - entry) / risk, 2)

        return {
            "direction": direction,
            "entry":     round(entry, 5),
            "sl":        round(sl, 5),
            "tp":        round(tp, 5),
            "rr":        rr,
            "conditions": {
                "mtf_bias":   mtf_bias,
                "structure":  structural_dir,
                "liquidity":  "sell_sweep" if mtf_bias == "bullish" else "buy_sweep",
                "trend":      trend,
                "volume_ok":  volume_ok,
            }
        }
