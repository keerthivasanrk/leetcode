# ======================================================
# controller.py — Master Trading Controller
# ======================================================

from engine.structure import StructureEngine
from engine.liquidity import LiquidityEngine
from engine.entry import EntryEngine
from engine.sessions import SessionEngine
from engine.news import NewsEngine
from engine.position import PositionSizer
from config.user_profile import UserProfile


class TradingController:
    def __init__(self):
        self.user = UserProfile()

        self.structure = StructureEngine()
        self.liquidity = LiquidityEngine()
        self.entry = EntryEngine()
        self.session = SessionEngine()
        self.news = NewsEngine()
        self.position = PositionSizer(self.user)

        self.news.fetch_news()

    # --------------------------------------------------
    def evaluate(self, pair, candle):
        decision = {"action": "WAIT"}

        # News filter
        if self.news.is_high_risk_time()[0]:
            return decision

        # Session filter
        can_trade, _ = self.session.can_trade_now()
        if not can_trade:
            return decision

        structure = self.structure.update(candle)
        liquidity = self.liquidity.update(candle, structure)

        trade = self.entry.generate(
            candle, structure, liquidity,
            {"high_probability": True}
        )

        if not trade:
            return decision

        lot = self.position.calculate_lot_size(
            pair, trade["entry"], trade["sl"]
        )

        if not lot:
            return decision

        margin = self.position.margin_required(
            pair, lot, trade["entry"]
        )

        decision["action"] = trade["signal"]
        decision["trade"] = {
            **trade,
            "lot_size": lot,
            "margin_required": round(margin, 2)
        }

        return decision
