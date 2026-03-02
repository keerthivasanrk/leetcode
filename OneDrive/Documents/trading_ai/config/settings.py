import os
from dotenv import load_dotenv

load_dotenv()

OANDA_API_KEY    = os.getenv("OANDA_API_KEY", "")
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID", "")
OANDA_ENV        = os.getenv("OANDA_ENV", "practice")

PAIRS = [
    "EUR_USD",
    "GBP_USD",
    "XAU_USD",
]

BASE_TIMEFRAME = "M1"
BASE_TIMEFRAME_SECONDS = 60

MTF_TIMEFRAMES = {
    "macro":   "H4",
    "confirm": "H1",
}

RISK_PERCENT    = 0.01
RR_RATIO        = 2.0

VOLUME_LOOKBACK      = 20
VOLUME_MULTIPLIER    = 1.2

SWING_LOOKBACK = 3

MTF_REFRESH_MINUTES = 15
MTF_CANDLE_COUNT    = 100

NEWS_BUFFER_MINUTES = 15
NEWS_CURRENCIES     = {
    "EUR_USD": ["EUR", "USD"],
    "GBP_USD": ["GBP", "USD"],
    "XAU_USD": ["USD", "XAU"],
}
