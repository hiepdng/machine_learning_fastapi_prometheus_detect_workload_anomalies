## Machine Learning for CPU Anomaly Detection and Prediction with Prometheus, FastAPI and Grafana 


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
Run the below commands to download the demo repository and run the Docker containers.  
```
#Downloading the repository
git clone git@github.com:hiepdng/monitoring_metric_logs_traces_profiles_with_prometheus_grafana_stack.git

#Creating volumes
cd monitoring_metric_logs_traces_profiles_with_prometheus_grafana_stack
mkdir prometheus_data
sudo chown -R nobody:nogroup prometheus_data
mkdir grafana_data
sudo chown -R 472:472 grafana_data
mkdir loki_data
sudo chown -R 10001:10001 loki_data
mkdir alloy_data
sudo chown -R 473:473 alloy_data
mkdir tempo_data
sudo chown -R 10001:10001 tempo_data
mkdir pyroscope_data
sudo chown -R 10001:10001 pyroscope_data

#Running containers
docker compose up -d
```
