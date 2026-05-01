import numpy as np

print("--- MOTOR DE INFERENCIA TEMPORAL: FILTRADO Y PREDICCIÓN ---")

# ==============================================================
# 1. EL MODELO (Parámetros Estacionarios)
# ==============================================================
# Estados: [Lluvia, No Lluvia]
# P(X_t | X_t-1) - Probabilidades de transición
modelo_transicion = np.array([
    [0.7, 0.3], # Si hoy llueve, mañana llueve con 0.7
    [0.3, 0.7]  # Si hoy no llueve, mañana no llueve con 0.7
])

# P(E_t | X_t) - Probabilidades de sensor (Paraguas)
# Si llueve, hay paraguas con 0.9. Si no llueve, con 0.2.
modelo_sensor = np.array([
    [0.9, 0.1], # Lluvia: [Paraguas, No Paraguas]
    [0.2, 0.8]  # No Lluvia: [Paraguas, No Paraguas]
])

# Creencia inicial P(X_0): [Lluvia: 0.5, No Lluvia: 0.5]
creencia = np.array([0.5, 0.5])

# ==============================================================
# 2. LAS FUNCIONES MAESTRAS
# ==============================================================

def predecir(creencia_actual):
    """Tarea 2: Predicción - Mover la creencia al futuro."""
    # Multiplicamos la creencia por la matriz de transición
    return np.dot(creencia_actual, modelo_transicion)

def filtrar(creencia_predicha, evidencia_observada):
    """Tarea 1: Filtrado - Actualizar futuro con nueva evidencia."""
    # 1. Ver qué columna de la matriz de sensor usamos (0: Paraguas, 1: No)
    idx_evidencia = 0 if evidencia_observada == "Paraguas" else 1
    prob_evidencia = modelo_sensor[:, idx_evidencia]
    
    # 2. Multiplicar punto a punto y NORMALIZAR
    nueva_creencia = creencia_predicha * prob_evidencia
    return nueva_creencia / np.sum(nueva_creencia)

# ==============================================================
# 3. EJECUCIÓN EN EL TIEMPO
# ==============================================================
secuencia_evidencias = ["Paraguas", "Paraguas", "No Paraguas"]

print(f"Estado inicial: Lluvia={creencia[0]*100}%, No Lluvia={creencia[1]*100}%")
print("-" * 50)

historial_creencias = [creencia]

for t, ev in enumerate(secuencia_evidencias):
    # PASO 1: Predicción (¿Qué espero que pase?)
    creencia_p = predecir(creencia)
    
    # PASO 2: Filtrado (¿Qué pasó realmente?)
    creencia = filtrar(creencia_p, ev)
    historial_creencias.append(creencia)
    
    print(f"Día {t+1} - Evidencia: {ev}")
    print(f"  -> Predicción: Lluvia {creencia_p[0]*100:.1f}%")
    print(f"  -> Filtrado (POSTERIOR): Lluvia {creencia[0]*100:.1f}%")

# ==============================================================
# 4. EXPLICACIÓN (Simbolizada)
# ==============================================================
print("-" * 50)
secuencia_final = ["Lluvia" if c[0] > c[1] else "No Lluvia" for c in historial_creencias[1:]]
print(f"EXPLICACIÓN MÁS PROBABLE (Secuencia): {' -> '.join(secuencia_final)}")
