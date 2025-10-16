import talib
import matplotlib.pyplot as plt
from datetime import datetime
from .base_strategy import BaseStrategy


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


# 向後相容的函數介面
def init(df):
    """計算雙均線指標"""
    df["MA5"] = talib.SMA(df["close"].values.flatten(), timeperiod=5)
    df["MA20"] = talib.SMA(df["close"].values.flatten(), timeperiod=20)


def start_strategy(target_stock, start_date, end_date, stopLoss=0.1):
    """執行雙均線策略（向後相容）"""
    strategy = MAStrategy()
    return strategy.start_strategy(target_stock, start_date, end_date, stopLoss)


def draw_MA_indicator(df):
    """繪製均線指標圖（向後相容）"""
    strategy = MAStrategy()
    strategy.df = df
    strategy.draw_indicator()


def main():
    target_stock = "2498.TW"  # 分析公司代號 e.g., '2330.TW'是台積電
    start_date = datetime(2021, 1, 1)  # 設定資料開始日期
    end_date = datetime(2021, 7, 19)  # 設定資料結束日期
    stopLoss = 0.1  # 停損點，指-10%會強制賣出

    # 執行策略並取得結果
    df = start_strategy(target_stock, start_date, end_date, stopLoss)

    # 繪製均線指標圖
    draw_MA_indicator(df)


if __name__ == "__main__":
    main()
