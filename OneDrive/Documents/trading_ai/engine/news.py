import feedparser
from datetime import datetime, timedelta, timezone
from datetime import time as dtime


FF_FEED_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

FALLBACK_WINDOWS = [
    (dtime(8, 25),  dtime(8, 35)),
    (dtime(12, 25), dtime(13, 5)),
    (dtime(14, 55), dtime(15, 5)),
    (dtime(17, 55), dtime(18, 5)),
]


class NewsEngine:
    def __init__(self, buffer_minutes=15, currencies=None):
        self.buffer   = timedelta(minutes=buffer_minutes)
        self.watched  = set(currencies or ["USD", "EUR", "GBP", "XAU"])
        self.events   = []
        self._use_feed = True

    def fetch_news(self):
        try:
            feed = feedparser.parse(FF_FEED_URL)

            if feed.bozo and not feed.entries:
                raise ValueError("Feed parse error")

            parsed = []
            for entry in feed.entries:
                impact   = entry.get("ff_impact", "").strip()
                currency = entry.get("ff_currency", "").strip().upper()
                title    = entry.get("title", "")

                if impact.upper() != "HIGH":
                    continue

                date_str = entry.get("ff_date", "")
                time_str = entry.get("ff_time", "")

                if not date_str:
                    continue

                dt = self._parse_ff_datetime(date_str, time_str)
                if dt:
                    parsed.append((dt, currency, impact, title))

            self.events    = parsed
            self._use_feed = True
            print(f"   📰 NewsEngine: loaded {len(self.events)} HIGH-impact events from ForexFactory")

        except Exception as e:
            self._use_feed = False
            self.events    = []
            print(f"   ⚠️  NewsEngine: RSS unavailable ({e}). Using fallback time windows.")

    def is_high_impact(self, pair=None):
        now = datetime.now(timezone.utc)

        if self._use_feed and self.events:
            watched = self._currencies_for_pair(pair)
            for event_dt, currency, _, title in self.events:
                if watched and currency not in watched:
                    continue
                delta = abs((now - event_dt).total_seconds())
                if delta <= self.buffer.total_seconds():
                    print(f"   🚫 News block: {title} ({currency}) in {int(delta)}s")
                    return True
            return False

        now_t = now.time()
        for start, end in FALLBACK_WINDOWS:
            if start <= now_t <= end:
                return True
        return False

    @staticmethod
    def _currencies_for_pair(pair):
        if not pair:
            return set()
        base, quote = pair.split("_") if "_" in pair else (pair, "")
        return {base, quote}

    @staticmethod
    def _parse_ff_datetime(date_str, time_str):
        try:
            dt_str = f"{date_str} {time_str}".strip()
            for fmt in ("%B %d, %Y %I:%M%p", "%b %d, %Y %I:%M%p",
                        "%B %d, %Y", "%b %d, %Y"):
                try:
                    dt = datetime.strptime(dt_str, fmt)
                    dt = dt.replace(tzinfo=timezone.utc) + timedelta(hours=5)
                    return dt
                except ValueError:
                    continue
        except Exception:
            pass
        return None
