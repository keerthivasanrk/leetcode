import os
import csv
import json
import time
import threading
from datetime import datetime, timezone
from flask import Flask, render_template, Response, jsonify

from engine.sessions import SessionEngine
from engine.news     import NewsEngine
from config.settings import PAIRS

app         = Flask(__name__)
LOG_FILE    = os.path.join("output", "signals.log")
PRICES_FILE = os.path.join("output", "prices.json")
_news       = NewsEngine()
_session    = SessionEngine()

_lock       = threading.Lock()
_signals    = []
_sse_queue  = []


def _load_existing_signals():
    if not os.path.exists(LOG_FILE):
        return []
    rows = []
    try:
        with open(LOG_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except Exception:
        pass
    return rows


def _watch_log():
    last_size = os.path.getsize(LOG_FILE) if os.path.exists(LOG_FILE) else 0

    while True:
        time.sleep(0.5)
        try:
            if not os.path.exists(LOG_FILE):
                continue

            current_size = os.path.getsize(LOG_FILE)
            if current_size <= last_size:
                continue

            with open(LOG_FILE, newline="") as f:
                f.seek(last_size)
                reader = csv.DictReader(f, fieldnames=[
                    "timestamp", "pair", "direction",
                    "entry", "sl", "tp", "lot_size", "rr"
                ])
                for row in reader:
                    if row["timestamp"] == "timestamp":
                        continue
                    with _lock:
                        _signals.append(row)
                        _sse_queue.append(row)

            last_size = current_size
        except Exception:
            pass


@app.route("/")
def index():
    with _lock:
        history = list(reversed(_signals[-50:]))
    return render_template("index.html", signals=history, pairs=PAIRS)


@app.route("/api/prices")
def api_prices():
    prices = {}
    if os.path.exists(PRICES_FILE):
        try:
            with open(PRICES_FILE, "r") as f:
                prices = json.load(f)
        except Exception:
            pass
    return jsonify(prices)


@app.route("/api/status")
def api_status():
    can_trade, reason = _session.can_trade_now()
    session_name      = _session.current_session()
    in_kz, kz_name    = _session.is_killzone()
    news_block        = _news.is_high_impact()

    now_utc = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

    return jsonify({
        "time":        now_utc,
        "session":     session_name,
        "kill_zone":   kz_name or "None",
        "can_trade":   can_trade,
        "news_block":  news_block,
        "total":       len(_signals),
        "buys":        sum(1 for s in _signals if s.get("direction") == "BUY"),
        "sells":       sum(1 for s in _signals if s.get("direction") == "SELL"),
    })


@app.route("/stream")
def stream():
    def event_generator():
        sent = 0
        while True:
            time.sleep(0.5)
            with _lock:
                new_items = _sse_queue[sent:]
                sent = len(_sse_queue)

            for item in new_items:
                yield f"data: {json.dumps(item)}\n\n"

    return Response(event_generator(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache",
                             "X-Accel-Buffering": "no"})


if __name__ == "__main__":
    existing = _load_existing_signals()
    with _lock:
        _signals.extend(existing)

    try:
        _news.fetch_news()
    except Exception:
        pass

    t = threading.Thread(target=_watch_log, daemon=True)
    t.start()

    print("\n🖥️  Dashboard running at http://localhost:5000")
    print("   (Keep main.py running in the other terminal)\n")

    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
