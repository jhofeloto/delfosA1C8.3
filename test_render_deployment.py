#!/usr/bin/env python3
"""
Script de pruebas para despliegue en Render
Sistema de Biomarcadores Digitales
"""

import requests
import json
import time
import sys
from typing import Dict, Any
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RenderDeploymentTester:
    """Tester para despliegue en Render"""

    def __init__(self, base_url: str = "https://delfos-biomarkers.onrender.com"):
        self.base_url = base_url.rstrip('/')
        self.test_results = {}

    def test_health_check(self) -> bool:
        """Probar health check de la aplicación"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                logger.info("✅ Health check exitoso")
                self.test_results['health_check'] = True
                return True
            else:
                logger.error(f"❌ Health check falló: {response.status_code}")
                self.test_results['health_check'] = False
                return False
        except Exception as e:
            logger.error(f"❌ Error en health check: {e}")
            self.test_results['health_check'] = False
            return False

    def test_mlflow_ui(self) -> bool:
        """Probar MLflow UI"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                logger.info("✅ MLflow UI accesible")
                self.test_results['mlflow_ui'] = True
                return True
            else:
                logger.error(f"❌ MLflow UI no accesible: {response.status_code}")
                self.test_results['mlflow_ui'] = False
                return False
        except Exception as e:
            logger.error(f"❌ Error accediendo MLflow UI: {e}")
            self.test_results['mlflow_ui'] = False
            return False

    def test_api_docs(self) -> bool:
        """Probar documentación de API"""
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=10)
            if response.status_code == 200:
                logger.info("✅ API docs accesible")
                self.test_results['api_docs'] = True
                return True
            else:
                logger.error(f"❌ API docs no accesible: {response.status_code}")
                self.test_results['api_docs'] = False
                return False
        except Exception as e:
            logger.error(f"❌ Error accediendo API docs: {e}")
            self.test_results['api_docs'] = False
            return False

    def test_prediction_endpoint(self) -> bool:
        """Probar endpoint de predicción"""
        test_data = {
            "edad": 45,
            "sexo": "F",
            "peso": 70.5,
            "altura": 165,
            "presion_sistolica": 120,
            "presion_diastolica": 80,
            "glucosa": 95,
            "colesterol_total": 180,
            "colesterol_hdl": 50,
            "colesterol_ldl": 110,
            "trigliceridos": 150,
            "imc": 25.8,
            "perimetro_abdominal": 85,
            "actividad_fisica": "moderada",
            "historial_familiar": "si",
            "tabaquismo": "no",
            "consumo_alcohol": "ocasional"
        }

        try:
            response = requests.post(
                f"{self.base_url}/predict",
                json=test_data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Predicción exitosa: {result}")
                self.test_results['prediction'] = True
                return True
            else:
                logger.error(f"❌ Predicción falló: {response.status_code} - {response.text}")
                self.test_results['prediction'] = False
                return False
        except Exception as e:
            logger.error(f"❌ Error en predicción: {e}")
            self.test_results['prediction'] = False
            return False

    def test_dashboard(self) -> bool:
        """Probar dashboard"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                logger.info("✅ Dashboard accesible")
                self.test_results['dashboard'] = True
                return True
            else:
                logger.error(f"❌ Dashboard no accesible: {response.status_code}")
                self.test_results['dashboard'] = False
                return False
        except Exception as e:
            logger.error(f"❌ Error accediendo dashboard: {e}")
            self.test_results['dashboard'] = False
            return False

    def test_performance(self) -> bool:
        """Probar rendimiento de la API"""
        test_data = {
            "edad": 50,
            "sexo": "M",
            "peso": 80.0,
            "altura": 175,
            "presion_sistolica": 130,
            "presion_diastolica": 85,
            "glucosa": 110,
            "colesterol_total": 200,
            "colesterol_hdl": 45,
            "colesterol_ldl": 120,
            "trigliceridos": 180,
            "imc": 26.1,
            "perimetro_abdominal": 95,
            "actividad_fisica": "baja",
            "historial_familiar": "si",
            "tabaquismo": "si",
            "consumo_alcohol": "moderado"
        }

        times = []
        for i in range(3):  # Menos requests para Render (más lento)
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.base_url}/predict",
                    json=test_data,
                    timeout=30
                )
                end_time = time.time()

                if response.status_code == 200:
                    times.append(end_time - start_time)
                else:
                    logger.error(f"❌ Request {i+1} falló: {response.status_code}")
                    return False
            except Exception as e:
                logger.error(f"❌ Error en request {i+1}: {e}")
                return False

        avg_time = sum(times) / len(times)
        max_time = max(times)

        logger.info(f"✅ Rendimiento: {len(times)} requests exitosos")
        logger.info(f"   Tiempo promedio: {avg_time:.2f}s")
        logger.info(f"   Tiempo máximo: {max_time:.2f}s")

        # Render puede ser más lento en cold starts
        if avg_time < 10.0 and max_time < 20.0:
            self.test_results['performance'] = True
            return True
        else:
            logger.warning("⚠️  Rendimiento por debajo del umbral esperado (normal en Render)")
            self.test_results['performance'] = False
            return False

    def test_ssl_certificate(self) -> bool:
        """Probar certificado SSL"""
        try:
            import ssl
            import urllib3
            from urllib.parse import urlparse

            parsed_url = urlparse(self.base_url)
            if parsed_url.scheme != 'https':
                logger.warning("⚠️  No se está usando HTTPS")
                self.test_results['ssl'] = False
                return False

            # Verificar certificado
            response = requests.get(self.base_url, timeout=10, verify=True)
            if response.status_code == 200:
                logger.info("✅ Certificado SSL válido")
                self.test_results['ssl'] = True
                return True
            else:
                logger.error(f"❌ Error con SSL: {response.status_code}")
                self.test_results['ssl'] = False
                return False
        except Exception as e:
            logger.error(f"❌ Error verificando SSL: {e}")
            self.test_results['ssl'] = False
            return False

    def run_all_tests(self) -> Dict[str, Any]:
        """Ejecutar todas las pruebas"""
        logger.info("🚀 Iniciando pruebas de despliegue en Render...")
        logger.info(f"🌐 URL base: {self.base_url}")
        logger.info("-" * 50)

        tests = [
            ("Health Check", self.test_health_check),
            ("SSL Certificate", self.test_ssl_certificate),
            ("MLflow UI", self.test_mlflow_ui),
            ("API Docs", self.test_api_docs),
            ("Prediction Endpoint", self.test_prediction_endpoint),
            ("Dashboard", self.test_dashboard),
            ("Performance", self.test_performance),
        ]

        for test_name, test_func in tests:
            logger.info(f"🔍 Probando: {test_name}")
            try:
                test_func()
            except Exception as e:
                logger.error(f"❌ Error ejecutando {test_name}: {e}")
                self.test_results[test_name.lower().replace(" ", "_")] = False
            logger.info("")

        # Resumen
        self.print_summary()
        return self.test_results

    def print_summary(self):
        """Imprimir resumen de resultados"""
        logger.info("📊 RESUMEN DE PRUEBAS")
        logger.info("-" * 50)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)

        logger.info(f"Total de pruebas: {total_tests}")
        logger.info(f"Pruebas exitosas: {passed_tests}")
        logger.info(f"Pruebas fallidas: {total_tests - passed_tests}")
        logger.info(f"Tasa de éxito: {(passed_tests/total_tests)*100:.1f}%")

        logger.info("\n📋 Detalle de resultados:")
        for test, result in self.test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"  {test}: {status}")

        if passed_tests == total_tests:
            logger.info("\n🎉 ¡Todas las pruebas pasaron! El despliegue está funcionando correctamente.")
            return True
        else:
            logger.warning(f"\n⚠️  {total_tests - passed_tests} pruebas fallaron. Revisa los logs para más detalles.")
            return False

def main():
    """Función principal"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "https://delfos-biomarkers.onrender.com"

    tester = RenderDeploymentTester(base_url)
    results = tester.run_all_tests()

    # Salir con código apropiado
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()