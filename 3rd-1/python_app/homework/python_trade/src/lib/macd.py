import talib
import matplotlib.pyplot as plt
from datetime import datetime
from .base_strategy import BaseStrategy


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


# 向後相容的函數介面
def init(df):
    """計算 MACD 指標"""
    df["MACD"], df["Signal"], df["Hist"] = talib.MACD(
        df["close"].values.flatten(),
        fastperiod=12,
        slowperiod=26,
        signalperiod=9,
    )


def start_strategy(target_stock, start_date, end_date, stopLoss=0.1):
    """執行 MACD 策略（向後相容）"""
    strategy = MACDStrategy()
    return strategy.start_strategy(target_stock, start_date, end_date, stopLoss)


def draw_MACD_indicator(df):
    """繪製 MACD 指標圖（向後相容）"""
    strategy = MACDStrategy()
    strategy.df = df
    strategy.draw_indicator()


def main():
    target_stock = "2498.TW"  # 分析公司代號 e.g., '2330.TW'是台積電
    start_date = datetime(2021, 1, 1)  # 設定資料開始日期
    end_date = datetime(2021, 7, 19)  # 設定資料結束日期
    stopLoss = 0.1  # 停損點，指-10%會強制賣出

    # 執行策略並取得結果
    df = start_strategy(target_stock, start_date, end_date, stopLoss)

    # 繪製 MACD 指標圖
    draw_MACD_indicator(df)


if __name__ == "__main__":
    main()
