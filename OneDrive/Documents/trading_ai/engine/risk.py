class RiskEngine:
    def __init__(self, balance, risk_percent=0.01):
        self.balance = balance
        self.risk_percent = risk_percent

    def calculate_position_size(self, entry, stop_loss, leverage=1):
        if entry is None or stop_loss is None:
            return None

        stop_distance = abs(entry - stop_loss)

        if stop_distance <= 0:
            return None

        risk_amount = self.balance * self.risk_percent

        position_size = (risk_amount / stop_distance) * leverage

        return round(position_size, 2)
