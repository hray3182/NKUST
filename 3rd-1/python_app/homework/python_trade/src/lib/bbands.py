import talib
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime


def init(df):
    # 計算布林帶指標
    df["Upper"], df["Middle"], df["Lower"] = talib.BBANDS(
        df["close"].values.flatten(), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
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

    # 計算布林帶指標
    df["Upper"], df["Middle"], df["Lower"] = talib.BBANDS(
        df["close"].values.flatten(), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
    )

    # 初始化
    flag = 0
    buyPrice = 0
    trades = []
    stopLoss = -stopLoss  # 把停損轉為負數

    for i in range(20, len(df)):
        current_price = df["close"].iloc[i].item()
        prev_price = df["close"].iloc[i - 1].item()
        lower_band = df["Lower"].iloc[i]
        upper_band = df["Upper"].iloc[i]
        prev_lower = df["Lower"].iloc[i - 1]
        prev_upper = df["Upper"].iloc[i - 1]

        # 買入訊號：價格從下軌反彈（前一天觸及或跌破下軌，當天回到下軌上方）
        if prev_price <= prev_lower and current_price > lower_band and flag == 0:
            flag = 1
            buyPrice = current_price
            buy_date = df.index[i]
            print(
                f"Buy Date: {buy_date.strftime('%Y-%m-%d')}, Buy Price: {buyPrice:.2f}, Lower Band: {lower_band:.2f}"
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

        # 賣出訊號：價格觸及或突破上軌
        elif current_price >= upper_band and flag == 1:
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
                f"Sell Date: {sell_date.strftime('%Y-%m-%d')}, Sell Price: {sellPrice:.2f}, P&L: {profit:.2f} ({profit_pct:.2f}%), Upper Band: {upper_band:.2f}"
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


def draw_BBANDS_indicator(df):
    fig, ax = plt.subplots(figsize=(14, 8))

    # Price trend
    ax.plot(
        df.index,
        df["close"].values.flatten(),
        label="Close Price",
        color="black",
        linewidth=1.5,
    )

    # Bollinger Bands
    ax.plot(df.index, df["Upper"], label="Upper Band", color="red", linestyle="--", linewidth=1)
    ax.plot(df.index, df["Middle"], label="Middle Band (SMA20)", color="blue", linestyle="-", linewidth=1)
    ax.plot(df.index, df["Lower"], label="Lower Band", color="green", linestyle="--", linewidth=1)

    # Fill between bands
    ax.fill_between(df.index, df["Lower"], df["Upper"], alpha=0.1, color="gray")

    ax.set_title("Bollinger Bands Strategy", fontsize=14, fontweight="bold")
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

    # 繪製布林帶指標圖
    draw_BBANDS_indicator(df)


if __name__ == "__main__":
    main()
