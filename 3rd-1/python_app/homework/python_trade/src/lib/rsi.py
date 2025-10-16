import talib
import matplotlib.pyplot as plt
from datetime import datetime
from .base_strategy import BaseStrategy


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
        ax1.set_title("Stock Price Chart", fontsize=14, fontweight="bold")
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


# 向後相容的函數介面
def init(df):
    """計算 RSI 指標"""
    df["RSI"] = talib.RSI(df["close"].values.flatten(), timeperiod=14)


def start_strategy(target_stock, start_date, end_date, stopLoss=0.1):
    """執行 RSI 策略（向後相容）"""
    strategy = RSIStrategy()
    return strategy.start_strategy(target_stock, start_date, end_date, stopLoss)


def draw_RSI_indicator(df):
    """繪製 RSI 指標圖（向後相容）"""
    strategy = RSIStrategy()
    strategy.df = df
    strategy.draw_indicator()


def main():
    target_stock = "2498.TW"  # 分析公司代號 e.g., '2330.TW'是台積電
    start_date = datetime(2021, 1, 1)  # 設定資料開始日期
    end_date = datetime(2021, 7, 19)  # 設定資料結束日期
    stopLoss = 0.1  # 停損點，指-10%會強制賣出

    # 執行策略並取得結果
    df = start_strategy(target_stock, start_date, end_date, stopLoss)

    # 繪製 RSI 指標圖
    draw_RSI_indicator(df)


if __name__ == "__main__":
    main()
