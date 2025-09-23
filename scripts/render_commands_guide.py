#!/usr/bin/env python3
"""
DÓNDE CONFIGURAR LOS COMANDOS BUILD Y START EN RENDER
"""

print("🔍 DÓNDE ENCONTRAR LOS CAMPOS BUILD COMMAND Y START COMMAND")
print("="*70)

print("\n❌ PROBLEMA:")
print("   Los campos 'Build Command' y 'Start Command'")
print("   NO APARECEN hasta que cambies de Docker a Python 3")

print("\n✅ SOLUCIÓN - PASO A PASO:")
print("   ")

print("   PASO 1: IR A SETTINGS")
print("   +-------------------------------+")
print("   | Dashboard > Tu Servicio      |")
print("   | > Settings                   |")
print("   +-------------------------------+")

print("\n   PASO 2: BUSCAR BUILD & DEPLOY")
print("   +-------------------------------+")
print("   | Build & Deploy section       |")
print("   +-------------------------------+")

print("\n   PASO 3: CAMBIAR DOCKERFILE PATH")
print("   +-------------------------------+")
print("   | Dockerfile Path: ./Dockerfile|")
print("   |                              |")
print("   | CAMBIA A: No Dockerfile     |")
print("   +-------------------------------+")
print("   ")
print("   ⚠️ HAZ CLIC EN 'Save Changes' AQUÍ")
print("   ⚠️ ESPERA 10 SEGUNDOS")

print("\n   PASO 4: REFRESCA LA PÁGINA")
print("   +-------------------------------+")
print("   | F5 o Command+R               |")
print("   +-------------------------------+")

print("\n   PASO 5: AHORA VERÁS LOS CAMPOS")
print("   +-------------------------------+")
print("   | Runtime: Python 3            |")
print("   |                              |")
print("   | Build Command: [campo vacío] |")
print("   |                              |")
print("   | Start Command: [campo vacío] |")
print("   +-------------------------------+")

print("\n📝 CONFIGURACIÓN FINAL:")
print("   ")
print("   Build Command:")
print("   +-------------------------------+")
print("   | pip install -r requirements.txt|")
print("   +-------------------------------+")
print("   ")
print("   Start Command:")
print("   +-------------------------------+")
print("   | python api.py --host 0.0.0.0 |")
print("   | --port $PORT                 |")
print("   +-------------------------------+")

print("\n🎯 RESUMEN:")
print("   1. Cambiar Dockerfile Path → No Dockerfile")
print("   2. Guardar cambios")
print("   3. Refrescar página")
print("   4. Aparecerán Build Command y Start Command")
print("   5. Llenar los campos")
print("   6. Guardar nuevamente")

print("\n💡 ¿POR QUÉ NO APARECEN?")
print("   Render solo muestra estos campos cuando")
print("   detecta que es un servicio Python nativo,")
print("   no Docker. El cambio de Dockerfile Path")
print("   es lo que activa el modo Python 3.")

print("\n🔍 SI SIGUE SIN APARECER:")
print("   • Espera 30 segundos")
print("   • Refresca la página")
print("   • Cierra y vuelve a abrir el navegador")
print("   • Verifica que guardaste el cambio")

print("\n📞 AYUDA:")
print("   Si después de cambiar a 'No Dockerfile'")
print("   no aparecen los campos, toma una captura")
print("   de pantalla de lo que ves y muéstramela.")