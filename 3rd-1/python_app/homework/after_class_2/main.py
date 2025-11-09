import numpy as np
import pandas as pd
import talib #技術指標套件
import yfinance as yf #股價下載套件
from datetime import datetime
import matplotlib.pyplot as plt #畫圖套

target_stock = '2330.TW' #分析公司代號 e.g., '2330.TW'是台積電
start_date = datetime(2024, 1, 1) #設定資料開始日期
end_date = datetime(2024, 12, 31) #設定資料結束日期
#將資料放到Dataframe裡面
df = yf.download(target_stock, start_date, end_date)
print(df.head())
#保留所需欄位
df = df[['Open','High','Low','Close','Volume']]
print(df.head())
#更改欄位名稱，將第一個字母改為小寫
df.rename(columns={'Close':'close', 'High':'high', 'Low':'low', 'Open':'open','Volume':'volume' }, inplace = True) 

closePrices = df['close'].values.ravel() #從df取得收盤價，並轉呈1D陣列
macd, signal, histogram = talib.MACD(closePrices)

#設定x, y軸資料
xpt = df.index

print(xpt)

def drawSeries(xValues, macd, signal, histogram, target_stock):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), 
                                     gridspec_kw={'height_ratios': [2, 1]})
    
    # 上圖：MACD Line 和 Signal Line
    ax1.set_title(f'{target_stock} - MACD', size=15)
    ax1.plot(xValues, macd, '-', color='blue', label='MACD Line', linewidth=1.5)
    ax1.plot(xValues, signal, '-', color='red', label='Signal Line', linewidth=1.5)
    ax1.axhline(y=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax1.legend(loc="best", fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylabel('Value', fontsize=11)
    
    # 下圖：Histogram
    ax2.set_title('MACD Histogram', size=12)
    colors = ['red' if val >= 0 else 'green' for val in histogram]
    ax2.bar(xValues, histogram, color=colors, alpha=0.6, width=1)
    ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.8)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylabel('Histogram', fontsize=11)
    ax2.set_xlabel('Date', fontsize=11)
    
    plt.tight_layout()
    plt.show()


drawSeries(xpt, macd, signal, histogram, target_stock)