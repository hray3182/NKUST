import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime
from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """交易策略基礎類別，包含共同的資料下載、交易邏輯和報告功能"""

    def __init__(self):
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

    def start_strategy(self, target_stock, start_date, end_date, stop_loss=0.1):
        """執行交易策略"""
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
        ax.set_ylabel("Price", fontsize=12)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)

    @abstractmethod
    def draw_indicator(self):
        """繪製指標圖表（由子類別實作）"""
        pass
