from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
import pandas as pd
import os
from simulator.generator import TelemetrySimulator
from classifier.behavior_model import classify_behaviors, MLBehaviorClassifier
from processor.preprocessing import preprocess

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")
router = APIRouter()

# Dummy user for demo
demo_user = {"username": "admin", "password": "password"}

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username != demo_user["username"]:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == demo_user["username"] and form_data.password == demo_user["password"]:
        access_token = create_access_token(data={"sub": demo_user["username"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect username or password")

@router.get("/telemetry/live")
async def get_live_telemetry(token: str = Depends(verify_token)):
    if os.path.exists("simulated_telemetry.csv"):
        df = pd.read_csv("simulated_telemetry.csv")
        return df.tail(10).to_dict(orient="records")
    return []

@router.get("/telemetry/history")
async def get_historical_telemetry(start: float = None, end: float = None, token: str = Depends(verify_token)):
    if os.path.exists("simulated_telemetry.csv"):
        df = pd.read_csv("simulated_telemetry.csv")
        if start:
            df = df[df["timestamp"] >= start]
        if end:
            df = df[df["timestamp"] <= end]
        return df.to_dict(orient="records")
    return []

@router.get("/behavior/results")
async def get_behavior_results(token: str = Depends(verify_token)):
    if os.path.exists("simulated_telemetry.csv"):
        df = preprocess("simulated_telemetry.csv")
        result = classify_behaviors(df, method='rule')
        return result.to_dict(orient="records")
    return []

@router.post("/simulate/run")
async def run_simulation(species: str = 'deer', movement_mode: str = 'walk', sampling_rate: float = 1.0, duration: int = 60, token: str = Depends(verify_token)):
    sim = TelemetrySimulator(species=species, movement_mode=movement_mode, sampling_rate=sampling_rate, duration=duration)
    sim.save_to_csv('simulated_telemetry.csv')
    return {"status": "Simulation complete"}

@router.post("/model/train")
async def train_model(label_col: str = 'behavior', token: str = Depends(verify_token)):
    if os.path.exists("simulated_telemetry.csv"):
        df = preprocess("simulated_telemetry.csv")
        # For demo, assume 'behavior' column exists
        clf = MLBehaviorClassifier()
        clf.train(df, label_col=label_col, save_path='rf_model.joblib')
        return {"status": "Model trained and saved as rf_model.joblib"}
    return {"status": "No data to train on"} 