# Wildlife Movement Profiler — Usage & Comments

## Quick Launch: Dummy Dashboard on Localhost

To serve and view the dummy dashboard at a localhost URL (recommended for best browser compatibility):

```sh
# 1. Start a simple HTTP server (from anywhere in the project):
python -m http.server 8050 --directory Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main

# 2. In a new terminal, open the dashboard in your browser:
python -m webbrowser http://localhost:8050/dummy_dashboard.html
# Or manually visit: http://localhost:8050/dummy_dashboard.html
```

This approach works on all platforms and ensures the dashboard is served over HTTP, not file://, which is required for some browser features.

---

**Note:** All commands below use explicit relative paths, so you can run them from anywhere inside the project directory. The dashboard now runs on port 8050 by default.

---

## 1. Setup & Installation

```sh
# Install Python dependencies (from project root or any subdirectory)
pip install -r Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/requirements.txt
```

---

## 2. Running the Dashboard (Backend Server)

```sh
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/dashboard/app.py
```
- After running the above command, **open [http://localhost:8050/](http://localhost:8050/) in your web browser** to access the dashboard.

---

## 3. Running in Dummy Mode (No Python Required)

**Dummy mode** allows you to demo and visualize the dashboard and analytics features without running any backend or installing Python. This is ideal for quick demos, development, or sharing the project with others.

**Steps:**
1. Use the quick launch commands above, or
2. Locate the file:
   - `Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/dummy_dashboard.html`
   and open it in any modern web browser.
3. Explore the interactive map, charts, and controls. All data and logic are embedded in the HTML file—no backend or server is needed.

**What to expect:**
- The dashboard will show sample animal tracks, sensor data, and behavior analytics.
- You do not need any external hardware, Python, or server for this mode.

**Troubleshooting:**
- If you do not see data, ensure you are opening the correct HTML file and using a modern browser.
- Refresh the page if needed.

---

## 4. Simulating Telemetry Data (Full Python Pipeline)

1. **Generate synthetic telemetry data:**
   ```sh
   python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/simulator/generator.py
   ```
2. **Preprocess and extract features:**
   ```sh
   python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/processor/preprocessing.py
   ```
3. **Classify behaviors (rule-based or ML):**
   ```sh
   python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/classifier/behavior_model.py
   ```

---

## 5. Running the API (Optional, for Programmatic Access)

If you have an API app (e.g., `api/routes.py`), mount it in a FastAPI app and run with uvicorn:
```sh
# Example (if you create an app in api/main.py):
# uvicorn Wildlife-Movement-Profiler-main.Wildlife-Movement-Profiler-main.api.main:app --reload
```

---

## 6. Running Tests

```sh
pytest Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/tests/test_pipeline.py
```

---

## 7. Module Purposes & Key Comments

### `dashboard/app.py`
- **Purpose:** Main backend server. Hosts the dashboard, serves telemetry and analytics endpoints. User must open the dashboard URL manually.
- **Key Comments:**
  - "FastAPI dashboard app for visualizing wildlife telemetry and behavior data"
  - "Runs on port 8050; open http://localhost:8050/ manually"

### `simulator/generator.py`
- **Purpose:** Generates synthetic wildlife telemetry data (GPS, accelerometer, etc.) and saves to CSV.
- **Key Comments:**
  - "Simulates telemetry data for a given species and movement mode"
  - "Save generated telemetry data to a CSV file"

### `processor/preprocessing.py`
- **Purpose:** Cleans, normalizes, and extracts features from telemetry data.
- **Key Comments:**
  - "Preprocessing pipeline for wildlife telemetry data"
  - "Extract features: speed, heading, acceleration magnitude, temperature trend"

### `classifier/behavior_model.py`
- **Purpose:** Classifies animal behavior using rule-based or ML models.
- **Key Comments:**
  - "Classifies behavior using simple rule-based logic or Random Forest ML"
  - "Train the ML model and optionally save it to disk"

### `dummy_dashboard.html`
- **Purpose:** Standalone HTML demo of the dashboard (no Python required).

---

## 8. Troubleshooting
- **No data on dashboard?**
  - Ensure `python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/dashboard/app.py` is running and the dashboard is open in your browser at [http://localhost:8050/](http://localhost:8050/).
  - For dummy mode, ensure you are opening the correct HTML file or using the localhost quick launch method above.
  - Refresh the dashboard page if needed.
  - Check your terminal for errors or warnings.
  - If port 8050 is in use, stop any other process using it or change the port in `dashboard/app.py`.

---

## 9. Updating to GitHub

```sh
git add .
git commit -m "Update project and usage docs for explicit path commands and dummy mode"
git push
```

---

For more details, see the main README or the code comments in each file. 