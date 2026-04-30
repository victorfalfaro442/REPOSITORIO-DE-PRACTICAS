import random

print("--- SIMULACIÓN DE PROCESO ESTACIONARIO (CADENA TEMPORAL) ---")

# ==============================================================
# 1. EL MODELO DE TRANSICIÓN (Estacionario)
# ==============================================================
# Estas probabilidades NO CAMBIAN a lo largo de la simulación.
# Es la esencia de la estacionariedad.
transiciones = {
    'Estable': {'Estable': 0.90, 'Burbuja': 0.10}, # Es difícil entrar en burbuja
    'Burbuja': {'Estable': 0.30, 'Burbuja': 0.70}  # Una vez dentro, es probable quedarse un tiempo
}

# ==============================================================
# 2. EL MOTOR DE EVOLUCIÓN TEMPORAL
# ==============================================================
def simular_paso_del_tiempo(estado_actual):
    """Aplica las reglas estacionarias para obtener el siguiente estado."""
    opciones = list(transiciones[estado_actual].keys())
    probabilidades = list(transiciones[estado_actual].values())
    
    # La IA predice el estado t basándose únicamente en t-1
    siguiente_estado = random.choices(opciones, weights=probabilidades, k=1)[0]
    return siguiente_estado

# ==============================================================
# 3. EJECUCIÓN: OBSERVANDO EL PROCESO EN EL TIEMPO
# ==============================================================
estado_inicial = 'Estable'
pasos_de_tiempo = 20

print(f"[*] Iniciando simulación estacionaria...")
print(f"[*] Reglas: P(Burbuja|Estable) = {transiciones['Estable']['Burbuja']:.2f}")
print("-" * 50)

historial = [estado_inicial]
estado_actual = estado_inicial

for t in range(1, pasos_de_tiempo + 1):
    estado_actual = simular_paso_del_tiempo(estado_actual)
    historial.append(estado_actual)
    
    # Formateo visual de la línea de tiempo
    simbolo = "📈" if estado_actual == 'Estable' else "🔥"
    print(f"Tiempo t={t:02d}: {estado_actual:8s} {simbolo}")

# ==============================================================
# 4. ANÁLISIS ESTADÍSTICO (Hacia el Estado Estacionario)
# ==============================================================
conteo_burbuja = historial.count('Burbuja')
porcentaje_burbuja = (conteo_burbuja / len(historial)) * 100

print("-" * 50)
print(f"RESULTADO: En {pasos_de_tiempo} pasos, el sistema estuvo en CRISIS el {porcentaje_burbuja:.1f}% del tiempo.")
