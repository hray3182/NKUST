"""
策略評估器
評估所有策略的表現，選出最佳的3個策略
"""
from strategies import (
    MAStrategy, BBANDSStrategy, KDStrategy, MACDStrategy, RSIStrategy,
    EMAStrategy, WilliamsRStrategy, CCIStrategy, ADXStrategy, 
    OBVStrategy, ATRStrategy, TripleMAStrategy, GridStrategy,
    MomentumReversalStrategy
)
from strategy_combination import StrategyCombination
from datetime import datetime


class StrategyEvaluator:
    """策略評估器"""

    def __init__(self):
        """初始化所有策略類別"""
        self.strategy_classes = [
            MAStrategy,
            BBANDSStrategy,
            KDStrategy,
            MACDStrategy,
            RSIStrategy,
            EMAStrategy,
            WilliamsRStrategy,
            CCIStrategy,
            ADXStrategy,
            OBVStrategy,
            ATRStrategy,
            TripleMAStrategy,
            GridStrategy,
            MomentumReversalStrategy,
        ]
        self.strategy_names = [cls.__name__ for cls in self.strategy_classes]

    def evaluate_single_strategy(self, strategy_class, target_stock, start_date, end_date, stop_loss=0.1):
        """
        評估單一策略

        Args:
            strategy_class: 策略類別
            target_stock: 股票代號
            start_date: 開始日期
            end_date: 結束日期
            stop_loss: 停損點

        Returns:
            總報酬（已扣除交易成本）
        """
        # 建立策略組合（只有一個策略）
        strategy = strategy_class(target_stock, start_date, end_date, stop_loss)
        combination = StrategyCombination([strategy], target_stock, start_date, end_date, stop_loss)
        
        # 執行回測
        total_profit = combination.backtest(verbose=False)
        
        return total_profit

    def evaluate_all_strategies(self, target_stock, start_date, end_date, stop_loss=0.1):
        """
        評估所有策略

        Args:
            target_stock: 股票代號
            start_date: 開始日期
            end_date: 結束日期
            stop_loss: 停損點

        Returns:
            策略名稱和報酬的字典列表，按報酬排序
        """
        results = []
        
        print(f"\n評估策略在 {target_stock} 的表現...")
        print("=" * 80)
        
        for strategy_class, strategy_name in zip(self.strategy_classes, self.strategy_names):
            try:
                profit = self.evaluate_single_strategy(
                    strategy_class, target_stock, start_date, end_date, stop_loss
                )
                results.append({
                    "name": strategy_name,
                    "class": strategy_class,
                    "profit": profit
                })
                print(f"{strategy_name:<25} 報酬: {profit:>12.2f} 元")
            except Exception as e:
                print(f"{strategy_name:<25} 評估失敗: {str(e)}")
                results.append({
                    "name": strategy_name,
                    "class": strategy_class,
                    "profit": float('-inf')
                })
        
        # 按報酬排序（降序）
        results.sort(key=lambda x: x["profit"], reverse=True)
        
        print("\n" + "=" * 80)
        print("策略排名（按報酬排序）:")
        print("-" * 80)
        for i, result in enumerate(results, 1):
            print(f"{i:2d}. {result['name']:<25} 報酬: {result['profit']:>12.2f} 元")
        
        return results

    def select_top_strategies(self, target_stock, start_date, end_date, stop_loss=0.1, top_n=3):
        """
        選出表現最好的N個策略

        Args:
            target_stock: 股票代號
            start_date: 開始日期
            end_date: 結束日期
            stop_loss: 停損點
            top_n: 選出前N個策略

        Returns:
            最佳策略類別列表
        """
        results = self.evaluate_all_strategies(target_stock, start_date, end_date, stop_loss)
        
        top_strategies = results[:top_n]
        
        print(f"\n選出前 {top_n} 個最佳策略:")
        print("-" * 80)
        for i, result in enumerate(top_strategies, 1):
            print(f"{i}. {result['name']} (報酬: {result['profit']:.2f} 元)")
        
        return [result["class"] for result in top_strategies]


