#!/bin/bash
echo "🌐 Iniciando Interfaz Web del Sistema Predictivo de Diabetes"
echo "📍 URL: http://localhost:8501"
streamlit run web_app.py --server.port 8501 --server.address 0.0.0.0
