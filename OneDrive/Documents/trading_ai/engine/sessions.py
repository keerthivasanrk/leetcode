from datetime import datetime, time
import pytz


class SessionEngine:
    def __init__(self, timezone="UTC"):
        self.tz = pytz.timezone(timezone)

        self.sessions = {
            "ASIA": (time(0, 0), time(6, 0)),
            "LONDON": (time(7, 0), time(10, 0)),
            "NEW_YORK": (time(12, 0), time(16, 0)),
        }

        self.kill_zones = {
            "LONDON_KZ": (time(7, 0), time(9, 0)),
            "NEW_YORK_KZ": (time(12, 0), time(14, 0)),
        }

    def _now_utc(self):
        return datetime.utcnow().replace(tzinfo=pytz.utc)

    def current_session(self):
        now = self._now_utc().time()

        for session, (start, end) in self.sessions.items():
            if start <= now <= end:
                return session

        return "OFF_SESSION"

    def is_killzone(self):
        now = self._now_utc().time()

        for kz, (start, end) in self.kill_zones.items():
            if start <= now <= end:
                return True, kz

        return False, None

    def can_trade_now(self):
        session = self.current_session()
        in_kz, kz_name = self.is_killzone()

        if session == "OFF_SESSION":
            return False, "Outside major sessions"

        if not in_kz:
            return False, f"In session ({session}) but outside kill zone"

        return True, f"Kill Zone active: {kz_name}"
