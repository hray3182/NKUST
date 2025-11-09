"""
交易策略模組
包含所有技術指標交易策略的實現
"""
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import talib
from datetime import datetime
from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """交易策略基礎類別，包含共同的資料下載、交易邏輯和報告功能"""

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        """
        初始化交易策略

        Args:
            target_stock: 股票代號 (e.g., '2498.TW')
            start_date: 資料開始日期
            end_date: 資料結束日期
            stop_loss: 停損點，預設為 0.1 (即 -10%)
        """
        self.target_stock = target_stock
        self.start_date = start_date
        self.end_date = end_date
        self.stop_loss = stop_loss
        self.df = None
        self.trades = []

    def download_data(self, target_stock, start_date, end_date):
        """下載股票資料並進行欄位重命名"""
        df = yf.download(target_stock, start_date, end_date, auto_adjust=True)
        df = df[["Open", "High", "Low", "Close", "Volume"]]
        df.rename(
            columns={
                "Close": "close",
                "High": "high",
                "Low": "low",
                "Open": "open",
                "Volume": "volume",
            },
            inplace=True,
        )
        self.df = df
        return df

    @abstractmethod
    def calculate_indicators(self, df):
        """計算技術指標（由子類別實作）"""
        pass

    @abstractmethod
    def check_buy_signal(self, i):
        """檢查買入訊號（由子類別實作）"""
        pass

    @abstractmethod
    def check_sell_signal(self, i):
        """檢查賣出訊號（由子類別實作）"""
        pass

    @abstractmethod
    def get_start_index(self):
        """取得開始交易的索引位置（由子類別實作）"""
        pass

    def check_stop_loss(self, current_price, buy_price, stop_loss):
        """檢查是否觸及停損點"""
        return (current_price - buy_price) / buy_price <= stop_loss

    def record_trade(self, buy_date, buy_price, sell_date, sell_price, exit_type):
        """記錄交易"""
        profit = sell_price - buy_price
        profit_pct = (profit / buy_price) * 100

        self.trades.append(
            {
                "Buy Date": buy_date,
                "Buy Price": buy_price,
                "Sell Date": sell_date,
                "Sell Price": sell_price,
                "Profit": profit,
                "Profit %": profit_pct,
                "Exit Type": exit_type,
            }
        )

        if exit_type == "Stop Loss":
            print(
                f"[STOP LOSS] Sell Date: {sell_date.strftime('%Y-%m-%d')}, "
                f"Sell Price: {sell_price:.2f}, P&L: {profit:.2f} ({profit_pct:.2f}%)"
            )
        else:
            print(
                f"Sell Date: {sell_date.strftime('%Y-%m-%d')}, "
                f"Sell Price: {sell_price:.2f}, P&L: {profit:.2f} ({profit_pct:.2f}%)"
            )

    def print_trading_summary(self):
        """顯示交易摘要"""
        if self.trades:
            trades_df = pd.DataFrame(self.trades)
            print("\n=== Trading Summary ===")
            print(trades_df.to_string(index=False))
            print(f"\nTotal Trades: {len(self.trades)}")
            print(f"Total Profit: {trades_df['Profit'].sum():.2f}")
            print(f"Average Profit per Trade: {trades_df['Profit'].mean():.2f}")
            print(
                f"Win Rate: {(trades_df['Profit'] > 0).sum() / len(self.trades) * 100:.2f}%"
            )
            print(f"\nExit by Signal: {(trades_df['Exit Type'] == 'Signal').sum()}")
            print(
                f"Exit by Stop Loss: {(trades_df['Exit Type'] == 'Stop Loss').sum()}"
            )
        else:
            print("No trades executed.")

    def start_strategy(self, target_stock=None, start_date=None, end_date=None, stop_loss=None):
        """
        執行交易策略

        Args:
            target_stock: 股票代號，若為 None 則使用初始化時的值
            start_date: 資料開始日期，若為 None 則使用初始化時的值
            end_date: 資料結束日期，若為 None 則使用初始化時的值
            stop_loss: 停損點，若為 None 則使用初始化時的值
        """
        # 使用傳入的參數或類別屬性
        target_stock = target_stock or self.target_stock
        start_date = start_date or self.start_date
        end_date = end_date or self.end_date
        stop_loss = stop_loss if stop_loss is not None else self.stop_loss

        # 下載股票資料
        df = self.download_data(target_stock, start_date, end_date)

        # 計算技術指標
        self.calculate_indicators(df)

        # 初始化
        flag = 0
        buy_price = 0
        buy_date = None
        self.trades = []
        stop_loss_value = -stop_loss  # 把停損轉為負數

        start_idx = self.get_start_index()

        for i in range(start_idx, len(df)):
            current_price = df["close"].iloc[i].item()

            # 買入訊號
            if flag == 0 and self.check_buy_signal(i):
                flag = 1
                buy_price = current_price
                buy_date = df.index[i]
                print(
                    f"Buy Date: {buy_date.strftime('%Y-%m-%d')}, Buy Price: {buy_price:.2f}"
                )

            # 持有期間檢查停損
            elif flag == 1 and self.check_stop_loss(
                current_price, buy_price, stop_loss_value
            ):
                flag = 0
                self.record_trade(
                    buy_date, buy_price, df.index[i], current_price, "Stop Loss"
                )

            # 賣出訊號
            elif flag == 1 and self.check_sell_signal(i):
                flag = 0
                self.record_trade(
                    buy_date, buy_price, df.index[i], current_price, "Signal"
                )

        # 顯示交易摘要
        self.print_trading_summary()

        return df

    def draw_price_chart(self, ax):
        """繪製價格圖表（共用部分）"""
        ax.plot(
            self.df.index,
            self.df["close"].values.flatten(),
            label="Close Price",
            color="black",
            linewidth=1.5,
        )

        # 如果有設定 target_stock，在標題中顯示
        title = "Stock Price Chart"
        if self.target_stock:
            title = f"{self.target_stock} - Stock Price Chart"
        ax.set_title(title, fontsize=14, fontweight="bold")

        ax.set_ylabel("Price", fontsize=12)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)

    @abstractmethod
    def draw_indicator(self):
        """繪製指標圖表（由子類別實作）"""
        pass


class MAStrategy(BaseStrategy):
    """雙均線交易策略"""

    def calculate_indicators(self, df):
        """計算雙均線指標"""
        df["MA5"] = talib.SMA(df["close"].values.flatten(), timeperiod=5)
        df["MA20"] = talib.SMA(df["close"].values.flatten(), timeperiod=20)

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 20

    def check_buy_signal(self, i):
        """檢查買入訊號：黃金交叉（MA5 上穿 MA20）"""
        current_ma5 = self.df["MA5"].iloc[i]
        current_ma20 = self.df["MA20"].iloc[i]
        prev_ma5 = self.df["MA5"].iloc[i - 1]
        prev_ma20 = self.df["MA20"].iloc[i - 1]

        return current_ma5 > current_ma20 and prev_ma5 <= prev_ma20

    def check_sell_signal(self, i):
        """檢查賣出訊號：死亡交叉（MA5 下穿 MA20）"""
        current_ma5 = self.df["MA5"].iloc[i]
        current_ma20 = self.df["MA20"].iloc[i]
        prev_ma5 = self.df["MA5"].iloc[i - 1]
        prev_ma20 = self.df["MA20"].iloc[i - 1]

        return current_ma5 < current_ma20 and prev_ma5 >= prev_ma20

    def draw_indicator(self):
        """繪製均線指標圖表"""
        fig, ax = plt.subplots(figsize=(14, 8))

        # Price trend
        ax.plot(
            self.df.index,
            self.df["close"].values.flatten(),
            label="Close Price",
            color="black",
            linewidth=1.5,
        )

        # Moving Averages
        ax.plot(self.df.index, self.df["MA5"], label="MA5", color="blue", linewidth=1.5)
        ax.plot(
            self.df.index, self.df["MA20"], label="MA20", color="orange", linewidth=1.5
        )

        ax.set_title(
            "Moving Average Strategy (MA5 & MA20)", fontsize=14, fontweight="bold"
        )
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price", fontsize=12)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()


class BBANDSStrategy(BaseStrategy):
    """布林帶交易策略"""

    def calculate_indicators(self, df):
        """計算布林帶指標"""
        df["Upper"], df["Middle"], df["Lower"] = talib.BBANDS(
            df["close"].values.flatten(), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 20

    def check_buy_signal(self, i):
        """檢查買入訊號：價格從下軌反彈（前一天觸及或跌破下軌，當天回到下軌上方）"""
        current_price = self.df["close"].iloc[i].item()
        prev_price = self.df["close"].iloc[i - 1].item()
        lower_band = self.df["Lower"].iloc[i]
        prev_lower = self.df["Lower"].iloc[i - 1]

        return prev_price <= prev_lower and current_price > lower_band

    def check_sell_signal(self, i):
        """檢查賣出訊號：價格觸及或突破上軌"""
        current_price = self.df["close"].iloc[i].item()
        upper_band = self.df["Upper"].iloc[i]

        return current_price >= upper_band

    def draw_indicator(self):
        """繪製布林帶指標圖表"""
        fig, ax = plt.subplots(figsize=(14, 8))

        # Price trend
        ax.plot(
            self.df.index,
            self.df["close"].values.flatten(),
            label="Close Price",
            color="black",
            linewidth=1.5,
        )

        # Bollinger Bands
        ax.plot(
            self.df.index,
            self.df["Upper"],
            label="Upper Band",
            color="red",
            linestyle="--",
            linewidth=1,
        )
        ax.plot(
            self.df.index,
            self.df["Middle"],
            label="Middle Band (SMA20)",
            color="blue",
            linestyle="-",
            linewidth=1,
        )
        ax.plot(
            self.df.index,
            self.df["Lower"],
            label="Lower Band",
            color="green",
            linestyle="--",
            linewidth=1,
        )

        # Fill between bands
        ax.fill_between(
            self.df.index, self.df["Lower"], self.df["Upper"], alpha=0.1, color="gray"
        )

        ax.set_title("Bollinger Bands Strategy", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price", fontsize=12)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()


class KDStrategy(BaseStrategy):
    """KD 隨機指標交易策略"""

    def calculate_indicators(self, df):
        """計算 KD 指標"""
        df["K"], df["D"] = talib.STOCH(
            df["high"].values.flatten(),
            df["low"].values.flatten(),
            df["close"].values.flatten(),
            fastk_period=9,
            slowk_period=3,
            slowd_period=3,
        )

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 15

    def check_buy_signal(self, i):
        """檢查買入訊號：KD 黃金交叉（K 上穿 D）"""
        current_k = self.df["K"].iloc[i]
        current_d = self.df["D"].iloc[i]
        prev_k = self.df["K"].iloc[i - 1]
        prev_d = self.df["D"].iloc[i - 1]

        return current_k > current_d and prev_k <= prev_d

    def check_sell_signal(self, i):
        """檢查賣出訊號：KD 死亡交叉（K 下穿 D）"""
        current_k = self.df["K"].iloc[i]
        current_d = self.df["D"].iloc[i]
        prev_k = self.df["K"].iloc[i - 1]
        prev_d = self.df["D"].iloc[i - 1]

        return current_k < current_d and prev_k >= prev_d

    def draw_indicator(self):
        """繪製 KD 指標圖表"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

        # Top chart: Price trend
        self.draw_price_chart(ax1)

        # Bottom chart: KD indicator
        ax2.plot(self.df.index, self.df["K"], label="K Line", color="blue", linewidth=1.5)
        ax2.plot(
            self.df.index, self.df["D"], label="D Line", color="orange", linewidth=1.5
        )

        # Overbought/Oversold zones
        ax2.axhline(y=80, color="red", linestyle="--", alpha=0.5)
        ax2.axhline(y=20, color="green", linestyle="--", alpha=0.5)
        ax2.axhline(y=50, color="gray", linestyle=":", alpha=0.3)

        # Fill zones
        ax2.fill_between(self.df.index, 80, 100, alpha=0.1, color="red")
        ax2.fill_between(self.df.index, 0, 20, alpha=0.1, color="green")

        ax2.set_title("KD Stochastic Indicator", fontsize=14, fontweight="bold")
        ax2.set_xlabel("Date", fontsize=12)
        ax2.set_ylabel("KD Value", fontsize=12)
        ax2.legend(loc="best")
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 100)

        plt.tight_layout()
        plt.show()


class MACDStrategy(BaseStrategy):
    """MACD 交易策略"""

    def calculate_indicators(self, df):
        """計算 MACD 指標"""
        df["MACD"], df["Signal"], df["Hist"] = talib.MACD(
            df["close"].values.flatten(),
            fastperiod=12,
            slowperiod=26,
            signalperiod=9,
        )

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 26

    def check_buy_signal(self, i):
        """檢查買入訊號：MACD 黃金交叉（MACD 上穿 Signal）"""
        current_macd = self.df["MACD"].iloc[i]
        current_signal = self.df["Signal"].iloc[i]
        prev_macd = self.df["MACD"].iloc[i - 1]
        prev_signal = self.df["Signal"].iloc[i - 1]

        return current_macd > current_signal and prev_macd <= prev_signal

    def check_sell_signal(self, i):
        """檢查賣出訊號：MACD 死亡交叉（MACD 下穿 Signal）"""
        current_macd = self.df["MACD"].iloc[i]
        current_signal = self.df["Signal"].iloc[i]
        prev_macd = self.df["MACD"].iloc[i - 1]
        prev_signal = self.df["Signal"].iloc[i - 1]

        return current_macd < current_signal and prev_macd >= prev_signal

    def draw_indicator(self):
        """繪製 MACD 指標圖表"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

        # Top chart: Price trend
        self.draw_price_chart(ax1)

        # Bottom chart: MACD indicator
        ax2.plot(
            self.df.index, self.df["MACD"], label="MACD", color="blue", linewidth=1.5
        )
        ax2.plot(
            self.df.index,
            self.df["Signal"],
            label="Signal",
            color="orange",
            linewidth=1.5,
        )

        # MACD histogram
        colors = ["red" if val < 0 else "green" for val in self.df["Hist"]]
        ax2.bar(
            self.df.index,
            self.df["Hist"],
            label="Histogram",
            color=colors,
            alpha=0.3,
            width=0.8,
        )

        # Zero line
        ax2.axhline(y=0, color="gray", linestyle="-", alpha=0.5)

        ax2.set_title("MACD Indicator", fontsize=14, fontweight="bold")
        ax2.set_xlabel("Date", fontsize=12)
        ax2.set_ylabel("MACD Value", fontsize=12)
        ax2.legend(loc="best")
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()


class RSIStrategy(BaseStrategy):
    """RSI 交易策略"""

    def calculate_indicators(self, df):
        """計算 RSI 指標"""
        df["RSI"] = talib.RSI(df["close"].values.flatten(), timeperiod=14)

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 15

    def check_buy_signal(self, i):
        """檢查買入訊號：RSI 從超賣區（<30）向上突破 30"""
        current_rsi = self.df["RSI"].iloc[i]
        prev_rsi = self.df["RSI"].iloc[i - 1]

        return current_rsi > 30 and prev_rsi <= 30

    def check_sell_signal(self, i):
        """檢查賣出訊號：RSI 從超買區（>70）向下跌破 70"""
        current_rsi = self.df["RSI"].iloc[i]
        prev_rsi = self.df["RSI"].iloc[i - 1]

        return current_rsi < 70 and prev_rsi >= 70

    def draw_indicator(self):
        """繪製 RSI 指標圖表"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

        # Top chart: Price trend
        self.draw_price_chart(ax1)

        # Bottom chart: RSI indicator
        ax2.plot(
            self.df.index, self.df["RSI"], label="RSI", color="purple", linewidth=1.5
        )

        # Overbought/Oversold zones
        ax2.axhline(
            y=70, color="red", linestyle="--", alpha=0.5, label="Overbought (70)"
        )
        ax2.axhline(
            y=30, color="green", linestyle="--", alpha=0.5, label="Oversold (30)"
        )
        ax2.axhline(y=50, color="gray", linestyle=":", alpha=0.3)

        # Fill zones
        ax2.fill_between(self.df.index, 70, 100, alpha=0.1, color="red")
        ax2.fill_between(self.df.index, 0, 30, alpha=0.1, color="green")

        ax2.set_title("RSI Indicator", fontsize=14, fontweight="bold")
        ax2.set_xlabel("Date", fontsize=12)
        ax2.set_ylabel("RSI Value", fontsize=12)
        ax2.legend(loc="best")
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 100)

        plt.tight_layout()
        plt.show()
