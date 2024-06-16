from flask import Flask
from routes.backtest_routes import backtest_bp
from routes.optimization_routes import optimize_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(backtest_bp)
app.register_blueprint(optimize_bp)

if __name__ == '__main__':
    app.run(debug=True)
