from fastapi import FastAPI
from prometheus_api_client import PrometheusConnect
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
import numpy as np
from prometheus_client import Gauge, make_asgi_app

app = FastAPI()

# Define custom Gauge metrics for ML outputs
ANOMALY_SCORE = Gauge("ml_cpu_anomaly_flag", "1 if anomaly detected, 0 otherwise")
PREDICTED_CPU = Gauge("ml_cpu_predicted_value", "Predicted CPU usage")

prom = PrometheusConnect(url="http://prometheus_node:9090", disable_ssl=True)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/detect-anomalies")
def detect_anomalies(query: str = "sum(rate(node_cpu_seconds_total[5m]))"):
    # Fetch last 1 hour of metric data
    metric_data = prom.custom_query_range(
        query=query,
        start_time=pd.Timestamp.now() - pd.Timedelta(hours=1),
        end_time=pd.Timestamp.now(),
        step="1m",
    )

    if not metric_data:
        return {"status": "no data"}

    # Convert Prometheus JSON into a DataFrame
    values = metric_data[0]["values"]
    df = pd.DataFrame(values, columns=["timestamp", "value"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df["value"] = df["value"].astype(float)

    # Resample to ensure uniform 1-minute intervals and fill gaps
    df = df.set_index("timestamp").resample("1min").mean().ffill()

    # 1. Anomaly detection
    iso_model = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = iso_model.fit_predict(df[["value"]])

    # 2. Forecast next CPU value (Linear Regression over time steps)
    X = np.arange(len(df)).reshape(-1, 1)
    y = df["value"].values
    reg_model = LinearRegression().fit(X, y)
    predicted_next_cpu = float(reg_model.predict([[len(df)]])[0])

    # Update Prometheus Gauges
    latest_is_anomaly = 1 if df["anomaly"].iloc[-1] == -1 else 0
    ANOMALY_SCORE.set(latest_is_anomaly)
    PREDICTED_CPU.set(predicted_next_cpu)

    anomalies = df[df["anomaly"] == -1].reset_index().to_dict(orient="records")
    return {
        "predicted_cpu": predicted_next_cpu,
        "latest_anomaly": latest_is_anomaly,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
    }
