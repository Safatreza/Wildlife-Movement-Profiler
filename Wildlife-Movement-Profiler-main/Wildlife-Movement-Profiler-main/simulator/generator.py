# Simulator for generating synthetic wildlife telemetry data
import numpy as np
import pandas as pd
import time
import random
from typing import Generator, Optional

class TelemetrySimulator:
    """Simulates telemetry data for a given species and movement mode."""
    def __init__(self, 
                 species: str = 'deer',
                 movement_mode: str = 'walk',
                 sampling_rate: float = 1.0,  # Hz
                 duration: int = 60,  # seconds
                 start_lat: float = 45.0,
                 start_lon: float = -75.0):
        # Initialize simulation parameters
        self.species = species
        self.movement_mode = movement_mode
        self.sampling_rate = sampling_rate
        self.duration = duration
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.reset()

    def reset(self):
        """Reset the simulator to the starting position and time."""
        self.current_lat = self.start_lat
        self.current_lon = self.start_lon
        self.current_time = 0

    def _simulate_gps(self):
        """Simulate GPS movement based on movement mode."""
        # Movement step size (meters) by mode
        step_dict = {'rest': 0.1, 'walk': 1.0, 'run': 5.0, 'fly': 10.0}
        step = step_dict.get(self.movement_mode, 1.0)
        # Random bearing
        bearing = np.deg2rad(random.uniform(0, 360))
        # Approximate conversion: 1 deg lat ~ 111km, 1 deg lon ~ 111km * cos(lat)
        dlat = (step / 111_000) * np.cos(bearing)
        dlon = (step / (111_000 * np.cos(np.deg2rad(self.current_lat)))) * np.sin(bearing)
        self.current_lat += dlat
        self.current_lon += dlon
        return self.current_lat, self.current_lon

    def _simulate_accelerometer(self):
        """Simulate 3-axis acceleration (m/s^2) based on movement mode."""
        base = {'rest': 0.01, 'walk': 0.2, 'run': 1.0, 'fly': 2.0}
        noise = np.random.normal(0, 0.05, 3)
        mag = base.get(self.movement_mode, 0.2)
        return (mag + noise).tolist()

    def _simulate_gyroscope(self):
        """Simulate 3-axis angular velocity (deg/s) based on movement mode."""
        base = {'rest': 0.01, 'walk': 1.0, 'run': 5.0, 'fly': 10.0}
        noise = np.random.normal(0, 0.1, 3)
        mag = base.get(self.movement_mode, 1.0)
        return (mag + noise).tolist()

    def _simulate_compass(self):
        """Simulate compass heading (degrees)."""
        return random.uniform(0, 360)

    def _simulate_temperature(self):
        """Simulate body temperature (Celsius) based on species."""
        base_temp = {'deer': 38.5, 'wolf': 39.0, 'eagle': 41.0}
        temp = base_temp.get(self.species, 38.5) + np.random.normal(0, 0.5)
        return temp

    def generate(self) -> Generator[dict, None, None]:
        """Yield simulated telemetry data as a stream of dictionaries."""
        self.reset()
        n_samples = int(self.duration * self.sampling_rate)
        interval = 1.0 / self.sampling_rate
        for i in range(n_samples):
            lat, lon = self._simulate_gps()
            accel = self._simulate_accelerometer()
            gyro = self._simulate_gyroscope()
            compass = self._simulate_compass()
            temp = self._simulate_temperature()
            data = {
                'timestamp': time.time(),
                'species': self.species,
                'movement_mode': self.movement_mode,
                'latitude': lat,
                'longitude': lon,
                'accel_x': accel[0],
                'accel_y': accel[1],
                'accel_z': accel[2],
                'gyro_x': gyro[0],
                'gyro_y': gyro[1],
                'gyro_z': gyro[2],
                'compass': compass,
                'temperature': temp
            }
            yield data
            time.sleep(interval)

    def save_to_csv(self, filename: str):
        """Save generated telemetry data to a CSV file."""
        records = list(self.generate())
        df = pd.DataFrame(records)
        df.to_csv(filename, index=False)

    def stream(self, method: str = 'mqtt', topic: str = 'wildlife/telemetry', host: str = 'localhost', port: int = 1883):
        """Stream generated data via MQTT or WebSocket (placeholder)."""
        # Placeholder for streaming via MQTT or WebSocket
        # In production, use paho-mqtt or websockets libraries
        print(f"[STREAM] Simulating {method.upper()} stream to {host}:{port} on topic '{topic}'...")
        for data in self.generate():
            print(f"[STREAM] {data}")
            # Here, you would publish to MQTT/WebSocket
            # e.g., mqtt_client.publish(topic, json.dumps(data))
            # or websocket.send(json.dumps(data))

# Example usage
if __name__ == "__main__":
    # Create a simulator instance for a deer walking at 2 Hz for 5 seconds
    sim = TelemetrySimulator(species='deer', movement_mode='walk', sampling_rate=2, duration=5)
    # Save simulated data to CSV
    sim.save_to_csv('simulated_telemetry.csv')
    # Uncomment to stream data (requires MQTT/WebSocket setup)
    # sim.stream(method='mqtt') 