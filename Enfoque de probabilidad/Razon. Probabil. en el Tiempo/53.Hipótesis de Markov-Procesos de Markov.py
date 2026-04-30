import random

print("--- IMPLEMENTACIÓN: PROCESO DE MARKOV (Primer Orden) ---")

# ==============================================================
# 1. DEFINICIÓN DE ESTADOS
# ==============================================================
estados = ['Operativo', 'Lento', 'Caído']

# ==============================================================
# 2. MATRIZ DE TRANSICIÓN (La esencia de Markov)
# ==============================================================
# P(Siguiente | Actual)
# Cada fila suma 1.0 (Normalización)
modelo_transicion = {
    'Operativo': {'Operativo': 0.85, 'Lento': 0.10, 'Caído': 0.05},
    'Lento':     {'Operativo': 0.20, 'Lento': 0.60, 'Caído': 0.20},
    'Caído':     {'Operativo': 0.50, 'Lento': 0.10, 'Caído': 0.40} # El 0.50 es por el técnico reparando
}

# ==============================================================
# 3. EL ALGORITMO DE PREDICCIÓN MARKOVIANA
# ==============================================================
def predecir_siguiente_estado(estado_presente):
    """
    Basado estrictamente en la Hipótesis de Markov:
    El futuro SOLO depende del presente.
    """
    probabilidades = modelo_transicion[estado_presente]
    
    # Extraemos opciones y sus pesos
    opciones = list(probabilidades.keys())
    pesos = list(probabilidades.values())
    
    # Realizamos el salto estocástico
    return random.choices(opciones, weights=pesos, k=1)[0]

# ==============================================================
# 4. SIMULACIÓN TEMPORAL (24 horas)
# ==============================================================
estado_actual = 'Operativo'
print(f"[*] Estado inicial (t=0): {estado_actual}")
print("-" * 40)

for hora in range(1, 25):
    # La IA no mira el historial, solo mira 'estado_actual'
    estado_siguiente = predecir_siguiente_estado(estado_actual)
    
    # Mostramos el cambio si ocurre
    if estado_siguiente != estado_actual:
        print(f"Hora {hora:02d}: Transición de {estado_actual} -> {estado_siguiente}")
    
    estado_actual = estado_siguiente

print("-" * 40)
print(f"[*] Estado final después de 24h: {estado_actual}")
