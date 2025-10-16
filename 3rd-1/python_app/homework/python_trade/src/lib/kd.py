import talib
import matplotlib.pyplot as plt
from datetime import datetime
from .base_strategy import BaseStrategy


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


# 向後相容的函數介面
def init(df):
    """計算 KD 指標"""
    df["K"], df["D"] = talib.STOCH(
        df["high"].values.flatten(),
        df["low"].values.flatten(),
        df["close"].values.flatten(),
        fastk_period=9,
        slowk_period=3,
        slowd_period=3,
    )


def start_strategy(target_stock, start_date, end_date, stopLoss=0.1):
    """執行 KD 策略（向後相容）"""
    strategy = KDStrategy()
    return strategy.start_strategy(target_stock, start_date, end_date, stopLoss)


def draw_KD_indicator(df):
    """繪製 KD 指標圖（向後相容）"""
    strategy = KDStrategy()
    strategy.df = df
    strategy.draw_indicator()


def main():
    target_stock = "2498.TW"  # 分析公司代號 e.g., '2330.TW'是台積電
    start_date = datetime(2021, 1, 1)  # 設定資料開始日期
    end_date = datetime(2021, 7, 19)  # 設定資料結束日期
    stopLoss = 0.1  # 停損點，指-10%會強制賣出

    # 執行策略並取得結果
    df = start_strategy(target_stock, start_date, end_date, stopLoss)

    # 繪製 KD 指標圖
    draw_KD_indicator(df)


if __name__ == "__main__":
    main()
