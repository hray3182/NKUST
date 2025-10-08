import talib
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime


def init(df):
    # 計算 KD 指標
    df["K"], df["D"] = talib.STOCH(
        df["high"].values.flatten(),
        df["low"].values.flatten(),
        df["close"].values.flatten(),
        fastk_period=9,
        slowk_period=3,
        slowd_period=3,
    )


def start_strategy(target_stock, start_date, end_date, stopLoss=0.1):
    # 下載股票資料
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

    # 計算 KD 指標
    df["K"], df["D"] = talib.STOCH(
        df["high"].values.flatten(),
        df["low"].values.flatten(),
        df["close"].values.flatten(),
        fastk_period=9,
        slowk_period=3,
        slowd_period=3,
    )

    # 初始化
    flag = 0
    buyPrice = 0
    trades = []
    stopLoss = -stopLoss  # 把停損轉為負數

    for i in range(15, len(df)):
        current_price = df["close"].iloc[i].item()
        current_k = df["K"].iloc[i]
        current_d = df["D"].iloc[i]
        prev_k = df["K"].iloc[i - 1]
        prev_d = df["D"].iloc[i - 1]

        # 買入訊號：KD 黃金交叉（K 上穿 D）
        if current_k > current_d and prev_k <= prev_d and flag == 0:
            flag = 1
            buyPrice = current_price
            buy_date = df.index[i]
            print(
                f"Buy Date: {buy_date.strftime('%Y-%m-%d')}, Buy Price: {buyPrice:.2f}"
            )

        # 持有期間先檢查停損
        elif flag == 1 and (current_price - buyPrice) / buyPrice <= stopLoss:
            flag = 0
            sellPrice = current_price
            sell_date = df.index[i]
            profit = sellPrice - buyPrice
            profit_pct = (profit / buyPrice) * 100

            trades.append(
                {
                    "Buy Date": buy_date,
                    "Buy Price": buyPrice,
                    "Sell Date": sell_date,
                    "Sell Price": sellPrice,
                    "Profit": profit,
                    "Profit %": profit_pct,
                    "Exit Type": "Stop Loss",
                }
            )

            print(
                f"[STOP LOSS] Sell Date: {sell_date.strftime('%Y-%m-%d')}, Sell Price: {sellPrice:.2f}, P&L: {profit:.2f} ({profit_pct:.2f}%)"
            )

        # 賣出訊號：KD 死亡交叉（K 下穿 D）
        elif current_k < current_d and prev_k >= prev_d and flag == 1:
            flag = 0
            sellPrice = current_price
            sell_date = df.index[i]
            profit = sellPrice - buyPrice
            profit_pct = (profit / buyPrice) * 100

            trades.append(
                {
                    "Buy Date": buy_date,
                    "Buy Price": buyPrice,
                    "Sell Date": sell_date,
                    "Sell Price": sellPrice,
                    "Profit": profit,
                    "Profit %": profit_pct,
                    "Exit Type": "Signal",
                }
            )

            print(
                f"Sell Date: {sell_date.strftime('%Y-%m-%d')}, Sell Price: {sellPrice:.2f}, P&L: {profit:.2f} ({profit_pct:.2f}%)"
            )

    # 顯示交易摘要
    if trades:
        trades_df = pd.DataFrame(trades)
        print("\n=== Trading Summary ===")
        print(trades_df.to_string(index=False))
        print(f"\nTotal Trades: {len(trades)}")
        print(f"Total Profit: {trades_df['Profit'].sum():.2f}")
        print(f"Average Profit per Trade: {trades_df['Profit'].mean():.2f}")
        print(f"Win Rate: {(trades_df['Profit'] > 0).sum() / len(trades) * 100:.2f}%")
        print(f"\nExit by Signal: {(trades_df['Exit Type'] == 'Signal').sum()}")
        print(f"Exit by Stop Loss: {(trades_df['Exit Type'] == 'Stop Loss').sum()}")
    else:
        print("No trades executed.")

    return df


def draw_KD_indicator(df):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    # Top chart: Price trend
    ax1.plot(
        df.index,
        df["close"].values.flatten(),
        label="Close Price",
        color="black",
        linewidth=1.5,
    )
    ax1.set_title("Stock Price Chart", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Price", fontsize=12)
    ax1.legend(loc="best")
    ax1.grid(True, alpha=0.3)

    # Bottom chart: KD indicator
    ax2.plot(df.index, df["K"], label="K Line", color="blue", linewidth=1.5)
    ax2.plot(df.index, df["D"], label="D Line", color="orange", linewidth=1.5)

    # Overbought/Oversold zones
    ax2.axhline(y=80, color="red", linestyle="--", alpha=0.5)
    ax2.axhline(y=20, color="green", linestyle="--", alpha=0.5)
    ax2.axhline(y=50, color="gray", linestyle=":", alpha=0.3)

    # Fill zones
    ax2.fill_between(df.index, 80, 100, alpha=0.1, color="red")
    ax2.fill_between(df.index, 0, 20, alpha=0.1, color="green")

    ax2.set_title("KD Stochastic Indicator", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Date", fontsize=12)
    ax2.set_ylabel("KD Value", fontsize=12)
    ax2.legend(loc="best")
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 100)

    plt.tight_layout()
    plt.show()


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
