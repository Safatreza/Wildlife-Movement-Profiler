# FastAPI API routes for telemetry, simulation, and behavior classification
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
import pandas as pd
import os
from simulator.generator import TelemetrySimulator
from classifier.behavior_model import classify_behaviors, MLBehaviorClassifier
from processor.preprocessing import preprocess

router = APIRouter()

# JWT authentication setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
SECRET_KEY = "secret"
ALGORITHM = "HS256"

# Helper to create JWT access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to verify JWT token
def verify_token(token: str = Depends(oauth2_scheme)):
    """Verify JWT token and return user info."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Login endpoint
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token."""
    # Dummy authentication for demo
    if form_data.username == "admin" and form_data.password == "password":
        access_token = create_access_token({"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect username or password")

# Live telemetry endpoint
@router.get("/telemetry/live")
async def get_live_telemetry(token: str = Depends(verify_token)):
    """Return live telemetry data (simulated)."""
    sim = TelemetrySimulator(duration=2)
    data = list(sim.generate())
    return data

# Historical telemetry endpoint
@router.get("/telemetry/historical")
async def get_historical_telemetry(start: float = None, end: float = None, token: str = Depends(verify_token)):
    """Return historical telemetry data from CSV, filtered by time."""
    if not os.path.exists("simulated_telemetry.csv"):
        return []
    df = pd.read_csv("simulated_telemetry.csv")
    if start is not None:
        df = df[df["timestamp"] >= start]
    if end is not None:
        df = df[df["timestamp"] <= end]
    return df.to_dict(orient="records")

# Behavior classification endpoint
@router.get("/behavior/results")
async def get_behavior_results(token: str = Depends(verify_token)):
    """Return behavior classification results for telemetry data."""
    if not os.path.exists("simulated_telemetry.csv"):
        return []
    df = pd.read_csv("simulated_telemetry.csv")
    df = preprocess("simulated_telemetry.csv")
    result = classify_behaviors(df, method="rule")
    return result.to_dict(orient="records")

# Run simulation endpoint
@router.post("/simulate")
async def run_simulation(species: str = 'deer', movement_mode: str = 'walk', sampling_rate: float = 1.0, duration: int = 60, token: str = Depends(verify_token)):
    """Run a new telemetry simulation and save to CSV."""
    sim = TelemetrySimulator(species=species, movement_mode=movement_mode, sampling_rate=sampling_rate, duration=duration)
    sim.save_to_csv("simulated_telemetry.csv")
    return {"status": "ok"}

# Train ML model endpoint
@router.post("/train")
async def train_model(label_col: str = 'behavior', token: str = Depends(verify_token)):
    """Train a machine learning model for behavior classification."""
    if not os.path.exists("simulated_telemetry.csv"):
        raise HTTPException(status_code=400, detail="No data to train on.")
    df = pd.read_csv("simulated_telemetry.csv")
    df = preprocess("simulated_telemetry.csv")
    clf = MLBehaviorClassifier()
    clf.train(df, label_col=label_col, save_path="rf_model.joblib")
    return {"status": "trained"} 