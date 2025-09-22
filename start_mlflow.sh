#!/bin/bash
echo "📊 Iniciando MLflow UI"
echo "📍 URL: http://localhost:5000"
mlflow ui --backend-store-uri outputs/mlruns --host 0.0.0.0 --port 5000
