# Wildlife Movement Profiler — Usage Guide

## 1. Try the Dummy Dashboard (No Python Backend Required)

**Step 1:** Serve the dummy dashboard from anywhere in the project:
```sh
python -m http.server 8050 --directory Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main
```

**Step 2:** Open the dummy dashboard in your browser:
- http://localhost:8050/dummy_dashboard.html

Or, from the terminal:
```sh
python -m webbrowser http://localhost:8050/dummy_dashboard.html
```

**To stop the server:**
Press `Ctrl+C` in the terminal where you started `http.server`.

---

## 2. Run the Full Interactive Dashboard (Python Backend)

**Step 1:** Install dependencies (from anywhere in the project):
```sh
pip install -r Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/requirements.txt
```

**Step 2:** Start the backend dashboard server (from anywhere in the project):
```sh
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/dashboard/app.py
```

**Step 3:** Open the dashboard in your browser:
- http://localhost:8050/

---

## 3. Full Data Pipeline (Optional)

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

- For the dummy dashboard, always use the `http.server` method above. Do **not** try to run the HTML file as a Python app or open it directly with `file://` in your browser.
- For the backend dashboard, always use the `python .../dashboard/app.py` command. Do **not** try to serve it as a static file.
- All commands work from anywhere in the project—no need to change directories.
- If port 8050 is in use, stop any other process using it or change the port in the command above.

---

## Updating to GitHub

```sh
git add .
git commit -m "Clarify usage: dummy dashboard is static, backend is Python app, all commands work from anywhere"
git push
```

---

For more details, see the main README or the code comments in each file. 