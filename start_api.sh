#!/bin/bash
echo "🏥 Iniciando API REST del Sistema Predictivo de Diabetes"
echo "📍 URL: http://localhost:8000"
echo "📚 Documentación: http://localhost:8000/docs"
python api.py --host 0.0.0.0 --port 8000
