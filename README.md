## Workload Anomaly Detection and Prediction with FastAPI, Prometheus, and Machine Learning


Applying machine learning to node_cpu_seconds_total means using time-series algorithms—such as anomaly detection, forecasting, and workload clustering—on CPU utilization rates derived from this Prometheus Node Exporter metric. Rather than relying on rigid static thresholds (like alerting whenever CPU passes 80%), ML models learn normal cyclical patterns across CPU modes to flag unusual behavior and predict future resource exhaustion  

This is a complete setup using Docker inmages, included prom/prometheus, prom/node-exporter, grafana and python, along with FastAPI  Python web framework.  

File structure:  
├── app  
│   ├── Dockerfile.app  
│   ├── main.py  
│   └── requirements.txt  
├── docker-compose.yml  
├── grafana_data/  
├── grafana-datasources.yaml/  
├── prometheus_data/  
├── prometheus_node_data/  
├── prometheus_node.yml  
└── prometheus.yml  

**Setup:**  
Run the below commands to download the demo repository and run this setup.  
```
#Downloading the repository
git clone git@github.com:hiepdng/machine_learning_fastapi_prometheus_detect_workload_anomalies.git

#Creating volumes
cd monitoring_metric_logs_traces_profiles_with_prometheus_grafana_stack
mkdir app
mkdir prometheus_data
sudo chown -R nobody:nogroup prometheus_data
mkdir prometheus_node_data
sudo chown -R nobody:nogroup prometheus_node_data
mkdir grafana_data
sudo chown -R 472:472 grafana_data

#Running containers
docker compose up -d
```
**Note:**  
- The `app` directory contains all need files to build ml-api, which is used to calculate anomalies and predictions of workload (CPU).  
- There are two Prometheus instances:  
  - The `prometheus` is for scraping ml-api's metrics for Grafana to pull.  
  - The `prometheus_node is for scraping node-exporter's metrics for ml-api to pull.
 
**Access Grafana web:**  
Go to http://localhost:3000/ to access your local Grafana webpage and monitor Drilldown Metrics. It will show `ml_cpu_anomaly_flag` and `ml_cpu_predicted_value`qq

To view specific container webpages:  
- ml-api: http://localhost:8000/, http://localhost:8000/docs, http://localhost:8000/redoc
- Node-exporter: http://localhost:9100/ or http://localhost:9100/metrics
- Prometheus: http://localhost:9090/
- Prometheus_node: http://localhost:9091/
<br>

**View Grafana Drilldown Metrics, Logs, Traces and Profiles:**  
To view a corresponding page:
- Go to http://localhost:3000/
- Click on **Drilldown** ➔ **Metrics**, **Logs**, **Traces** or **Profiles**
- Note:
  - **Metrics** requires **Prometheus** data source.
  - **Logs** requires **Loki** data source.
  - **Traces** requires **Tempo** data source.
  - **Profiles** required **Pyroscope** data source.
  
  All of the required data sources are included in the grafana-datasources.yaml file.  If a data source is missing or if you want to modify data source options,  click on **Connections**➔**Data sources**➔**Add new data source** and enter properly options.  
<br>
