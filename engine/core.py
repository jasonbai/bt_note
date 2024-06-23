import bt
import pandas as pd

class BacktestAnalyzer:
    def __init__(self, result):
        self.result = result

    def plot_weights(self):
        """绘制资产权重变化图"""
        self.result.plot_security_weights()

    def print_latest_holdings_and_signals(self):
        """输出最新的持仓和买卖建议"""
        latest_weights = self.result.get_security_weights().iloc[-1]
        print("最新持仓:")
        print(latest_weights)

        buy_signals = latest_weights[latest_weights > 0].index.tolist()
        sell_signals = latest_weights[latest_weights == 0].index.tolist()

        print("\n买入建议:")
        print(buy_signals)

        print("\n卖出建议:")
        print(sell_signals)

    def get_transactions(self, save_to_csv=False):
        """获取交易明细"""
        transactions = self.result.get_transactions()
        print("\n交易明细:")
        print(transactions)
        
        if save_to_csv:
            transactions.to_csv("交易明细.csv")
        
        return transactions

# 示例用法
# analyzer = BacktestAnalyzer(result)
# analyzer.plot_weights()
# analyzer.print_latest_holdings_and_signals()
# analyzer.get_transactions(save_to_csv=True)

## --- 策略区 --- ##
# 1. 均线策略
## note： 含取数，后续拆出
def above_sma(tickers, sma_per=50, start='2019-01-01', name='above_sma'):
    """
    Long securities that are above their n period
    Simple Moving Averages with equal weights.

    exmaple:
    # create the backtests
        tickers = 'rsp,iwy,moat,pff,vnq'
        sma10 = above_sma(tickers, sma_per=10, name='sma10')
        sma100 = above_sma(tickers, sma_per=100, name='sma100')
        sma200 = above_sma(tickers, sma_per=200, name='sma200')
    """
    # download data
    data = bt.get(tickers, start=start)
    # calc sma
    sma = data.rolling(sma_per).mean()
    # 选择价格在其移动平均线和120%移动平均线之间的证券
    between_sma_and_120_sma = (data > sma) & (data < 1.2 * sma)

    # create strategy
    s = bt.Strategy(name, [SelectWhere(between_sma_and_120_sma),
                           bt.algos.WeighEqually(),
                           bt.algos.Rebalance()])

    # now we create the backtest
    return bt.Backtest(s, data)

# 2. 基准策略
## note： 含取数逻辑，后续拆出
def long_only_ew(tickers, start='2019-01-01', name='long_only_ew'):
    """
    exmaple:
    benchmark = long_only_ew('iwy', name='iwy')

    """
    s = bt.Strategy(name, [bt.algos.RunOnce(),
                           bt.algos.SelectAll(),
                           bt.algos.WeighEqually(),
                           bt.algos.Rebalance()])
    data = bt.get(tickers, start=start)
    return bt.Backtest(s, data)