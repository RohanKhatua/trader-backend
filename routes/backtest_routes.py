from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.strategy_loader import load_strategy
from utils.data_loader import load_data
import json
import backtrader as bt

backtest_bp = Blueprint('backtest_bp', __name__)

# Load strategy configuration
with open('config/strategies.json') as f:
    strategy_config = json.load(f)

def run_backtest(entry_strategy_path, entry_params, exit_strategy_path, exit_params, symbol, data_source, start_date, end_date, initial_cash):
    entry_strategy_class = load_strategy(entry_strategy_path)
    exit_strategy_class = load_strategy(exit_strategy_path)

    # Load data
    data = load_data(data_source, symbol, start_date, end_date)

    # Create cerebro instance
    cerebro = bt.Cerebro()

    # Add data to cerebro
    cerebro.adddata(data)

    # Add entry and exit strategies to cerebro
    cerebro.addstrategy(entry_strategy_class, **entry_params)
    cerebro.addstrategy(exit_strategy_class, **exit_params)

    # Set initial cash
    cerebro.broker.set_cash(initial_cash)

    # Add analyzers
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trade_analyzer")
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")

    # Run backtest
    results = cerebro.run()

    # Get final portfolio value and performance metrics
    final_value = cerebro.broker.getvalue()
    performance = results[0].analyzers.sharpe.get_analysis()
    drawdown = results[0].analyzers.drawdown.get_analysis()
    trades = results[0].analyzers.trade_analyzer.get_analysis()

    return final_value, performance, drawdown, trades

@backtest_bp.route('/backtest', methods=['POST'])
def backtest():
    data = request.json
    
    entry_strategy_name = data['entry_strategy']
    entry_params = data['entry_params']
    exit_strategy_name = data['exit_strategy']
    exit_params = data['exit_params']
    symbol = data['symbol']
    data_source = data['data_source']
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    initial_cash = data['initial_cash']
    
    entry_strategy_path = strategy_config['entry_strategies'].get(entry_strategy_name)
    exit_strategy_path = strategy_config['exit_strategies'].get(exit_strategy_name)
    
    if entry_strategy_path is None or exit_strategy_path is None:
        return jsonify({'error': 'Invalid strategy name'}), 400
    
    final_value, performance, drawdown, trades = run_backtest(entry_strategy_path, entry_params, exit_strategy_path, exit_params, symbol, data_source, start_date, end_date, initial_cash)
    
    return jsonify({
        'initial_cash': initial_cash,
        'final_value': final_value,
        'performance': performance,
        'drawdown': drawdown,
        'trades': trades
    })
