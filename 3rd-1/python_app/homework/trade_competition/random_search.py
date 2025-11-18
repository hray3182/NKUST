"""
隨機搜尋最佳策略組合
從策略庫中隨機選擇1-3個策略組成組合，找出最佳組合
"""
import random
import itertools
import copy
import os
import pickle
import hashlib
import yfinance as yf
import pandas as pd
from strategy_combination import StrategyCombination
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
import time


class RandomSearch:
    """隨機搜尋最佳策略組合"""

    def __init__(self, strategy_classes, target_stock, start_date, end_date, stop_loss=0.1, cache_dir="data_cache"):
        """
        初始化隨機搜尋

        Args:
            strategy_classes: 策略類別列表（整個策略庫）
            target_stock: 股票代號
            start_date: 開始日期
            end_date: 結束日期
            stop_loss: 停損點
        """
        self.strategy_classes = strategy_classes
        self.target_stock = target_stock
        self.start_date = start_date
        self.end_date = end_date
        self.stop_loss = stop_loss
        self.cache_dir = cache_dir
        
        os.makedirs(self.cache_dir, exist_ok=True)
        
        self.df = self._load_or_download_data(target_stock, start_date, end_date)
        
        self.precomputed_strategies = {}
        for strategy_class in strategy_classes:
            strategy = strategy_class(target_stock, start_date, end_date, stop_loss)
            df_copy = self.df.copy()
            strategy.calculate_indicators(df_copy)
            self.precomputed_strategies[strategy_class] = strategy
    
    def _get_cache_key(self, target_stock, start_date, end_date):
        """生成緩存鍵"""
        date_str = f"{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}"
        key_string = f"{target_stock}_{date_str}"
        cache_key = hashlib.md5(key_string.encode()).hexdigest()
        return cache_key
    
    def _load_or_download_data(self, target_stock, start_date, end_date):
        """
        載入緩存的數據或下載新數據
        
        Returns:
            DataFrame: 股票數據
        """
        cache_key = self._get_cache_key(target_stock, start_date, end_date)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    df = pickle.load(f)
                return df
            except Exception:
                pass
        
        df = yf.download(target_stock, start_date, end_date, auto_adjust=True, progress=False)
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
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)
        df = df.sort_index()
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(df, f)
        except Exception:
            pass
        
        return df.copy()

    def generate_all_combinations(self):
        """
        產生所有可能的策略組合（1-3個策略）

        Returns:
            策略組合列表
        """
        combinations = []
        
        for strategy_class in self.strategy_classes:
            combinations.append([strategy_class])
        
        if len(self.strategy_classes) >= 2:
            for combo in itertools.combinations(self.strategy_classes, 2):
                combinations.append(list(combo))
        
        if len(self.strategy_classes) >= 3:
            for combo in itertools.combinations(self.strategy_classes, 3):
                combinations.append(list(combo))
        
        return combinations

    def _evaluate_combination(self, combo):
        """
        評估單一策略組合（用於並行處理）

        Args:
            combo: 策略類別列表

        Returns:
            (策略名稱列表, 報酬) 或 None（如果失敗）
        """
        try:
            strategies = [copy.deepcopy(self.precomputed_strategies[cls]) for cls in combo]
            
            df_copy = self.df.copy()
            for strategy in strategies:
                strategy.df = df_copy

            combination = StrategyCombination(
                strategies, self.target_stock, self.start_date, self.end_date, self.stop_loss
            )

            profit = combination.backtest_with_data(df_copy, verbose=False, skip_indicator_calculation=True)

            strategy_names = combination.get_strategy_names()
            profit_float = float(profit) if profit is not None else 0.0
            
            return {
                "strategies": strategy_names,
                "profit": profit_float,
                "combination": combo
            }
        except Exception:
            return None

    def random_search(self, n_iterations=None, n_jobs=None):
        """
        搜尋最佳策略組合（測試所有組合，使用多進程並行處理）

        Args:
            n_iterations: 搜尋迭代次數
            n_jobs: 並行處理的進程數，None 表示使用所有可用 CPU 核心

        Returns:
            最佳組合資訊（策略類別列表、報酬、找到最佳組合的嘗試次數）
        """
        search_start_time = time.time()
        all_combinations = self.generate_all_combinations()
        
        tested_combinations = all_combinations
        
        if n_jobs is None:
            n_jobs = max(1, cpu_count())
        
        results = []
        best_profit = float('-inf')
        best_combination = None
        best_strategy_names = None
        best_found_at_attempt = None
        completed = 0
        
        with ThreadPoolExecutor(max_workers=n_jobs) as executor:
            future_to_combo = {}
            for idx, combo in enumerate(tested_combinations, 1):
                future = executor.submit(self._evaluate_combination, combo)
                future_to_combo[future] = (combo, idx)
            
            for future in as_completed(future_to_combo):
                completed += 1
                combo, attempt_number = future_to_combo[future]
                result = future.result()
                
                if result:
                    result["attempt_number"] = attempt_number
                    results.append(result)
                    result_profit = float(result["profit"])
                    if result_profit > best_profit:
                        best_profit = result_profit
                        best_combination = result["combination"]
                        best_strategy_names = result["strategies"]
        
        results.sort(key=lambda x: (-float(x["profit"]), x.get("attempt_number", float('inf'))))
        
        if results:
            best_result = results[0]
            best_profit = float(best_result["profit"])
            best_combination = best_result["combination"]
            best_strategy_names = best_result["strategies"]
            best_found_at_attempt = best_result.get("attempt_number", None)
        else:
            best_profit = float('-inf')
            best_combination = None
            best_strategy_names = None
            best_found_at_attempt = None
        
        return {
            "best_combination": best_combination,
            "best_strategy_names": best_strategy_names,
            "best_profit": best_profit,
            "best_found_at_attempt": best_found_at_attempt,
            "all_results": results
        }



