import talib
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime


def init(df):
    # 計算雙均線指標
    df["MA5"] = talib.SMA(df["close"].values.flatten(), timeperiod=5)
    df["MA20"] = talib.SMA(df["close"].values.flatten(), timeperiod=20)


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

    # 計算雙均線指標
    df["MA5"] = talib.SMA(df["close"].values.flatten(), timeperiod=5)
    df["MA20"] = talib.SMA(df["close"].values.flatten(), timeperiod=20)

    # 初始化
    flag = 0
    buyPrice = 0
    trades = []
    stopLoss = -stopLoss  # 把停損轉為負數

    for i in range(20, len(df)):
        current_price = df["close"].iloc[i].item()
        current_ma5 = df["MA5"].iloc[i]
        current_ma20 = df["MA20"].iloc[i]
        prev_ma5 = df["MA5"].iloc[i - 1]
        prev_ma20 = df["MA20"].iloc[i - 1]

        # 買入訊號：黃金交叉（MA5 上穿 MA20）
        if current_ma5 > current_ma20 and prev_ma5 <= prev_ma20 and flag == 0:
            flag = 1
            buyPrice = current_price
            buy_date = df.index[i]
            print(
                f"Buy Date: {buy_date.strftime('%Y-%m-%d')}, Buy Price: {buyPrice:.2f}, MA5: {current_ma5:.2f}, MA20: {current_ma20:.2f}"
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

        # 賣出訊號：死亡交叉（MA5 下穿 MA20）
        elif current_ma5 < current_ma20 and prev_ma5 >= prev_ma20 and flag == 1:
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
                f"Sell Date: {sell_date.strftime('%Y-%m-%d')}, Sell Price: {sellPrice:.2f}, P&L: {profit:.2f} ({profit_pct:.2f}%), MA5: {current_ma5:.2f}, MA20: {current_ma20:.2f}"
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


def draw_MA_indicator(df):
    fig, ax = plt.subplots(figsize=(14, 8))

    # Price trend
    ax.plot(
        df.index,
        df["close"].values.flatten(),
        label="Close Price",
        color="black",
        linewidth=1.5,
    )

    # Moving Averages
    ax.plot(df.index, df["MA5"], label="MA5", color="blue", linewidth=1.5)
    ax.plot(df.index, df["MA20"], label="MA20", color="orange", linewidth=1.5)

    ax.set_title("Moving Average Strategy (MA5 & MA20)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Price", fontsize=12)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


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
