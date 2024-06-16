from flask import Blueprint, request, jsonify
from datetime import datetime
from utils.strategy_loader import load_strategy
from utils.data_loader import load_data
import json
import backtrader as bt

optimize_bp = Blueprint('optimize_bp', __name__)

# Load strategy configuration
with open('config/strategies.json') as f:
    strategy_config = json.load(f)

def run_optimization(strategy_class_path, symbol, start_date, end_date, initial_cash, param_grid):
    strategy_class = load_strategy(strategy_class_path)
    
    # Load data
    data = load_data('yahoo', symbol, start_date, end_date)

    # Create cerebro instance
    cerebro = bt.Cerebro()

    # Add data to cerebro
    cerebro.adddata(data)

    # Add strategy with parameters
    cerebro.optstrategy(strategy_class, **param_grid)

    # Set initial cash
    cerebro.broker.set_cash(initial_cash)

    # Add analyzers
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trade_analyzer")
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")

    # Run backtest
    results = cerebro.run()

    # Collect results
    optimization_results = []
    for result in results:
        for strategy in result:
            optimization_results.append({
                'params': strategy.p._getkwargs(),
                'sharpe_ratio': strategy.analyzers.sharpe.get_analysis()['sharperatio'],
                'final_value': strategy.broker.getvalue()
            })

    return optimization_results

@optimize_bp.route('/optimize', methods=['POST'])
def optimize():
    data = request.json

    strategy_name = data['strategy']
    symbol = data['symbol']
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    initial_cash = data['initial_cash']
    param_grid = data['param_grid']

    strategy_path = strategy_config['entry_strategies'].get(strategy_name)

    if strategy_path is None:
        return jsonify({'error': 'Unknown strategy'}), 400

    optimization_results = run_optimization(strategy_path, symbol, start_date, end_date, initial_cash, param_grid)

    return jsonify(optimization_results)
