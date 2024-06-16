import importlib

def load_strategy(strategy_path):
    module_name, class_name = strategy_path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    strategy_class = getattr(module, class_name)
    return strategy_class
