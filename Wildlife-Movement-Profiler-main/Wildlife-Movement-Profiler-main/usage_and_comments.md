# Wildlife Movement Profiler — Quick Start Guide

## 1. Try the Dummy Dashboard (No Setup Required)

**Step 1:** Start a local server to serve the dashboard (from anywhere in the project):
```sh
python -m http.server 8050 --directory Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main
```

**Step 2:** Open the dummy dashboard in your browser:
```sh
python -m webbrowser http://localhost:8050/dummy_dashboard.html
```
Or just copy and paste this link into your browser:
- http://localhost:8050/dummy_dashboard.html

**To stop the server:**
- Press `Ctrl+C` in the terminal where you started `http.server`

---

## 2. Run the Full Dashboard Backend (Python Required)

**Step 1:** Install dependencies:
```sh
pip install -r Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/requirements.txt
```

**Step 2:** Start the backend dashboard server:
```sh
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/dashboard/app.py
```

**Step 3:** Open the dashboard in your browser:
- http://localhost:8050/

---

## 3. (Optional) Full Data Pipeline

**Simulate telemetry data:**
```sh
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/simulator/generator.py
```

**Preprocess and extract features:**
```sh
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/processor/preprocessing.py
```

**Classify behaviors:**
```sh
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/classifier/behavior_model.py
```

**Run tests:**
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
git commit -m "Update usage: linear dummy and backend dashboard workflow"
git push
```

---

For more details, see the main README or the code comments in each file. 