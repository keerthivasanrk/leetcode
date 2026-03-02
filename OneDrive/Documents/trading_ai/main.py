import sys
import json
import time

from broker.oanda import OandaBroker
from config.settings import (
    OANDA_API_KEY, OANDA_ACCOUNT_ID, PAIRS, RISK_PERCENT
)

from engine.candles       import CandleBuilder
from engine.structure     import StructureEngine
from engine.liquidity     import LiquidityEngine
from engine.entry         import EntryEngine
from engine.risk          import RiskEngine
from engine.news          import NewsEngine
from engine.sessions      import SessionEngine
from engine.trend_filter  import TrendFilter
from engine.volume_filter import VolumeFilter
from engine.mtf_bias      import MTFBiasEngine

from output.signal_logger import SignalLogger


def print_banner(balance, leverage):
    print()
    print("╔══════════════════════════════════════════════╗")
    print("║    🤖  AI TRADING SIGNAL ENGINE  v2.0        ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║  Broker    : OANDA Practice                 ║")
    print(f"║  Pairs     : {', '.join(PAIRS):<31} ║")
    print(f"║  Balance   : ${balance:<30} ║")
    print(f"║  Leverage  : 1:{str(leverage):<29} ║")
    print(f"║  Risk/Trade: {int(RISK_PERCENT*100)}%{' '*30} ║")
    print("║  Mode      : Signal Only (no auto-execution) ║")
    print("╚══════════════════════════════════════════════╝")
    print()


def get_user_inputs():
    print("\n=== Trading AI Setup ===")
    try:
        balance  = float(input("Enter Account Balance ($): ").strip())
        leverage = int(input("Enter Leverage (e.g. 10, 50, 100): ").strip())
    except (ValueError, EOFError):
        print("⚠️  Invalid input — using defaults: $10,000 / 1:100")
        balance, leverage = 10000.0, 100
    return balance, leverage


def main():
    balance, leverage = get_user_inputs()
    print_banner(balance, leverage)

    if not OANDA_API_KEY or not OANDA_ACCOUNT_ID:
        print("❌  OANDA credentials missing. Add them to your .env file.")
        sys.exit(1)

    logger  = SignalLogger()
    news    = NewsEngine()
    mtf     = MTFBiasEngine()
    session = SessionEngine()

    print("📰 Fetching economic news calendar…")
    news.fetch_news()

    print("📊 Loading multi-timeframe bias (H4 / H1)…")
    mtf.start()

    print("\n⏳ Waiting for live ticks — monitoring:", PAIRS)
    print("="*50)

    engines = {}
    last_prices = {pair: 0.0 for pair in PAIRS}
    last_price_export = 0

    for pair in PAIRS:
        engines[pair] = {
            "candles":   CandleBuilder(),
            "structure": StructureEngine(),
            "liquidity": LiquidityEngine(),
            "entry":     EntryEngine(),
            "risk":      RiskEngine(balance, risk_percent=RISK_PERCENT),
            "trend":     TrendFilter(),
            "volume":    VolumeFilter(),
        }

    def on_tick(tick):
        try:
            pair   = tick.get("instrument")
            engine = engines.get(pair)
            if engine is None:
                return

            bid   = float(tick["bids"][0]["price"])
            ask   = float(tick["asks"][0]["price"])
            price = (bid + ask) / 2.0

            last_prices[pair] = round(price, 5)

            nonlocal last_price_export
            if time.time() - last_price_export > 1.0:
                try:
                    with open("output/prices.json", "w") as f:
                        json.dump(last_prices, f)
                    last_price_export = time.time()
                except Exception:
                    pass

            candle = engine["candles"].update(tick["time"], price)
            if candle is None:
                return

            history = engine["candles"].get_history()

            structure = engine["structure"].update(candle)

            liquidity = engine["liquidity"].update(candle, structure)

            can_trade, reason = session.can_trade_now()
            if not can_trade:
                return

            if news.is_high_impact(pair):
                return

            trend = engine["trend"].get_trend(history)

            volume_ok = engine["volume"].is_volume_confirmed(candle, history)

            mtf_bias = mtf.get_bias(pair)

            signal = engine["entry"].check(
                candle    = candle,
                structure = structure,
                liquidity = liquidity,
                trend     = trend,
                volume_ok = volume_ok,
                mtf_bias  = mtf_bias,
            )

            if signal is None:
                return

            lot = engine["risk"].calculate_position_size(
                entry     = signal["entry"],
                stop_loss = signal["sl"],
                leverage  = leverage,
            )

            if lot is None:
                return

            logger.log(
                pair       = pair,
                direction  = signal["direction"],
                entry      = signal["entry"],
                sl         = signal["sl"],
                tp         = signal["tp"],
                lot_size   = lot,
                rr         = signal.get("rr"),
                conditions = signal.get("conditions"),
            )

        except Exception as e:
            print(f"⚠️  Tick Error ({tick.get('instrument', '?')}): {e}")

    broker = OandaBroker(OANDA_API_KEY, OANDA_ACCOUNT_ID)

    try:
        broker.stream_prices(PAIRS, on_tick)
    except KeyboardInterrupt:
        print("\n\n🛑  Engine stopped by user.")
        mtf.stop()


if __name__ == "__main__":
    main()
