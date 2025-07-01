from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import os

app = FastAPI()
templates = Jinja2Templates(directory="dashboard/templates")
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

# Load or simulate data for demo
DATA_PATH = "simulated_telemetry.csv"
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Show main dashboard page
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/data")
async def get_data():
    # Return latest telemetry data (for AJAX/JS polling)
    if not df.empty:
        return df.tail(100).to_dict(orient="records")
    return []

@app.get("/api/plot/gps")
async def plot_gps():
    # Plot GPS tracks on a map
    if df.empty:
        return {"html": "<p>No data</p>"}
    fig = go.Figure(go.Scattermapbox(
        lat=df["latitude"],
        lon=df["longitude"],
        mode="lines+markers",
        marker=dict(size=6, color="blue"),
        line=dict(width=2, color="blue"),
        text=df["timestamp"].astype(str)
    ))
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=10,
        mapbox_center={"lat": df["latitude"].mean(), "lon": df["longitude"].mean()},
        margin={"l":0,"r":0,"t":0,"b":0}
    )
    html = pio.to_html(fig, full_html=False)
    return {"html": html}

@app.get("/api/plot/behavior")
async def plot_behavior():
    # Plot behavior classification over time
    if df.empty or "behavior" not in df:
        return {"html": "<p>No behavior data</p>"}
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["behavior"],
        mode="lines+markers",
        marker=dict(size=6, color="orange"),
        line=dict(width=2, color="orange"),
        name="Behavior"
    ))
    fig.update_layout(title="Behavior Over Time", xaxis_title="Time", yaxis_title="Behavior")
    html = pio.to_html(fig, full_html=False)
    return {"html": html}

@app.get("/api/plot/sensors")
async def plot_sensors():
    # Plot sensor data (e.g., speed, accel_mag, temp)
    if df.empty:
        return {"html": "<p>No data</p>"}
    fig = go.Figure()
    for col in ["speed", "accel_mag", "temperature"]:
        if col in df:
            fig.add_trace(go.Scatter(x=df["timestamp"], y=df[col], mode="lines", name=col))
    fig.update_layout(title="Sensor Data Over Time", xaxis_title="Time")
    html = pio.to_html(fig, full_html=False)
    return {"html": html}

@app.websocket("/ws/data")
async def websocket_data(websocket: WebSocket):
    await websocket.accept()
    # For demo: send last 10 rows every second
    import asyncio
    while True:
        if not df.empty:
            await websocket.send_json(df.tail(10).to_dict(orient="records"))
        await asyncio.sleep(1)

# Historical playback and filtering endpoint
@app.get("/api/data/filter")
async def filter_data(start: float = None, end: float = None, behavior: str = None):
    filtered = df.copy()
    if start is not None:
        filtered = filtered[filtered["timestamp"] >= start]
    if end is not None:
        filtered = filtered[filtered["timestamp"] <= end]
    if behavior and "behavior" in filtered:
        filtered = filtered[filtered["behavior"] == behavior]
    return filtered.to_dict(orient="records")

# --- TEMPLATES & STATIC FILES ---
# You will need to create:
# - dashboard/templates/index.html (main dashboard page)
# - dashboard/static/ (for JS, CSS, etc.) 