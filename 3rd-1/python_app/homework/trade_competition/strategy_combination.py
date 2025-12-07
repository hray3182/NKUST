"""
策略組合類別
支援組合最多3個策略，使用OR邏輯判斷買賣訊號
"""
import pandas as pd
import yfinance as yf
from strategies import BaseStrategy


class StrategyCombination:
    """策略組合類別，可組合最多3個策略"""

    def __init__(self, strategies, target_stock=None, start_date=None, end_date=None, stop_loss=0.1):
        """
        初始化策略組合

        Args:
            strategies: 策略列表（最多3個）
            target_stock: 股票代號
            start_date: 資料開始日期
            end_date: 資料結束日期
            stop_loss: 停損點
        """
        if len(strategies) > 3:
            raise ValueError("最多只能組合3個策略")
        
        self.strategies = strategies
        self.target_stock = target_stock
        self.start_date = start_date
        self.end_date = end_date
        self.stop_loss = stop_loss
        self.df = None
        self.trades = []
        
        # 交易成本參數（台灣股票市場）
        self.commission_rate = 0.001425  # 手續費 0.1425%
        self.tax_rate = 0.003  # 證券交易稅 0.3%（僅賣出時）
        self.shares = 1  # 每次交易股數（買進1股）

    def download_data(self, target_stock, start_date, end_date):
        """下載股票資料"""
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
        self.df = df
        return df

    def calculate_all_indicators(self, df):
        """計算所有策略的技術指標"""
        for strategy in self.strategies:
            strategy.df = df
            strategy.calculate_indicators(df)

    def get_start_index(self):
        """取得開始交易的索引位置（取所有策略中的最大值）"""
        return max(strategy.get_start_index() for strategy in self.strategies)

    def check_buy_signal(self, i):
        """檢查買入訊號：任一策略發出買入訊號即買入（OR邏輯）"""
        return any(strategy.check_buy_signal(i) for strategy in self.strategies)

    def check_sell_signal(self, i):
        """檢查賣出訊號：任一策略發出賣出訊號即賣出（OR邏輯）"""
        return any(strategy.check_sell_signal(i) for strategy in self.strategies)

    def check_stop_loss(self, current_price, buy_price, stop_loss):
        """檢查是否觸及停損點"""
        return (current_price - buy_price) / buy_price <= stop_loss

    def calculate_trading_costs(self, price, is_buy=True):
        """
        計算交易成本
        
        公式：
        買進：證券手續費 = 股票買進股價 × 股數 × 0.1425%
        賣出：證券手續費 + 證券交易稅 = (股票賣出股價 × 股數 × 0.1425%) + (股票賣出股價 × 股數 × 0.3%)
        
        Args:
            price: 交易價格
            is_buy: True為買進，False為賣出
        
        Returns:
            交易成本（元）
        """
        if is_buy:
            return price * self.shares * self.commission_rate
        else:
            return price * self.shares * (self.commission_rate + self.tax_rate)

    def backtest(self, target_stock=None, start_date=None, end_date=None, stop_loss=None, verbose=False):
        """
        執行回測

        Args:
            target_stock: 股票代號
            start_date: 資料開始日期
            end_date: 資料結束日期
            stop_loss: 停損點
            verbose: 是否顯示詳細資訊

        Returns:
            總報酬（已扣除交易成本，單位：元）
        """
        target_stock = target_stock or self.target_stock
        start_date = start_date or self.start_date
        end_date = end_date or self.end_date
        stop_loss = stop_loss if stop_loss is not None else self.stop_loss

        df = self.download_data(target_stock, start_date, end_date)

        self.calculate_all_indicators(df)

        # 初始化
        flag = 0  # 0: 空倉, 1: 持倉
        buy_price = 0
        buy_price_with_cost = 0
        buy_cost = 0
        buy_date = None
        self.trades = []
        stop_loss_value = -stop_loss

        start_idx = self.get_start_index()
        
        close_prices = df["close"].values
        df_index = df.index

        for i in range(start_idx, len(df)):
            current_price = close_prices[i]

            if flag == 0 and self.check_buy_signal(i):
                flag = 1
                buy_price = current_price
                buy_date = df_index[i]
                
                buy_cost = self.calculate_trading_costs(buy_price, is_buy=True)
                buy_price_with_cost = buy_price + buy_cost
                
                if verbose:
                    print(f"Buy Date: {buy_date.strftime('%Y-%m-%d')}, "
                          f"Buy Price: {buy_price:.2f}, Cost: {buy_cost:.2f}")

            elif flag == 1 and self.check_stop_loss(current_price, buy_price, stop_loss_value):
                flag = 0
                
                sell_cost = self.calculate_trading_costs(current_price, is_buy=False)
                sell_price_after_cost = current_price - sell_cost
                
                net_profit = sell_price_after_cost - buy_price_with_cost
                
                self.trades.append({
                    "Buy Date": buy_date,
                    "Buy Price": buy_price,
                    "Buy Cost": buy_cost,
                    "Sell Date": df_index[i],
                    "Sell Price": current_price,
                    "Sell Cost": sell_cost,
                    "Net Profit": net_profit,
                    "Exit Type": "Stop Loss"
                })
                
                if verbose:
                    print(f"[STOP LOSS] Sell Date: {df_index[i].strftime('%Y-%m-%d')}, "
                          f"Sell Price: {current_price:.2f}, Cost: {sell_cost:.2f}, "
                          f"Net Profit: {net_profit:.2f}")

            elif flag == 1 and self.check_sell_signal(i):
                flag = 0
                
                sell_cost = self.calculate_trading_costs(current_price, is_buy=False)
                sell_price_after_cost = current_price - sell_cost
                
                net_profit = sell_price_after_cost - buy_price_with_cost
                
                self.trades.append({
                    "Buy Date": buy_date,
                    "Buy Price": buy_price,
                    "Buy Cost": buy_cost,
                    "Sell Date": df_index[i],
                    "Sell Price": current_price,
                    "Sell Cost": sell_cost,
                    "Net Profit": net_profit,
                    "Exit Type": "Signal"
                })
                
                if verbose:
                    print(f"Sell Date: {df_index[i].strftime('%Y-%m-%d')}, "
                          f"Sell Price: {current_price:.2f}, Cost: {sell_cost:.2f}, "
                          f"Net Profit: {net_profit:.2f}")

        total_profit = sum(trade["Net Profit"] for trade in self.trades) if self.trades else 0.0

        return total_profit

    def backtest_with_data(self, df, stop_loss=None, verbose=False, skip_indicator_calculation=False):
        """
        執行回測（使用預先下載的資料，避免重複下載）

        Args:
            df: 預先下載的股票資料 DataFrame
            stop_loss: 停損點
            verbose: 是否顯示詳細資訊
            skip_indicator_calculation: 是否跳過指標計算（如果指標已預先計算）

        Returns:
            總報酬（已扣除交易成本，單位：元）
        """
        stop_loss = stop_loss if stop_loss is not None else self.stop_loss

        self.df = df

        if not skip_indicator_calculation:
            self.calculate_all_indicators(df)

        flag = 0
        buy_price = 0
        buy_price_with_cost = 0
        buy_cost = 0
        buy_date = None
        stop_loss_value = -stop_loss

        start_idx = self.get_start_index()

        close_prices = df["close"].values
        df_index = df.index
        total_profit = 0.0

        for i in range(start_idx, len(df)):
            current_price = close_prices[i]

            if flag == 0 and self.check_buy_signal(i):
                flag = 1
                buy_price = current_price
                buy_date = df_index[i]
                
                buy_cost = self.calculate_trading_costs(buy_price, is_buy=True)
                buy_price_with_cost = buy_price + buy_cost

                if verbose:
                    print(f"Buy Date: {buy_date.strftime('%Y-%m-%d')}, "
                          f"Buy Price: {buy_price:.2f}, Cost: {buy_cost:.2f}")

            elif flag == 1 and self.check_stop_loss(current_price, buy_price, stop_loss_value):
                flag = 0

                sell_cost = self.calculate_trading_costs(current_price, is_buy=False)
                sell_price_after_cost = current_price - sell_cost

                net_profit = sell_price_after_cost - buy_price_with_cost
                total_profit += net_profit

                if verbose:
                    print(f"[STOP LOSS] Sell Date: {df_index[i].strftime('%Y-%m-%d')}, "
                          f"Sell Price: {current_price:.2f}, Cost: {sell_cost:.2f}, "
                          f"Net Profit: {net_profit:.2f}")

            elif flag == 1 and self.check_sell_signal(i):
                flag = 0

                sell_cost = self.calculate_trading_costs(current_price, is_buy=False)
                sell_price_after_cost = current_price - sell_cost

                net_profit = sell_price_after_cost - buy_price_with_cost
                total_profit += net_profit

                if verbose:
                    print(f"Sell Date: {df_index[i].strftime('%Y-%m-%d')}, "
                          f"Sell Price: {current_price:.2f}, Cost: {sell_cost:.2f}, "
                          f"Net Profit: {net_profit:.2f}")

        return total_profit

    def get_total_profit(self):
        """取得總報酬（已扣除交易成本）"""
        if not self.trades:
            return 0.0
        return sum(trade["Net Profit"] for trade in self.trades)

    def get_strategy_names(self):
        """取得策略名稱列表"""
        return [strategy.__class__.__name__ for strategy in self.strategies]

