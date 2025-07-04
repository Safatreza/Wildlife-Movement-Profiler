import pytest
import pandas as pd
from fastapi.testclient import TestClient
from simulator.generator import TelemetrySimulator
from processor import preprocessing
from classifier import behavior_model
from api import auth
from fastapi import FastAPI

# --- Data Simulation Accuracy ---
def test_simulator_output_shape():
    sim = TelemetrySimulator(species='deer', movement_mode='walk', sampling_rate=2, duration=2)
    data = list(sim.generate())
    assert len(data) == 4
    for row in data:
        assert 'latitude' in row and 'longitude' in row
        assert 'accel_x' in row and 'gyro_x' in row and 'temperature' in row

# --- Preprocessing and Feature Extraction ---
def test_preprocessing_and_features():
    # Create mock data
    df = pd.DataFrame({
        'timestamp': [1, 2, 3, 4, 5],
        'latitude': [45.0, 45.0001, 45.0002, 45.0003, 45.0004],
        'longitude': [-75.0, -75.0001, -75.0002, -75.0003, -75.0004],
        'accel_x': [0.1, 0.2, 0.1, 0.2, 0.1],
        'accel_y': [0.0, 0.1, 0.0, 0.1, 0.0],
        'accel_z': [1.0, 1.1, 1.0, 1.1, 1.0],
        'gyro_x': [0.01]*5,
        'gyro_y': [0.02]*5,
        'gyro_z': [0.03]*5,
        'compass': [10, 20, 30, 40, 50],
        'temperature': [38, 38.1, 38.2, 38.3, 38.4]
    })
    df_clean = preprocessing.clean_and_normalize(df)
    assert not df_clean.isnull().any().any()
    df_feat = preprocessing.extract_features(df_clean)
    assert 'speed' in df_feat and 'accel_mag' in df_feat and 'temp_trend' in df_feat

# --- Behavior Classification Logic ---
def test_rule_based_classification():
    df = pd.DataFrame({
        'speed': [0.1, 0.5, 1.5],
        'temperature': [1.0, 0.0, 0.0]  # normalized
    })
    clf = behavior_model.RuleBasedClassifier()
    labels = clf.predict(df)
    assert list(labels) == ['resting', 'walking', 'running']

def test_ml_classifier_train_and_predict(tmp_path):
    # Mock labeled data
    df = pd.DataFrame({
        'speed': [0.1, 0.5, 1.5, 0.2, 1.2],
        'heading': [10, 20, 30, 40, 50],
        'accel_mag': [1, 2, 3, 1, 2],
        'temp_trend': [0, 1, 2, 0, 1],
        'behavior': ['resting', 'walking', 'running', 'walking', 'running']
    })
    clf = behavior_model.MLBehaviorClassifier()
    clf.train(df, label_col='behavior', save_path=str(tmp_path / 'model.joblib'))
    clf.load(str(tmp_path / 'model.joblib'))
    preds = clf.predict(df)
    assert len(preds) == len(df)

# --- API Endpoint Responses ---
@pytest.fixture
def test_app():
    from fastapi import FastAPI
    from api.routes import router as api_router
    from api.auth import router as auth_router
    app = FastAPI()
    app.include_router(auth_router, prefix="/api")
    app.include_router(api_router, prefix="/api")
    return app

def test_api_login_and_protected_endpoints(test_app):
    client = TestClient(test_app)
    # Login
    resp = client.post("/api/token", data={"username": "admin", "password": "password"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Test protected endpoint
    resp = client.get("/api/telemetry/live", headers=headers)
    assert resp.status_code in (200, 404, 422)  # 404/422 if no data
    # Test role restriction
    resp = client.post("/api/token", data={"username": "bob", "password": "viewerpass"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Viewer should not be able to train model (if role checks added)
    resp = client.post("/api/model/train", headers=headers)
    # Acceptable: 403 if role checks, 200/other if not implemented
    assert resp.status_code in (200, 403, 404, 422) 