from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

def feature_engineering(data):
    # Debugging: Print DataFrame columns
    # print("Feature engineering input columns:", data.columns)

    # Ensure the expected column names are present
    # expected_columns = ['open', 'high', 'low', 'close', 'volume']
    # for col in expected_columns:
    #     if col not in data.columns:
    #         raise KeyError(f"Expected column '{col}' not found in data")

    data['Return'] = data['Close'].pct_change()
    data['Volatility'] = data['Return'].rolling(window=5).std()
    data['Momentum'] = data['Close'].rolling(window=5).mean()
    data['SMA'] = data['Close'].rolling(window=20).mean()
    data = data.dropna()
    return data

def train_model(data, target):
    X = data.drop(columns=[target])
    y = data[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    
    joblib.dump(model, 'model.pkl')
    
    return mse

def load_model(model_path='model.pkl'):
    return joblib.load(model_path)

def make_predictions(model, data):
    predictions = model.predict(data)
    return predictions
