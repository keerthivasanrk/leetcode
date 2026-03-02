import threading
from engine.structure import StructureEngine
from broker.oanda_candles import OandaCandleFetcher
from config.settings import (
    OANDA_API_KEY, OANDA_ACCOUNT_ID, MTF_TIMEFRAMES,
    MTF_REFRESH_MINUTES, MTF_CANDLE_COUNT, PAIRS
)


class MTFBiasEngine:
    def __init__(self):
        self._fetcher = OandaCandleFetcher(
            account_id=OANDA_ACCOUNT_ID,
            api_key=OANDA_API_KEY,
            practice=True
        )
        self._bias  = {pair: {"macro": "neutral", "confirm": "neutral"} for pair in PAIRS}
        self._lock  = threading.Lock()
        self._stop  = threading.Event()

    def start(self):
        self._refresh_all()
        self._schedule_next()

    def stop(self):
        self._stop.set()

    def get_bias(self, pair):
        with self._lock:
            b = self._bias.get(pair, {})
        macro   = b.get("macro",   "neutral")
        confirm = b.get("confirm", "neutral")

        if macro == confirm and macro != "neutral":
            return macro
        return "neutral"

    def get_full_bias(self, pair):
        with self._lock:
            return dict(self._bias.get(pair, {"macro": "neutral", "confirm": "neutral"}))

    def _refresh_all(self):
        for pair in PAIRS:
            try:
                self._refresh_pair(pair)
            except Exception as e:
                print(f"⚠️  MTF refresh failed ({pair}): {e}")

    def _refresh_pair(self, pair):
        results = {}
        for label, tf in MTF_TIMEFRAMES.items():
            candles = self._fetcher.get_candles(pair, tf, count=MTF_CANDLE_COUNT)
            if not candles:
                results[label] = "neutral"
                continue

            eng = StructureEngine()
            for c in candles:
                eng.update(c)

            trend = eng.trend or "neutral"
            results[label] = trend

        with self._lock:
            self._bias[pair] = results

        print(
            f"   📊 MTF [{pair}] H4={results.get('macro','?'):>8} | "
            f"H1={results.get('confirm','?'):>8}"
        )

    def _schedule_next(self):
        if not self._stop.is_set():
            t = threading.Timer(
                MTF_REFRESH_MINUTES * 60,
                self._on_timer
            )
            t.daemon = True
            t.start()

    def _on_timer(self):
        self._refresh_all()
        self._schedule_next()
