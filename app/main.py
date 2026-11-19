from fastapi import FastAPI
from prometheus_api_client import PrometheusConnect
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest

import time
from prometheus_client import  Histogram, Counter, Gauge, make_asgi_app

app = FastAPI()

# Define custom Gauge metrics for ML outputs
ANOMALY_SCORE = Gauge("ml_cpu_anomaly_flag", "1 if anomaly detected, 0 otherwise")
PREDICTED_CPU = Gauge("ml_cpu_predicted_value", "Predicted CPU usage")


prom = PrometheusConnect(url="http://prometheus_node:9090", disable_ssl=True)

###There are three methods to expose standard HTTP metrics at /metrics:
### 1:
### from prometheus_client import start_http_server
### start_http_server(8001)        <-you need to expose port 8001 at Dockerfile
### 2:
### from prometheus_client import start_http_server
### from prometheus_fastapi_instrumentator import Instrumentator
### Instrumentator().instrument(app).expose(app)
### 3: below
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/detect-anomalies")
#def detect_anomalies(query: str = "rate(http_requests_total[5m])"):
#def detect_anomalies(query: str = "rate(node_cpu_seconds_total{mode='system'}[5m])"):
def detect_anomalies(query: str = "sum by (instance, mode) (rate(node_cpu_seconds_total[5m]))"):
def detect_anomalies(query: str = "1 - rate(node_cpu_seconds_total{mode="idle"}[5m])"):

 
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

    # Train/run lightweight anomaly detection
    model = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = model.fit_predict(df[["value"]])

    anomalies = df[df["anomaly"] == -1].to_dict(orient="records")

    #is_anomaly = 1 if latest_prediction == -1 else 0
    is_anomaly = 1 if anomalies == -1 else 0

    ANOMALY_SCORE.set(is_anomaly)
    return {"anomaly_count": len(anomalies), "anomalies": anomalies}

