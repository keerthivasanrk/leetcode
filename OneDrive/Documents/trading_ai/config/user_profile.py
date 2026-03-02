# ======================================================
# user_profile.py — User Risk & Account Configuration
# ======================================================

class UserProfile:
    def __init__(self):
        # -------------------------------
        # ACCOUNT DETAILS
        # -------------------------------
        self.account_balance = 10000      # USD
        self.account_currency = "USD"
        self.leverage = 100               # 1:100

        # -------------------------------
        # RISK MANAGEMENT
        # -------------------------------
        self.risk_per_trade = 0.01        # 1% per trade
        self.max_daily_risk = 0.03        # 3% per day
        self.max_open_trades = 1

        # -------------------------------
        # CONTRACT SETTINGS
        # -------------------------------
        self.forex_contract_size = 100000   # standard lot
        self.gold_contract_size = 100        # XAUUSD (100 oz)

        # -------------------------------
        # BROKER SETTINGS
        # -------------------------------
        self.min_lot = 0.01
        self.max_lot = 50.0

    # --------------------------------------------------
    def risk_amount(self):
        return self.account_balance * self.risk_per_trade
