# Preprocessing pipeline for wildlife telemetry data
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

def ingest_data(filepath: str) -> pd.DataFrame:
    """Read telemetry data from CSV."""
    df = pd.read_csv(filepath)
    return df

def clean_and_normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Clean missing values and normalize sensor columns."""
    df = df.copy()
    # Fill missing values with interpolation or mean
    df.interpolate(method='linear', inplace=True)
    df.fillna(df.mean(numeric_only=True), inplace=True)
    # Normalize sensor columns
    sensor_cols = ['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'temperature']
    for col in sensor_cols:
        if col in df:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                df[col] = (df[col] - mean) / std
    return df

def moving_average_filter(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """Apply moving average filter to sensor columns."""
    df = df.copy()
    sensor_cols = ['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'temperature']
    for col in sensor_cols:
        if col in df:
            df[col] = df[col].rolling(window, min_periods=1, center=True).mean()
    return df

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract features: speed, heading, acceleration magnitude, temperature trend."""
    df = df.copy()
    # Speed (meters/second) from GPS
    if 'latitude' in df and 'longitude' in df and 'timestamp' in df:
        lat = np.deg2rad(df['latitude'].values)
        lon = np.deg2rad(df['longitude'].values)
        dlat = np.diff(lat, prepend=lat[0])
        dlon = np.diff(lon, prepend=lon[0])
        # Haversine formula for distance
        a = np.sin(dlat/2)**2 + np.cos(lat) * np.cos(np.roll(lat, 1)) * np.sin(dlon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        R = 6371000  # Earth radius in meters
        dist = R * c
        dt = np.diff(df['timestamp'], prepend=df['timestamp'][0])
        dt[dt == 0] = 1e-6  # avoid division by zero
        speed = dist / dt
        df['speed'] = speed
    # Heading (degrees)
    if 'compass' in df:
        df['heading'] = df['compass']
    # Acceleration magnitude
    if all(col in df for col in ['accel_x', 'accel_y', 'accel_z']):
        df['accel_mag'] = np.sqrt(df['accel_x']**2 + df['accel_y']**2 + df['accel_z']**2)
    # Temperature trend (smoothed)
    if 'temperature' in df:
        # Use Savitzky-Golay filter for smoothing
        df['temp_trend'] = savgol_filter(df['temperature'], window_length=5 if len(df) >= 5 else len(df)//2*2+1, polyorder=2)
    return df

def preprocess(filepath: str) -> pd.DataFrame:
    """Full preprocessing pipeline: ingest, clean, filter, feature extraction."""
    df = ingest_data(filepath)
    df = clean_and_normalize(df)
    df = moving_average_filter(df)
    df = extract_features(df)
    return df

# Example usage
if __name__ == "__main__":
    # Run the full preprocessing pipeline on a sample file
    df = preprocess('simulated_telemetry.csv')
    print(df.head()) 