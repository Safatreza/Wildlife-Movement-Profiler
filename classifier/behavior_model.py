import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from typing import Optional

class RuleBasedClassifier:
    def __init__(self):
        pass

    def predict(self, df: pd.DataFrame) -> pd.Series:
        # Example rules: adjust as needed
        conditions = [
            (df['speed'] < 0.2) & (df['temperature'] > 0.5),  # normalized temp
            (df['speed'] >= 0.2) & (df['speed'] < 1.0),
            (df['speed'] >= 1.0),
        ]
        choices = ['resting', 'walking', 'running']
        return np.select(conditions, choices, default='unknown')

class MLBehaviorClassifier:
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_path = model_path
        if model_path:
            self.load(model_path)

    def train(self, df: pd.DataFrame, label_col: str = 'behavior', save_path: Optional[str] = None):
        features = self._get_features(df)
        X = df[features]
        y = df[label_col]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        if save_path:
            joblib.dump(self.model, save_path)
            self.model_path = save_path

    def predict(self, df: pd.DataFrame) -> pd.Series:
        if not self.model:
            raise ValueError("Model not loaded or trained.")
        features = self._get_features(df)
        X = df[features]
        return self.model.predict(X)

    def load(self, path: str):
        self.model = joblib.load(path)
        self.model_path = path

    @staticmethod
    def _get_features(df: pd.DataFrame):
        # Use all relevant features for classification
        features = []
        for col in ['speed', 'heading', 'accel_mag', 'temp_trend', 'temperature', 'gyro_x', 'gyro_y', 'gyro_z']:
            if col in df:
                features.append(col)
        return features

def classify_behaviors(df: pd.DataFrame, method: str = 'rule', model_path: Optional[str] = None) -> pd.DataFrame:
    """Classify behaviors and return DataFrame with behavior labels and timestamps."""
    result = df.copy()
    if method == 'rule':
        clf = RuleBasedClassifier()
        result['behavior'] = clf.predict(result)
    elif method == 'ml':
        clf = MLBehaviorClassifier(model_path)
        result['behavior'] = clf.predict(result)
    else:
        raise ValueError("Unknown classification method: choose 'rule' or 'ml'")
    return result[['timestamp', 'behavior']]

# Example usage
if __name__ == "__main__":
    # For rule-based
    df = pd.read_csv('simulated_telemetry.csv')
    from processor.preprocessing import preprocess
    df = preprocess('simulated_telemetry.csv')
    result = classify_behaviors(df, method='rule')
    print(result.head())
    # For ML-based (requires labeled data and a trained model)
    # clf = MLBehaviorClassifier()
    # clf.train(df, label_col='behavior', save_path='rf_model.joblib')
    # result = classify_behaviors(df, method='ml', model_path='rf_model.joblib')
    # print(result.head()) 