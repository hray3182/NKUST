import talib
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime


def init(df):
    # 計算 MACD 指標
    df["MACD"], df["Signal"], df["Hist"] = talib.MACD(
        df["close"].values.flatten(),
        fastperiod=12,
        slowperiod=26,
        signalperiod=9,
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

    # 計算 MACD 指標
    df["MACD"], df["Signal"], df["Hist"] = talib.MACD(
        df["close"].values.flatten(),
        fastperiod=12,
        slowperiod=26,
        signalperiod=9,
    )

    # 初始化
    flag = 0
    buyPrice = 0
    trades = []
    stopLoss = -stopLoss  # 把停損轉為負數

    for i in range(26, len(df)):
        current_price = df["close"].iloc[i].item()
        current_macd = df["MACD"].iloc[i]
        current_signal = df["Signal"].iloc[i]
        prev_macd = df["MACD"].iloc[i - 1]
        prev_signal = df["Signal"].iloc[i - 1]

        # 買入訊號：MACD 黃金交叉（MACD 上穿 Signal）
        if current_macd > current_signal and prev_macd <= prev_signal and flag == 0:
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

        # 賣出訊號：MACD 死亡交叉（MACD 下穿 Signal）
        elif current_macd < current_signal and prev_macd >= prev_signal and flag == 1:
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


def draw_MACD_indicator(df):
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

    # Bottom chart: MACD indicator
    ax2.plot(df.index, df["MACD"], label="MACD", color="blue", linewidth=1.5)
    ax2.plot(df.index, df["Signal"], label="Signal", color="orange", linewidth=1.5)

    # MACD histogram
    colors = ["red" if val < 0 else "green" for val in df["Hist"]]
    ax2.bar(df.index, df["Hist"], label="Histogram", color=colors, alpha=0.3, width=0.8)

    # Zero line
    ax2.axhline(y=0, color="gray", linestyle="-", alpha=0.5)

    ax2.set_title("MACD Indicator", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Date", fontsize=12)
    ax2.set_ylabel("MACD Value", fontsize=12)
    ax2.legend(loc="best")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


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
