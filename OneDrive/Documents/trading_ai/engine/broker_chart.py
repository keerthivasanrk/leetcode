import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation


class BrokerChart:
    def __init__(self, symbol, fetcher, timeframe):
        self.symbol = symbol
        self.fetcher = fetcher
        self.timeframe = timeframe

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.manager.set_window_title(symbol)

        self.animation = FuncAnimation(
            self.fig,
            self.update,
            interval=5000,
            cache_frame_data=False
        )

    def update(self, frame):
        candles = self.fetcher.get_candles(
            self.symbol,
            self.timeframe,
            count=100
        )

        if not candles:
            return

        self.ax.clear()
        self.ax.set_title(f"{self.symbol} ({self.timeframe})")

        for c in candles:
            color = "green" if c["close"] >= c["open"] else "red"

            self.ax.plot(
                [c["time"], c["time"]],
                [c["low"], c["high"]],
                color=color
            )

            self.ax.plot(
                [c["time"], c["time"]],
                [c["open"], c["close"]],
                linewidth=4,
                color=color
            )

        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        self.fig.autofmt_xdate()
