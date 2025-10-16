"""
主程式：執行所有技術指標交易策略
"""
from datetime import datetime
from lib.macd import MACDStrategy
from lib.rsi import RSIStrategy
from lib.bbands import BBANDSStrategy
from lib.ma import MAStrategy
from lib.kd import KDStrategy


def __init__():
    """初始化交易參數"""
    target_stock = "2498.TW"  # 分析公司代號 e.g., '2330.TW'是台積電
    start_date = datetime(2021, 1, 1)  # 設定資料開始日期
    end_date = datetime(2021, 7, 19)  # 設定資料結束日期
    stop_loss = 0.1  # 停損點，指-10%會強制賣出

    return target_stock, start_date, end_date, stop_loss


def main():
    # 載入交易參數
    target_stock, start_date, end_date, stop_loss = __init__()

    # 建立所有策略實例（將參數傳入父類別）
    strategies = {
        "MACD": MACDStrategy(target_stock, start_date, end_date, stop_loss),
        "RSI": RSIStrategy(target_stock, start_date, end_date, stop_loss),
        "BBANDS": BBANDSStrategy(target_stock, start_date, end_date, stop_loss),
        "MA": MAStrategy(target_stock, start_date, end_date, stop_loss),
        "KD": KDStrategy(target_stock, start_date, end_date, stop_loss),
    }

    # 執行所有策略並收集結果
    results = {}

    print("=" * 80)
    print(f"Stock: {target_stock}")
    print(f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Stop Loss: {stop_loss * 100}%")
    print("=" * 80)

    for strategy_name, strategy in strategies.items():
        print(f"\n{'=' * 80}")
        print(f"Running {strategy_name} Strategy")
        print("=" * 80)

        # 執行策略（參數已在初始化時設定，可以直接呼叫）
        df = strategy.start_strategy()
        results[strategy_name] = {
            "df": df,
            "trades": strategy.trades,
        }

    # 顯示所有策略的比較摘要
    print("\n" + "=" * 80)
    print("STRATEGY COMPARISON SUMMARY")
    print("=" * 80)
    print(
        f"{'Strategy':<15} {'Total Trades':<15} {'Total Profit':<15} {'Avg Profit':<15} {'Win Rate':<15}"
    )
    print("-" * 80)

    for strategy_name, result in results.items():
        trades = result["trades"]
        if trades:
            total_trades = len(trades)
            total_profit = sum(t["Profit"] for t in trades)
            avg_profit = total_profit / total_trades
            win_rate = sum(1 for t in trades if t["Profit"] > 0) / total_trades * 100
        else:
            total_trades = 0
            total_profit = 0
            avg_profit = 0
            win_rate = 0

        print(
            f"{strategy_name:<15} {total_trades:<15} {total_profit:<15.2f} {avg_profit:<15.2f} {win_rate:<15.2f}%"
        )

    print("=" * 80)

    # 詢問是否要繪製指標圖
    print("\nDo you want to draw indicator charts? (y/n)")
    choice = input().strip().lower()

    if choice == "y":
        for strategy_name, strategy in strategies.items():
            print(f"\nDrawing {strategy_name} indicator chart...")
            strategy.draw_indicator()


if __name__ == "__main__":
    main()
