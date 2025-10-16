import talib
import matplotlib.pyplot as plt
from datetime import datetime
from .base_strategy import BaseStrategy


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


# 向後相容的函數介面
def init(df):
    """計算布林帶指標"""
    df["Upper"], df["Middle"], df["Lower"] = talib.BBANDS(
        df["close"].values.flatten(), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
    )


def start_strategy(target_stock, start_date, end_date, stopLoss=0.1):
    """執行布林帶策略（向後相容）"""
    strategy = BBANDSStrategy()
    return strategy.start_strategy(target_stock, start_date, end_date, stopLoss)


def draw_BBANDS_indicator(df):
    """繪製布林帶指標圖（向後相容）"""
    strategy = BBANDSStrategy()
    strategy.df = df
    strategy.draw_indicator()


def main():
    target_stock = "2498.TW"  # 分析公司代號 e.g., '2330.TW'是台積電
    start_date = datetime(2021, 1, 1)  # 設定資料開始日期
    end_date = datetime(2021, 7, 19)  # 設定資料結束日期
    stopLoss = 0.1  # 停損點，指-10%會強制賣出

    # 執行策略並取得結果
    df = start_strategy(target_stock, start_date, end_date, stopLoss)

    # 繪製布林帶指標圖
    draw_BBANDS_indicator(df)


if __name__ == "__main__":
    main()
