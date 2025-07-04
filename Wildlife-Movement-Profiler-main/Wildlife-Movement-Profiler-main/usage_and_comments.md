# Wildlife Movement Profiler — Universal Quick Start (No Static Directory Needed)

Get your dashboard running from anywhere in your project—no need to be in a specific folder!

---

## 1. Start Dummy Data and Backend

Open two terminals (from anywhere inside your project folder):

**Terminal 1:** Start the backend dashboard server:
```sh
python Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main/dashboard/app.py
```

**Terminal 2:** Serve the dummy dashboard (for demo/visualization):
```sh
python -m http.server 8050 --directory Wildlife-Movement-Profiler-main/Wildlife-Movement-Profiler-main
```

---

## 2. Open the Dashboard UI

Once the backend or dummy server is running, simply open your browser and go to:
```
http://localhost:8050/
```

Or, to open it automatically from the terminal (Windows):
```sh
start http://localhost:8050/
```

You should see the dashboard UI with interactive charts and analytics. If you are running the dummy server, open:
```
http://localhost:8050/dummy_dashboard.html
```

---

## Troubleshooting
- **404 or Not Found?**
  - Make sure you started the backend server (`python .../dashboard/app.py`) or the dummy server (`python -m http.server ...`).
  - Visit `http://localhost:8050/` (backend) or `http://localhost:8050/dummy_dashboard.html` (dummy) in your browser.
  - Ensure the relevant files exist in the correct directory.
- **No Data?**
  - For backend, ensure all pipeline steps are run and data is available.
  - For dummy, the HTML file is self-contained and should always show sample data.
- **Port in Use?**
  - Stop any other process using port 8050 or change the port in the command above.

---

For more details, see the main README or code comments in each file. 