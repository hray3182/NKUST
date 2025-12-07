"""
主程式：交易競賽策略組合搜尋
對三個不同趨勢的股票進行回測，找出最佳策略組合
"""
from datetime import datetime
import time
import random
import os
import sys
from strategy_evaluator import StrategyEvaluator
from random_search import RandomSearch
from strategies import (
    MAStrategy, BBANDSStrategy, KDStrategy, MACDStrategy, RSIStrategy,
    EMAStrategy, WilliamsRStrategy, CCIStrategy, ADXStrategy, 
    OBVStrategy, ATRStrategy, TripleMAStrategy, GridStrategy,
    MomentumReversalStrategy
)


class Tee:
    """同時輸出到多個文件對象的類"""
    def __init__(self, *files):
        self.files = files
    
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()
    
    def flush(self):
        for f in self.files:
            f.flush()


def main():
    """主程式"""
    random.seed(69)
    
    result_dir = "result"
    os.makedirs(result_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(result_dir, f"{timestamp}.log")
    
    log_file = open(log_filename, 'w', encoding='utf-8')
    
    original_stdout = sys.stdout
    tee = Tee(sys.stdout, log_file)
    sys.stdout = tee
    
    try:
        program_start_time = time.time()
        
        stop_loss = 0.1
        
        test_cases = [
        {
            "name": "上漲趨勢",
            "stock": "2330.TW",
            "start_date": datetime(2013, 1, 1),
            "end_date": datetime(2022, 12, 31),
        },
        {
            "name": "盤整趨勢",
            "stock": "2412.TW",
            "start_date": datetime(2013, 1, 1),
            "end_date": datetime(2022, 12, 31),
        },
        {
            "name": "下跌趨勢",
            "stock": "2498.TW",
            "start_date": datetime(2013, 1, 1),
            "end_date": datetime(2022, 12, 31),
        },
        ]
        
        results_summary = []
        
        print("=" * 80)
        print("交易競賽策略組合搜尋系統")
        print(f"開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        for case_idx, case in enumerate(test_cases, 1):
            case_start_time = time.time()
            print("\n" + "=" * 80)
            print(f"測試案例 {case_idx}/{len(test_cases)}: {case['name']}")
            print(f"股票代號: {case['stock']}")
            print(f"回測期間: {case['start_date'].strftime('%Y-%m-%d')} ~ {case['end_date'].strftime('%Y-%m-%d')}")
            print(f"開始時間: {datetime.now().strftime('%H:%M:%S')}")
            print("=" * 80)
            
            print("\n【隨機搜尋最佳策略組合】")
            print("-" * 80)
            
            all_strategy_classes = [
                MAStrategy, BBANDSStrategy, KDStrategy, MACDStrategy, RSIStrategy,
                EMAStrategy, WilliamsRStrategy, CCIStrategy, ADXStrategy, 
                OBVStrategy, ATRStrategy, TripleMAStrategy, GridStrategy,
                MomentumReversalStrategy
            ]
            
            init_start = time.time()
            searcher = RandomSearch(
                all_strategy_classes,
                case["stock"],
                case["start_date"],
                case["end_date"],
                stop_loss
            )
            init_time = time.time() - init_start
            print(f"初始化完成，耗時 {init_time:.2f} 秒")
            
            search_start = time.time()
            search_result = searcher.random_search(n_iterations=None)
            search_time = time.time() - search_start
            print(f"搜尋完成，耗時 {search_time:.2f} 秒")
            
            best_profit = search_result["best_profit"]
            best_strategy_names = search_result["best_strategy_names"]
            best_found_at_attempt = search_result.get("best_found_at_attempt", None)
            
            best_profit_float = float(best_profit) if best_profit != float('-inf') else 0.0
            
            results_summary.append({
                "case_name": case["name"],
                "stock": case["stock"],
                "best_profit": best_profit_float,
                "best_strategies": best_strategy_names,
                "best_found_at_attempt": best_found_at_attempt
            })
            
            case_time = time.time() - case_start_time
            print("\n" + "=" * 80)
            print(f"【{case['name']}】最佳策略組合結果")
            print("=" * 80)
            print(f"最佳策略組合: {' + '.join(best_strategy_names)}")
            print(f"最佳報酬: {best_profit_float:.2f} 元")
            if best_found_at_attempt is not None:
                print(f"找到最佳組合的嘗試次數: 第 {best_found_at_attempt} 次嘗試")
            print(f"本案例總耗時: {case_time:.2f} 秒")
            print("=" * 80)
        
        print("\n" + "=" * 80)
        print("最終結果摘要")
        print("=" * 80)
        print(f"{'測試案例':<15} {'股票代號':<12} {'最佳報酬':>15} {'找到次數':>10} {'最佳策略組合':<50}")
        print("-" * 80)
        
        for result in results_summary:
            strategies_str = " + ".join(result["best_strategies"])
            attempt_info = f"第{result.get('best_found_at_attempt', 'N/A')}次" if result.get('best_found_at_attempt') else "N/A"
            print(f"{result['case_name']:<15} {result['stock']:<12} {result['best_profit']:>15.2f} 元 {attempt_info:>10} {strategies_str:<50}")
        
        print("=" * 80)
        
        print("\n" + "=" * 80)
        print("結果")
        print("=" * 80)
        for result in results_summary:
            print(f"{result['case_name']}回測區間最佳報酬: {result['best_profit']:.2f} 元")
        print("=" * 80)
        
        total_time = time.time() - program_start_time
        print(f"\n總執行時間: {total_time:.2f} 秒 ({total_time/60:.2f} 分鐘)")
        print(f"結束時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
    
    finally:
        sys.stdout = original_stdout
        log_file.close()
        print(f"\n結果已保存到: {log_filename}")


if __name__ == "__main__":
    main()

