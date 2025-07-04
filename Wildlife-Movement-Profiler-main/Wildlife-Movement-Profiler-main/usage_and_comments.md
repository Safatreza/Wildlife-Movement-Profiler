# Wildlife Movement Profiler - Usage & Comments

## Using the Dummy Version (No Installation Required)

The dummy version is a standalone HTML file that demonstrates the core visualization features of the platform using pre-generated sample data. No Python or dependencies are required.

**To use the dummy dashboard:**

1. Locate the file: `Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/dummy_dashboard.html`
2. Double-click or right-click and open it in any modern web browser (Chrome, Firefox, Edge, etc.).
3. Explore the interactive map, charts, and controls. All data and logic are embedded in the HTML file—no backend or server is needed.

**When to use:**
- For quick demos, presentations, or sharing with non-technical users.
- To preview the dashboard's capabilities before running the full Python project.

---

## Using the Full Python Project

This file provides all the commands you need to install dependencies, run simulations, preprocess data, classify behaviors, and launch the dashboard/API. All commands are copy-paste ready and can be run from anywhere in the project directory tree.

---

## 1. Install Python Dependencies

```sh
# Install all required Python packages (recommended: use a virtual environment)
pip install -r Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/requirements.txt
```

---

## 2. Generate Simulated Telemetry Data

```sh
# Run the simulator to generate synthetic telemetry data and save to CSV
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/simulator/generator.py
```

---

## 3. Preprocess Telemetry Data

```sh
# Run the preprocessing pipeline on the simulated data
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/processor/preprocessing.py
```

---

## 4. Classify Behaviors (Rule-based or ML)

```sh
# Run rule-based behavior classification on the preprocessed data
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/classifier/behavior_model.py

# (Optional) Train and use ML-based classifier (requires labeled data)
# Uncomment the relevant lines in behavior_model.py for ML training and prediction
```

---

## 5. Run the FastAPI Dashboard (Visualization)

```sh
# Start the FastAPI dashboard using uvicorn
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/dashboard/app.py

# The dashboard will automatically open in your default web browser at http://127.0.0.1:8050/
```

---

## 6. Run the FastAPI API (Programmatic Access)

```sh
# (If you have an API app, e.g., api/routes.py, mount it in a FastAPI app and run with uvicorn)
# Example (if you create an app in api/main.py):
# uvicorn Wildlife-Movement-Profiler-main.Wildlife-Movement-Profiler-main.api.main:app --reload
```

---

## 7. Run Tests

```sh
# Run all tests to verify the pipeline
pytest Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/tests/test_pipeline.py
```

---

## 8. Project Structure Overview

- `simulator/generator.py`: Generates synthetic telemetry data.
- `processor/preprocessing.py`: Cleans and extracts features from telemetry data.
- `classifier/behavior_model.py`: Classifies animal behavior (rule-based or ML).
- `dashboard/app.py`: FastAPI dashboard for visualization.
- `api/`: FastAPI API endpoints for programmatic access (requires integration).
- `tests/`: Test suite for the pipeline.
- `dummy_dashboard.html`: Standalone HTML demo of the dashboard (no Python required).

---

## 9. Notes

- The dashboard requires `dashboard/templates/index.html` and `dashboard/static/` for HTML and static assets. Create these if you want to customize the UI.
- Default authentication for API is username: `admin`, password: `password` (for demo only).
- All commands assume you have Python and pip installed and available in your PATH.
- When running the dashboard, your browser will open automatically to http://127.0.0.1:8050/. 