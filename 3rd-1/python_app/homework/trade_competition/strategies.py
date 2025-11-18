"""
交易策略模組
包含所有技術指標交易策略的實現
"""
import pandas as pd
import numpy as np
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

    def get_total_profit(self):
        """計算總報酬（不含交易成本）"""
        if not self.trades:
            return 0.0
        return sum(trade["Profit"] for trade in self.trades)

    def draw_price_chart(self, ax):
        """繪製價格圖表（共用部分）"""
        ax.plot(
            self.df.index,
            self.df["close"].values.flatten(),
            label="Close Price",
            color="black",
            linewidth=1.5,
        )

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

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._ma5_array = None
        self._ma20_array = None

    def calculate_indicators(self, df):
        """計算雙均線指標"""
        df["MA5"] = talib.SMA(df["close"].values.flatten(), timeperiod=5)
        df["MA20"] = talib.SMA(df["close"].values.flatten(), timeperiod=20)
        # 預先轉換為 NumPy 陣列
        self._ma5_array = df["MA5"].values
        self._ma20_array = df["MA20"].values

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 20

    def check_buy_signal(self, i):
        """檢查買入訊號：黃金交叉（MA5 上穿 MA20）"""
        # 檢查 NaN 值
        if (np.isnan(self._ma5_array[i]) or np.isnan(self._ma20_array[i]) or
            np.isnan(self._ma5_array[i-1]) or np.isnan(self._ma20_array[i-1])):
            return False
        return (self._ma5_array[i] > self._ma20_array[i] and
                self._ma5_array[i-1] <= self._ma20_array[i-1])

    def check_sell_signal(self, i):
        """檢查賣出訊號：死亡交叉（MA5 下穿 MA20）"""
        # 檢查 NaN 值
        if (np.isnan(self._ma5_array[i]) or np.isnan(self._ma20_array[i]) or
            np.isnan(self._ma5_array[i-1]) or np.isnan(self._ma20_array[i-1])):
            return False
        return (self._ma5_array[i] < self._ma20_array[i] and
                self._ma5_array[i-1] >= self._ma20_array[i-1])

    def draw_indicator(self):
        """繪製均線指標圖表"""
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.plot(
            self.df.index,
            self.df["close"].values.flatten(),
            label="Close Price",
            color="black",
            linewidth=1.5,
        )
        ax.plot(self.df.index, self.df["MA5"], label="MA5", color="blue", linewidth=1.5)
        ax.plot(self.df.index, self.df["MA20"], label="MA20", color="orange", linewidth=1.5)
        ax.set_title("Moving Average Strategy (MA5 & MA20)", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price", fontsize=12)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


class BBANDSStrategy(BaseStrategy):
    """布林帶交易策略"""

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._close_array = None
        self._upper_array = None
        self._lower_array = None

    def calculate_indicators(self, df):
        """計算布林帶指標"""
        df["Upper"], df["Middle"], df["Lower"] = talib.BBANDS(
            df["close"].values.flatten(), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        # 預先轉換為 NumPy 陣列
        self._close_array = df["close"].values
        self._upper_array = df["Upper"].values
        self._lower_array = df["Lower"].values

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 20

    def check_buy_signal(self, i):
        """檢查買入訊號：價格從下軌反彈"""
        # 檢查 NaN 值
        if (np.isnan(self._close_array[i]) or np.isnan(self._lower_array[i]) or
            np.isnan(self._close_array[i-1]) or np.isnan(self._lower_array[i-1])):
            return False
        return (self._close_array[i-1] <= self._lower_array[i-1] and
                self._close_array[i] > self._lower_array[i])

    def check_sell_signal(self, i):
        """檢查賣出訊號：價格觸及或突破上軌"""
        # 檢查 NaN 值
        if np.isnan(self._close_array[i]) or np.isnan(self._upper_array[i]):
            return False
        return self._close_array[i] >= self._upper_array[i]

    def draw_indicator(self):
        """繪製布林帶指標圖表"""
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.plot(
            self.df.index,
            self.df["close"].values.flatten(),
            label="Close Price",
            color="black",
            linewidth=1.5,
        )
        ax.plot(self.df.index, self.df["Upper"], label="Upper Band", color="red", linestyle="--", linewidth=1)
        ax.plot(self.df.index, self.df["Middle"], label="Middle Band (SMA20)", color="blue", linestyle="-", linewidth=1)
        ax.plot(self.df.index, self.df["Lower"], label="Lower Band", color="green", linestyle="--", linewidth=1)
        ax.fill_between(self.df.index, self.df["Lower"], self.df["Upper"], alpha=0.1, color="gray")
        ax.set_title("Bollinger Bands Strategy", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price", fontsize=12)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


class KDStrategy(BaseStrategy):
    """KD 隨機指標交易策略"""

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._k_array = None
        self._d_array = None

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
        # 預先轉換為 NumPy 陣列
        self._k_array = df["K"].values
        self._d_array = df["D"].values

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 15

    def check_buy_signal(self, i):
        """檢查買入訊號：KD 黃金交叉（K 上穿 D）"""
        # 檢查 NaN 值
        if (np.isnan(self._k_array[i]) or np.isnan(self._d_array[i]) or
            np.isnan(self._k_array[i-1]) or np.isnan(self._d_array[i-1])):
            return False
        return (self._k_array[i] > self._d_array[i] and
                self._k_array[i-1] <= self._d_array[i-1])

    def check_sell_signal(self, i):
        """檢查賣出訊號：KD 死亡交叉（K 下穿 D）"""
        # 檢查 NaN 值
        if (np.isnan(self._k_array[i]) or np.isnan(self._d_array[i]) or
            np.isnan(self._k_array[i-1]) or np.isnan(self._d_array[i-1])):
            return False
        return (self._k_array[i] < self._d_array[i] and
                self._k_array[i-1] >= self._d_array[i-1])

    def draw_indicator(self):
        """繪製 KD 指標圖表"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
        self.draw_price_chart(ax1)
        ax2.plot(self.df.index, self.df["K"], label="K Line", color="blue", linewidth=1.5)
        ax2.plot(self.df.index, self.df["D"], label="D Line", color="orange", linewidth=1.5)
        ax2.axhline(y=80, color="red", linestyle="--", alpha=0.5)
        ax2.axhline(y=20, color="green", linestyle="--", alpha=0.5)
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

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._macd_array = None
        self._signal_array = None

    def calculate_indicators(self, df):
        """計算 MACD 指標"""
        df["MACD"], df["Signal"], df["Hist"] = talib.MACD(
            df["close"].values.flatten(),
            fastperiod=12,
            slowperiod=26,
            signalperiod=9,
        )
        # 預先轉換為 NumPy 陣列
        self._macd_array = df["MACD"].values
        self._signal_array = df["Signal"].values

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 26

    def check_buy_signal(self, i):
        """檢查買入訊號：MACD 黃金交叉（MACD 上穿 Signal）"""
        # 檢查 NaN 值
        if (np.isnan(self._macd_array[i]) or np.isnan(self._signal_array[i]) or
            np.isnan(self._macd_array[i-1]) or np.isnan(self._signal_array[i-1])):
            return False
        return (self._macd_array[i] > self._signal_array[i] and
                self._macd_array[i-1] <= self._signal_array[i-1])

    def check_sell_signal(self, i):
        """檢查賣出訊號：MACD 死亡交叉（MACD 下穿 Signal）"""
        # 檢查 NaN 值
        if (np.isnan(self._macd_array[i]) or np.isnan(self._signal_array[i]) or
            np.isnan(self._macd_array[i-1]) or np.isnan(self._signal_array[i-1])):
            return False
        return (self._macd_array[i] < self._signal_array[i] and
                self._macd_array[i-1] >= self._signal_array[i-1])

    def draw_indicator(self):
        """繪製 MACD 指標圖表"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
        self.draw_price_chart(ax1)
        ax2.plot(self.df.index, self.df["MACD"], label="MACD", color="blue", linewidth=1.5)
        ax2.plot(self.df.index, self.df["Signal"], label="Signal", color="orange", linewidth=1.5)
        colors = ["red" if val < 0 else "green" for val in self.df["Hist"]]
        ax2.bar(self.df.index, self.df["Hist"], label="Histogram", color=colors, alpha=0.3, width=0.8)
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

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._rsi_array = None

    def calculate_indicators(self, df):
        """計算 RSI 指標"""
        df["RSI"] = talib.RSI(df["close"].values.flatten(), timeperiod=14)
        # 預先轉換為 NumPy 陣列
        self._rsi_array = df["RSI"].values

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 15

    def check_buy_signal(self, i):
        """檢查買入訊號：RSI 從超賣區（<30）向上突破 30"""
        # 檢查 NaN 值
        if np.isnan(self._rsi_array[i]) or np.isnan(self._rsi_array[i-1]):
            return False
        return self._rsi_array[i] > 30 and self._rsi_array[i-1] <= 30

    def check_sell_signal(self, i):
        """檢查賣出訊號：RSI 從超買區（>70）向下跌破 70"""
        # 檢查 NaN 值
        if np.isnan(self._rsi_array[i]) or np.isnan(self._rsi_array[i-1]):
            return False
        return self._rsi_array[i] < 70 and self._rsi_array[i-1] >= 70

    def draw_indicator(self):
        """繪製 RSI 指標圖表"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
        self.draw_price_chart(ax1)
        ax2.plot(self.df.index, self.df["RSI"], label="RSI", color="purple", linewidth=1.5)
        ax2.axhline(y=70, color="red", linestyle="--", alpha=0.5, label="Overbought (70)")
        ax2.axhline(y=30, color="green", linestyle="--", alpha=0.5, label="Oversold (30)")
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


class EMAStrategy(BaseStrategy):
    """EMA 指數移動平均線交叉策略"""

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._ema12_array = None
        self._ema26_array = None

    def calculate_indicators(self, df):
        """計算 EMA 指標"""
        df["EMA12"] = talib.EMA(df["close"].values.flatten(), timeperiod=12)
        df["EMA26"] = talib.EMA(df["close"].values.flatten(), timeperiod=26)
        # 預先轉換為 NumPy 陣列
        self._ema12_array = df["EMA12"].values
        self._ema26_array = df["EMA26"].values

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 26

    def check_buy_signal(self, i):
        """檢查買入訊號：EMA12 上穿 EMA26"""
        # 檢查 NaN 值
        if (np.isnan(self._ema12_array[i]) or np.isnan(self._ema26_array[i]) or
            np.isnan(self._ema12_array[i-1]) or np.isnan(self._ema26_array[i-1])):
            return False
        return (self._ema12_array[i] > self._ema26_array[i] and
                self._ema12_array[i-1] <= self._ema26_array[i-1])

    def check_sell_signal(self, i):
        """檢查賣出訊號：EMA12 下穿 EMA26"""
        # 檢查 NaN 值
        if (np.isnan(self._ema12_array[i]) or np.isnan(self._ema26_array[i]) or
            np.isnan(self._ema12_array[i-1]) or np.isnan(self._ema26_array[i-1])):
            return False
        return (self._ema12_array[i] < self._ema26_array[i] and
                self._ema12_array[i-1] >= self._ema26_array[i-1])

    def draw_indicator(self):
        """繪製 EMA 指標圖表"""
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.plot(self.df.index, self.df["close"].values.flatten(), label="Close Price", color="black", linewidth=1.5)
        ax.plot(self.df.index, self.df["EMA12"], label="EMA12", color="blue", linewidth=1.5)
        ax.plot(self.df.index, self.df["EMA26"], label="EMA26", color="orange", linewidth=1.5)
        ax.set_title("EMA Strategy (EMA12 & EMA26)", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price", fontsize=12)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


class WilliamsRStrategy(BaseStrategy):
    """威廉指標 (Williams %R) 交易策略"""

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._willr_array = None

    def calculate_indicators(self, df):
        """計算 Williams %R 指標"""
        df["WILLR"] = talib.WILLR(
            df["high"].values.flatten(),
            df["low"].values.flatten(),
            df["close"].values.flatten(),
            timeperiod=14
        )
        # 預先轉換為 NumPy 陣列
        self._willr_array = df["WILLR"].values

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 15

    def check_buy_signal(self, i):
        """檢查買入訊號：從超賣區（<-80）向上突破 -80"""
        # 檢查 NaN 值
        if np.isnan(self._willr_array[i]) or np.isnan(self._willr_array[i-1]):
            return False
        return self._willr_array[i] > -80 and self._willr_array[i-1] <= -80

    def check_sell_signal(self, i):
        """檢查賣出訊號：從超買區（>-20）向下跌破 -20"""
        # 檢查 NaN 值
        if np.isnan(self._willr_array[i]) or np.isnan(self._willr_array[i-1]):
            return False
        return self._willr_array[i] < -20 and self._willr_array[i-1] >= -20

    def draw_indicator(self):
        """繪製 Williams %R 指標圖表"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
        self.draw_price_chart(ax1)
        ax2.plot(self.df.index, self.df["WILLR"], label="Williams %R", color="purple", linewidth=1.5)
        ax2.axhline(y=-20, color="red", linestyle="--", alpha=0.5, label="Overbought (-20)")
        ax2.axhline(y=-80, color="green", linestyle="--", alpha=0.5, label="Oversold (-80)")
        ax2.fill_between(self.df.index, -20, 0, alpha=0.1, color="red")
        ax2.fill_between(self.df.index, -100, -80, alpha=0.1, color="green")
        ax2.set_title("Williams %R Indicator", fontsize=14, fontweight="bold")
        ax2.set_xlabel("Date", fontsize=12)
        ax2.set_ylabel("Williams %R Value", fontsize=12)
        ax2.legend(loc="best")
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(-100, 0)
        plt.tight_layout()
        plt.show()


class CCIStrategy(BaseStrategy):
    """CCI (商品通道指數) 交易策略"""

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._cci_array = None

    def calculate_indicators(self, df):
        """計算 CCI 指標"""
        df["CCI"] = talib.CCI(
            df["high"].values.flatten(),
            df["low"].values.flatten(),
            df["close"].values.flatten(),
            timeperiod=14
        )
        # 預先轉換為 NumPy 陣列
        self._cci_array = df["CCI"].values

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 15

    def check_buy_signal(self, i):
        """檢查買入訊號：CCI 從超賣區（<-100）向上突破 -100"""
        # 檢查 NaN 值
        if np.isnan(self._cci_array[i]) or np.isnan(self._cci_array[i-1]):
            return False
        return self._cci_array[i] > -100 and self._cci_array[i-1] <= -100

    def check_sell_signal(self, i):
        """檢查賣出訊號：CCI 從超買區（>100）向下跌破 100"""
        # 檢查 NaN 值
        if np.isnan(self._cci_array[i]) or np.isnan(self._cci_array[i-1]):
            return False
        return self._cci_array[i] < 100 and self._cci_array[i-1] >= 100

    def draw_indicator(self):
        """繪製 CCI 指標圖表"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
        self.draw_price_chart(ax1)
        ax2.plot(self.df.index, self.df["CCI"], label="CCI", color="blue", linewidth=1.5)
        ax2.axhline(y=100, color="red", linestyle="--", alpha=0.5, label="Overbought (100)")
        ax2.axhline(y=-100, color="green", linestyle="--", alpha=0.5, label="Oversold (-100)")
        ax2.axhline(y=0, color="gray", linestyle=":", alpha=0.3)
        ax2.fill_between(self.df.index, 100, 200, alpha=0.1, color="red")
        ax2.fill_between(self.df.index, -200, -100, alpha=0.1, color="green")
        ax2.set_title("CCI Indicator", fontsize=14, fontweight="bold")
        ax2.set_xlabel("Date", fontsize=12)
        ax2.set_ylabel("CCI Value", fontsize=12)
        ax2.legend(loc="best")
        ax2.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


class ADXStrategy(BaseStrategy):
    """ADX (平均趨向指標) 交易策略"""

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._adx_array = None
        self._plus_di_array = None
        self._minus_di_array = None

    def calculate_indicators(self, df):
        """計算 ADX 指標"""
        df["ADX"] = talib.ADX(
            df["high"].values.flatten(),
            df["low"].values.flatten(),
            df["close"].values.flatten(),
            timeperiod=14
        )
        df["PLUS_DI"] = talib.PLUS_DI(
            df["high"].values.flatten(),
            df["low"].values.flatten(),
            df["close"].values.flatten(),
            timeperiod=14
        )
        df["MINUS_DI"] = talib.MINUS_DI(
            df["high"].values.flatten(),
            df["low"].values.flatten(),
            df["close"].values.flatten(),
            timeperiod=14
        )
        # 預先轉換為 NumPy 陣列
        self._adx_array = df["ADX"].values
        self._plus_di_array = df["PLUS_DI"].values
        self._minus_di_array = df["MINUS_DI"].values

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 15

    def check_buy_signal(self, i):
        """檢查買入訊號：ADX > 25 且 PLUS_DI 上穿 MINUS_DI"""
        # 檢查 NaN 值
        if (np.isnan(self._adx_array[i]) or np.isnan(self._plus_di_array[i]) or
            np.isnan(self._minus_di_array[i]) or np.isnan(self._plus_di_array[i-1]) or
            np.isnan(self._minus_di_array[i-1])):
            return False
        adx_strong = self._adx_array[i] > 25
        di_cross = (self._plus_di_array[i] > self._minus_di_array[i] and
                    self._plus_di_array[i-1] <= self._minus_di_array[i-1])
        return adx_strong and di_cross

    def check_sell_signal(self, i):
        """檢查賣出訊號：ADX > 25 且 MINUS_DI 上穿 PLUS_DI"""
        # 檢查 NaN 值
        if (np.isnan(self._adx_array[i]) or np.isnan(self._plus_di_array[i]) or
            np.isnan(self._minus_di_array[i]) or np.isnan(self._plus_di_array[i-1]) or
            np.isnan(self._minus_di_array[i-1])):
            return False
        adx_strong = self._adx_array[i] > 25
        di_cross = (self._minus_di_array[i] > self._plus_di_array[i] and
                    self._minus_di_array[i-1] <= self._plus_di_array[i-1])
        return adx_strong and di_cross

    def draw_indicator(self):
        """繪製 ADX 指標圖表"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
        self.draw_price_chart(ax1)
        ax2.plot(self.df.index, self.df["ADX"], label="ADX", color="blue", linewidth=1.5)
        ax2.plot(self.df.index, self.df["PLUS_DI"], label="+DI", color="green", linewidth=1.5)
        ax2.plot(self.df.index, self.df["MINUS_DI"], label="-DI", color="red", linewidth=1.5)
        ax2.axhline(y=25, color="gray", linestyle="--", alpha=0.5, label="Strong Trend (25)")
        ax2.set_title("ADX Indicator", fontsize=14, fontweight="bold")
        ax2.set_xlabel("Date", fontsize=12)
        ax2.set_ylabel("ADX Value", fontsize=12)
        ax2.legend(loc="best")
        ax2.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


class OBVStrategy(BaseStrategy):
    """OBV (能量潮) 交易策略"""

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._obv_array = None
        self._obv_ma_array = None

    def calculate_indicators(self, df):
        """計算 OBV 指標"""
        # 確保數據類型為 float64
        close_array = df["close"].values.flatten().astype(float)
        volume_array = df["volume"].values.flatten().astype(float)
        df["OBV"] = talib.OBV(close_array, volume_array)
        df["OBV_MA"] = talib.SMA(df["OBV"].values.flatten().astype(float), timeperiod=20)
        # 預先轉換為 NumPy 陣列
        self._obv_array = df["OBV"].values
        self._obv_ma_array = df["OBV_MA"].values

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 20

    def check_buy_signal(self, i):
        """檢查買入訊號：OBV 上穿 OBV_MA"""
        # 檢查 NaN 值
        if (np.isnan(self._obv_array[i]) or np.isnan(self._obv_ma_array[i]) or
            np.isnan(self._obv_array[i-1]) or np.isnan(self._obv_ma_array[i-1])):
            return False
        return (self._obv_array[i] > self._obv_ma_array[i] and
                self._obv_array[i-1] <= self._obv_ma_array[i-1])

    def check_sell_signal(self, i):
        """檢查賣出訊號：OBV 下穿 OBV_MA"""
        # 檢查 NaN 值
        if (np.isnan(self._obv_array[i]) or np.isnan(self._obv_ma_array[i]) or
            np.isnan(self._obv_array[i-1]) or np.isnan(self._obv_ma_array[i-1])):
            return False
        return (self._obv_array[i] < self._obv_ma_array[i] and
                self._obv_array[i-1] >= self._obv_ma_array[i-1])

    def draw_indicator(self):
        """繪製 OBV 指標圖表"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
        self.draw_price_chart(ax1)
        ax2.plot(self.df.index, self.df["OBV"], label="OBV", color="blue", linewidth=1.5)
        ax2.plot(self.df.index, self.df["OBV_MA"], label="OBV MA(20)", color="orange", linewidth=1.5)
        ax2.set_title("OBV Indicator", fontsize=14, fontweight="bold")
        ax2.set_xlabel("Date", fontsize=12)
        ax2.set_ylabel("OBV Value", fontsize=12)
        ax2.legend(loc="best")
        ax2.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


class ATRStrategy(BaseStrategy):
    """ATR (平均真實波幅) 突破策略"""

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._close_array = None
        self._upper_band_array = None
        self._lower_band_array = None

    def calculate_indicators(self, df):
        """計算 ATR 指標"""
        df["ATR"] = talib.ATR(
            df["high"].values.flatten(),
            df["low"].values.flatten(),
            df["close"].values.flatten(),
            timeperiod=14
        )
        df["MA20"] = talib.SMA(df["close"].values.flatten(), timeperiod=20)
        df["Upper_Band"] = df["MA20"] + 2 * df["ATR"]
        df["Lower_Band"] = df["MA20"] - 2 * df["ATR"]
        # 預先轉換為 NumPy 陣列
        self._close_array = df["close"].values
        self._upper_band_array = df["Upper_Band"].values
        self._lower_band_array = df["Lower_Band"].values

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 20

    def check_buy_signal(self, i):
        """檢查買入訊號：價格突破上軌"""
        # 檢查 NaN 值
        if (np.isnan(self._close_array[i]) or np.isnan(self._upper_band_array[i]) or
            np.isnan(self._close_array[i-1]) or np.isnan(self._upper_band_array[i-1])):
            return False
        return (self._close_array[i] > self._upper_band_array[i] and
                self._close_array[i-1] <= self._upper_band_array[i-1])

    def check_sell_signal(self, i):
        """檢查賣出訊號：價格跌破下軌"""
        # 檢查 NaN 值
        if (np.isnan(self._close_array[i]) or np.isnan(self._lower_band_array[i]) or
            np.isnan(self._close_array[i-1]) or np.isnan(self._lower_band_array[i-1])):
            return False
        return (self._close_array[i] < self._lower_band_array[i] and
                self._close_array[i-1] >= self._lower_band_array[i-1])

    def draw_indicator(self):
        """繪製 ATR 指標圖表"""
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.plot(self.df.index, self.df["close"].values.flatten(), label="Close Price", color="black", linewidth=1.5)
        ax.plot(self.df.index, self.df["MA20"], label="MA20", color="blue", linewidth=1.5)
        ax.plot(self.df.index, self.df["Upper_Band"], label="Upper Band (MA20+2ATR)", color="red", linestyle="--", linewidth=1)
        ax.plot(self.df.index, self.df["Lower_Band"], label="Lower Band (MA20-2ATR)", color="green", linestyle="--", linewidth=1)
        ax.fill_between(self.df.index, self.df["Lower_Band"], self.df["Upper_Band"], alpha=0.1, color="gray")
        ax.set_title("ATR Breakout Strategy", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price", fontsize=12)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


class TripleMAStrategy(BaseStrategy):
    """三重均線交易策略"""

    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._ma5_array = None
        self._ma10_array = None
        self._ma20_array = None

    def calculate_indicators(self, df):
        """計算三重均線指標"""
        df["MA5"] = talib.SMA(df["close"].values.flatten(), timeperiod=5)
        df["MA10"] = talib.SMA(df["close"].values.flatten(), timeperiod=10)
        df["MA20"] = talib.SMA(df["close"].values.flatten(), timeperiod=20)
        # 預先轉換為 NumPy 陣列
        self._ma5_array = df["MA5"].values
        self._ma10_array = df["MA10"].values
        self._ma20_array = df["MA20"].values

    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 20

    def check_buy_signal(self, i):
        """檢查買入訊號：MA5 > MA10 > MA20 且 MA5 剛上穿 MA10"""
        # 檢查 NaN 值
        if (np.isnan(self._ma5_array[i]) or np.isnan(self._ma10_array[i]) or
            np.isnan(self._ma20_array[i]) or np.isnan(self._ma5_array[i-1]) or
            np.isnan(self._ma10_array[i-1])):
            return False
        alignment = self._ma5_array[i] > self._ma10_array[i] > self._ma20_array[i]
        cross = (self._ma5_array[i] > self._ma10_array[i] and
                 self._ma5_array[i-1] <= self._ma10_array[i-1])
        return alignment and cross

    def check_sell_signal(self, i):
        """檢查賣出訊號：MA5 < MA10 < MA20 且 MA5 剛下穿 MA10"""
        # 檢查 NaN 值
        if (np.isnan(self._ma5_array[i]) or np.isnan(self._ma10_array[i]) or
            np.isnan(self._ma20_array[i]) or np.isnan(self._ma5_array[i-1]) or
            np.isnan(self._ma10_array[i-1])):
            return False
        alignment = self._ma5_array[i] < self._ma10_array[i] < self._ma20_array[i]
        cross = (self._ma5_array[i] < self._ma10_array[i] and
                 self._ma5_array[i-1] >= self._ma10_array[i-1])
        return alignment and cross

    def draw_indicator(self):
        """繪製三重均線指標圖表"""
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.plot(self.df.index, self.df["close"].values.flatten(), label="Close Price", color="black", linewidth=1.5)
        ax.plot(self.df.index, self.df["MA5"], label="MA5", color="blue", linewidth=1.5)
        ax.plot(self.df.index, self.df["MA10"], label="MA10", color="orange", linewidth=1.5)
        ax.plot(self.df.index, self.df["MA20"], label="MA20", color="green", linewidth=1.5)
        ax.set_title("Triple Moving Average Strategy", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price", fontsize=12)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


class GridStrategy(BaseStrategy):
    """網格交易策略 - 適合盤整趨勢"""
    
    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1, grid_levels=5):
        """
        初始化網格交易策略
        
        Args:
            target_stock: 股票代號
            start_date: 資料開始日期
            end_date: 資料結束日期
            stop_loss: 停損點
            grid_levels: 網格層數（預設 5 層）
        """
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self.grid_levels = grid_levels
        self._close_array = None
        self._upper_array = None
        self._lower_array = None
        self._middle_array = None
        self._grid_buy_levels = None  # 買入網格層級
        self._grid_sell_levels = None  # 賣出網格層級
    
    def calculate_indicators(self, df):
        """計算網格指標（基於布林帶）"""
        # 使用布林帶確定價格區間
        df["Upper"], df["Middle"], df["Lower"] = talib.BBANDS(
            df["close"].values.flatten(), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        
        # 預先轉換為 NumPy 陣列
        self._close_array = df["close"].values
        self._upper_array = df["Upper"].values
        self._lower_array = df["Lower"].values
        self._middle_array = df["Middle"].values
        
        # 計算每個時間點的網格層級
        # 將價格區間分成 grid_levels 個網格
        self._grid_buy_levels = np.zeros(len(df))
        self._grid_sell_levels = np.zeros(len(df))
        
        for i in range(len(df)):
            if (not np.isnan(self._upper_array[i]) and 
                not np.isnan(self._lower_array[i]) and 
                not np.isnan(self._close_array[i])):
                # 計算當前價格在網格中的位置（0 到 grid_levels-1）
                price_range = self._upper_array[i] - self._lower_array[i]
                if price_range > 0:
                    # 計算當前價格所在的網格層級（從下往上，0 是最下層）
                    grid_position = (self._close_array[i] - self._lower_array[i]) / price_range
                    grid_level = int(grid_position * self.grid_levels)
                    grid_level = max(0, min(self.grid_levels - 1, grid_level))  # 限制在範圍內
                    
                    # 買入網格：價格在下半部分時（網格層級 < grid_levels/2）
                    self._grid_buy_levels[i] = grid_level if grid_level < self.grid_levels / 2 else -1
                    # 賣出網格：價格在上半部分時（網格層級 >= grid_levels/2）
                    self._grid_sell_levels[i] = grid_level if grid_level >= self.grid_levels / 2 else -1
                else:
                    self._grid_buy_levels[i] = -1
                    self._grid_sell_levels[i] = -1
            else:
                self._grid_buy_levels[i] = -1
                self._grid_sell_levels[i] = -1
    
    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 20
    
    def check_buy_signal(self, i):
        """
        檢查買入訊號：價格從較低網格反彈
        當價格從下層網格向上移動時買入
        """
        # 檢查 NaN 值
        if (np.isnan(self._close_array[i]) or np.isnan(self._lower_array[i]) or
            np.isnan(self._close_array[i-1]) or np.isnan(self._lower_array[i-1])):
            return False
        
        # 確保有有效的網格層級
        if (self._grid_buy_levels[i] < 0 or self._grid_buy_levels[i-1] < 0):
            return False
        
        # 買入條件：
        # 1. 當前價格在下半部分網格（適合買入區域）
        # 2. 價格從下層網格反彈（當前網格層級 > 前一天網格層級）
        # 3. 或者價格觸及下軌後反彈
        price_near_lower = self._close_array[i] <= self._lower_array[i] * 1.02  # 價格接近下軌（2% 容差）
        grid_bounce = self._grid_buy_levels[i] > self._grid_buy_levels[i-1]  # 網格層級上升
        
        return price_near_lower and grid_bounce
    
    def check_sell_signal(self, i):
        """
        檢查賣出訊號：價格觸及較高網格
        當價格觸及上層網格時賣出
        """
        # 檢查 NaN 值
        if (np.isnan(self._close_array[i]) or np.isnan(self._upper_array[i]) or
            np.isnan(self._close_array[i-1]) or np.isnan(self._upper_array[i-1])):
            return False
        
        # 確保有有效的網格層級
        if self._grid_sell_levels[i] < 0:
            return False
        
        # 賣出條件：
        # 1. 價格觸及或接近上軌
        # 2. 價格在上半部分網格（適合賣出區域）
        price_near_upper = self._close_array[i] >= self._upper_array[i] * 0.98  # 價格接近上軌（2% 容差）
        in_sell_zone = self._grid_sell_levels[i] >= self.grid_levels / 2
        
        return price_near_upper and in_sell_zone
    
    def draw_indicator(self):
        """繪製網格交易策略圖表"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # 繪製價格線
        ax.plot(
            self.df.index,
            self.df["close"].values.flatten(),
            label="Close Price",
            color="black",
            linewidth=1.5,
        )
        
        # 繪製布林帶
        ax.plot(self.df.index, self._upper_array, label="Upper Band", color="red", linestyle="--", linewidth=1)
        ax.plot(self.df.index, self._middle_array, label="Middle Band (SMA20)", color="blue", linestyle="-", linewidth=1)
        ax.plot(self.df.index, self._lower_array, label="Lower Band", color="green", linestyle="--", linewidth=1)
        
        # 繪製網格線（可選，顯示部分網格）
        # 在最後一個時間點繪製網格線作為示例
        if len(self.df) > 0:
            last_idx = len(self.df) - 1
            if (not np.isnan(self._upper_array[last_idx]) and 
                not np.isnan(self._lower_array[last_idx])):
                price_range = self._upper_array[last_idx] - self._lower_array[last_idx]
                for level in range(1, self.grid_levels):
                    grid_price = self._lower_array[last_idx] + (price_range * level / self.grid_levels)
                    ax.axhline(y=grid_price, color="gray", linestyle=":", alpha=0.3, linewidth=0.5)
        
        ax.fill_between(self.df.index, self._lower_array, self._upper_array, alpha=0.1, color="gray")
        ax.set_title(f"Grid Trading Strategy ({self.grid_levels} Levels)", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price", fontsize=12)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


class MomentumReversalStrategy(BaseStrategy):
    """
    動量反轉策略 - 捕捉動量後的短期反轉
    基於反向 RSI 的邏輯，結合動量確認
    """
    
    def __init__(self, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        super().__init__(target_stock, start_date, end_date, stop_loss)
        self._rsi_array = None
        self._roc_array = None
        self._close_array = None
    
    def calculate_indicators(self, df):
        """計算動量反轉指標"""
        # RSI 用於判斷超買超賣
        df["RSI"] = talib.RSI(df["close"].values.flatten(), timeperiod=14)
        # ROC (Rate of Change) 用於確認動量方向
        df["ROC"] = talib.ROC(df["close"].values.flatten(), timeperiod=10)
        # 預先轉換為 NumPy 陣列
        self._rsi_array = df["RSI"].values
        self._roc_array = df["ROC"].values
        self._close_array = df["close"].values
    
    def get_start_index(self):
        """取得開始交易的索引位置"""
        return 15  # 需要足夠的數據計算 RSI 和 ROC
    
    def check_buy_signal(self, i):
        """
        檢查買入訊號：RSI 從超買區回調時買入（反向邏輯）
        結合動量確認，確保動量向上
        """
        # 檢查 NaN 值
        if (np.isnan(self._rsi_array[i]) or np.isnan(self._rsi_array[i-1]) or
            np.isnan(self._roc_array[i]) or np.isnan(self._close_array[i]) or
            np.isnan(self._close_array[i-1])):
            return False
        
        # RSI 從超買區（>70）回調到 70 以下
        rsi_pullback = (self._rsi_array[i] < 70 and self._rsi_array[i-1] >= 70)
        
        # 動量確認：價格變化率為正或接近零（允許小幅波動）
        momentum_ok = self._roc_array[i] >= -1.0  # 允許小幅負動量
        
        return rsi_pullback and momentum_ok
    
    def check_sell_signal(self, i):
        """
        檢查賣出訊號：RSI 從超賣區反彈時賣出（反向邏輯）
        結合動量確認，確保動量向下
        """
        # 檢查 NaN 值
        if (np.isnan(self._rsi_array[i]) or np.isnan(self._rsi_array[i-1]) or
            np.isnan(self._roc_array[i]) or np.isnan(self._close_array[i]) or
            np.isnan(self._close_array[i-1])):
            return False
        
        # RSI 從超賣區（<30）反彈到 30 以上
        rsi_bounce = (self._rsi_array[i] > 30 and self._rsi_array[i-1] <= 30)
        
        # 動量確認：價格變化率為負或接近零（允許小幅波動）
        momentum_ok = self._roc_array[i] <= 1.0  # 允許小幅正動量
        
        return rsi_bounce and momentum_ok
    
    def draw_indicator(self):
        """繪製動量反轉策略圖表"""
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
        
        # 價格圖
        ax1.plot(self.df.index, self.df["close"].values.flatten(), label="Close Price", color="black", linewidth=1.5)
        ax1.set_title("Momentum Reversal Strategy", fontsize=14, fontweight="bold")
        ax1.set_ylabel("Price", fontsize=12)
        ax1.legend(loc="best")
        ax1.grid(True, alpha=0.3)
        
        # RSI 圖
        ax2.plot(self.df.index, self.df["RSI"], label="RSI", color="purple", linewidth=1.5)
        ax2.axhline(y=70, color="red", linestyle="--", alpha=0.5, label="Overbought (70)")
        ax2.axhline(y=30, color="green", linestyle="--", alpha=0.5, label="Oversold (30)")
        ax2.fill_between(self.df.index, 70, 100, alpha=0.1, color="red")
        ax2.fill_between(self.df.index, 0, 30, alpha=0.1, color="green")
        ax2.set_ylabel("RSI Value", fontsize=12)
        ax2.legend(loc="best")
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 100)
        
        # ROC 圖
        ax3.plot(self.df.index, self.df["ROC"], label="ROC (10)", color="blue", linewidth=1.5)
        ax3.axhline(y=0, color="gray", linestyle="-", alpha=0.5)
        ax3.set_ylabel("ROC (%)", fontsize=12)
        ax3.set_xlabel("Date", fontsize=12)
        ax3.legend(loc="best")
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

