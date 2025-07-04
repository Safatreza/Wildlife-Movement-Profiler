# Wildlife Movement Profiler — Quick Start: Dummy Dashboard

The fastest way to try out the dashboard and visualizations is **Dummy Mode**. You don't need to install any dependencies or run any backend server—just use Python's built-in tools to serve and view the dashboard in your browser.

---

## 🚀 Easiest Demo: Dummy Dashboard in Your Browser

**1. Start a local server to serve the dashboard (from anywhere in the project):**

```sh
python -m http.server 8050 --directory Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main
```

**2. Open the dashboard in your browser:**

```sh
python -m webbrowser http://localhost:8050/dummy_dashboard.html
```

Or just copy and paste this link into your browser:
- [http://localhost:8050/dummy_dashboard.html](http://localhost:8050/dummy_dashboard.html)

**What you get:**
- Interactive map, charts, and analytics using pre-generated sample data
- No Python dependencies or backend required—just your browser and Python (any version)

**To stop the server:**
- Press `Ctrl+C` in the terminal where you started `http.server`

---

## Full Project Usage (Simulation, Preprocessing, ML, API, etc.)

If you want to run the full Python pipeline, see the steps below. All commands use explicit relative paths and can be run from anywhere in the project.

### 1. Setup & Installation

```sh
pip install -r Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/requirements.txt
```

### 2. Run the Dashboard Backend

```sh
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/dashboard/app.py
```
- Then open [http://localhost:8050/](http://localhost:8050/) in your browser.

### 3. Simulate Telemetry Data

```sh
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/simulator/generator.py
```

### 4. Preprocess and Extract Features

```sh
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/processor/preprocessing.py
```

### 5. Classify Behaviors (Rule-based or ML)

```sh
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/classifier/behavior_model.py
```

### 6. Run Tests

```sh
pytest Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/tests/test_pipeline.py
```

---

## Troubleshooting
- If you don't see the dashboard, make sure the server is running and you're visiting the correct URL.
- For dummy mode, ensure you're using the `http://localhost:8050/dummy_dashboard.html` link (not opening the file directly).
- If port 8050 is in use, stop any other process using it or change the port in the command above.

---

## Updating to GitHub

```sh
git add .
git commit -m "Update usage: make dummy dashboard mode easiest entry point"
git push
```

---

For more details, see the main README or the code comments in each file. 