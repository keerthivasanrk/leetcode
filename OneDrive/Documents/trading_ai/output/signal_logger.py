import os
import csv
from datetime import datetime, timezone


_LOG_DIR  = os.path.join(os.path.dirname(__file__))
_LOG_FILE = os.path.join(_LOG_DIR, "signals.log")

_HEADER = ["timestamp", "pair", "direction", "entry", "sl", "tp", "lot_size", "rr"]


class SignalLogger:
    def __init__(self, log_file=_LOG_FILE):
        self.log_file = log_file
        self._ensure_file()

    def log(self, pair, direction, entry, sl, tp, lot_size, rr=None, conditions=None):
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        rr_display = f"{rr:.2f}" if rr else "N/A"

        print()
        print("╔══════════════════════════════════════╗")
        print("║         ✅  TRADE SIGNAL              ║")
        print("╠══════════════════════════════════════╣")
        print(f"║  Time      : {now_str:<22} ║")
        print(f"║  Pair      : {pair:<22} ║")
        print(f"║  Direction : {direction:<22} ║")
        print(f"║  Entry     : {str(entry):<22} ║")
        print(f"║  Stop Loss : {str(sl):<22} ║")
        print(f"║  Take Profit: {str(tp):<21} ║")
        print(f"║  Lot Size  : {str(lot_size):<22} ║")
        print(f"║  R:R       : {rr_display:<22} ║")
        print("╚══════════════════════════════════════╝")

        if conditions:
            print("  Conditions:")
            for k, v in conditions.items():
                print(f"    {k:<14}: {v}")

        print()

        with open(self.log_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([now_str, pair, direction, entry, sl, tp, lot_size, rr_display])

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.log_file) or ".", exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", newline="") as f:
                csv.writer(f).writerow(_HEADER)
