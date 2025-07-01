# Wildlife Movement Profiler

## Project Overview
Wildlife Movement Profiler is a modular, end-to-end platform for simulating, processing, classifying, and visualizing wildlife telemetry data. It is designed for researchers, conservationists, and data scientists to:
- Generate realistic synthetic telemetry data (GPS, accelerometer, gyroscope, compass, temperature)
- Ingest, clean, and preprocess telemetry data
- Extract features and classify animal behaviors (rule-based and ML-based)
- Visualize real-time and historical data on interactive dashboards and maps
- Provide secure RESTful APIs for integration and automation

The platform is suitable for rapid prototyping, algorithm development, and educational purposes in wildlife analytics.

---

## How to Run the Actual Project

### Prerequisites
- Python 3.10+ (for local development)
- Docker & Docker Compose (for containerized deployment)

### 1. Local Development
1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Generate synthetic telemetry data:**
   ```sh
   python simulator/generator.py
   ```
   This creates `simulated_telemetry.csv` with synthetic animal movement and sensor data.
3. **Preprocess and extract features:**
   ```sh
   python -c "from processor.preprocessing import preprocess; preprocess('simulated_telemetry.csv')"
   ```
4. **Run the API service:**
   ```sh
   uvicorn api.main:app --reload
   ```
   The API will be available at [http://localhost:8000/docs](http://localhost:8000/docs)
5. **Run the dashboard:**
   ```sh
   uvicorn dashboard.app:app --reload --port 8050
   ```
   The dashboard will be available at [http://localhost:8050](http://localhost:8050)

### 2. Docker Compose (Recommended)
1. **Build and start all services:**
   ```sh
   docker-compose up --build
   ```
   This launches the simulator, processor, API, and dashboard as separate services.
2. **Access the dashboard:** [http://localhost:8050](http://localhost:8050)
3. **Access the API docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Expected Output
- **simulated_telemetry.csv**: Synthetic telemetry data with GPS, sensor, and timestamped records
- **Dashboard**: Interactive charts and maps showing animal tracks, sensor data, and behavior classification over time
- **API**: Secure endpoints for fetching telemetry, behavior results, and triggering simulations/model training
- **Logs**: Console output for simulation, processing, and API requests

---

## Dummy Project: Standalone Visualization

### What is the Dummy Project?
The dummy project is a single HTML file (`dummy_dashboard.html`) that demonstrates the core visualization features of the platform using pre-generated sample data. It requires **no software installation**—just open in any modern web browser.

### Why a Dummy Project?
- **Accessibility**: Allows users to explore the platform's visualization and analytics capabilities without installing Python, Docker, or dependencies.
- **Demonstration**: Useful for presentations, quick demos, and sharing with non-technical stakeholders.
- **Education**: Helps users understand the data and visual outputs before running the full system.

### How to Use the Dummy Project
1. Open `dummy_dashboard.html` in your browser.
2. Explore:
   - Animal movement on an interactive map (Leaflet.js or Plotly)
   - Sensor and behavior time series (Plotly charts)
   - Playback and filtering controls (if included)

### Expected Output
- **Interactive map**: Shows a sample animal track
- **Charts**: Display simulated sensor and behavior data over time
- **No backend required**: All data and logic are embedded in the HTML file

---

## Full Documentation
See [docs/README.md](docs/README.md) for detailed architecture, contribution guidelines, and citation info.

## Features
- Synthetic telemetry data generation (GPS, accelerometer, etc.)
- Data ingestion, preprocessing, and feature extraction
- Rule-based and ML-based behavior classification
- Interactive web dashboard with Plotly and map visualizations
- RESTful API for external access
- CLI tools for data generation, training, and deployment

## Project Structure
See `project_structure.md` for a detailed folder breakdown.

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the entry point: `python main.py`

## License
MIT 