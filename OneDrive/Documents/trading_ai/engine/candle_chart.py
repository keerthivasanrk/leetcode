import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque


class CandleChart:
    def __init__(self, symbol, max_candles=100):
        self.symbol = symbol
        self.max_candles = max_candles
        self.candles = deque(maxlen=max_candles)

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.manager.set_window_title(symbol)

        self.anim = FuncAnimation(
            self.fig,
            self.draw,
            interval=1000,
            cache_frame_data=False
        )

    def add_candle(self, candle):
        self.candles.append(candle)

    def draw(self, _):
        if not self.candles:
            return

        self.ax.clear()

        for i, c in enumerate(self.candles):
            color = "green" if c["close"] >= c["open"] else "red"

            # Wick
            self.ax.plot([i, i], [c["low"], c["high"]], color=color, linewidth=1)

            # Body
            self.ax.plot([i, i], [c["open"], c["close"]], color=color, linewidth=6)

        prices = [c["high"] for c in self.candles] + [c["low"] for c in self.candles]
        self.ax.set_ylim(min(prices) * 0.999, max(prices) * 1.001)

        self.ax.set_title(self.symbol)
        self.ax.grid(True)
