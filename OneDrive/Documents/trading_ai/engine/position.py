# ======================================================
# position.py — Lot Size & Margin Calculator
# ======================================================

class PositionSizer:
    def __init__(self, user):
        self.user = user

    # --------------------------------------------------
    def pip_value(self, pair, lot_size):
        if "XAU" in pair:
            return lot_size * 1.0
        return lot_size * 10.0  # Forex standard

    # --------------------------------------------------
    def calculate_lot_size(self, pair, entry, sl):
        risk_amount = self.user.risk_amount()
        stop_distance = abs(entry - sl)

        if stop_distance <= 0:
            return None

        if "XAU" in pair:
            pip_val = 1.0
            contract = self.user.gold_contract_size
        else:
            pip_val = 10.0
            contract = self.user.forex_contract_size

        lot = risk_amount / (stop_distance * pip_val * contract / 100000)

        lot = round(lot, 2)

        if lot < self.user.min_lot:
            return None

        if lot > self.user.max_lot:
            lot = self.user.max_lot

        return lot

    # --------------------------------------------------
    def margin_required(self, pair, lot_size, price):
        if "XAU" in pair:
            contract = self.user.gold_contract_size
        else:
            contract = self.user.forex_contract_size

        return (lot_size * contract * price) / self.user.leverage
