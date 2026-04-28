import random

print("--- ALGORITMO: PONDERACIÓN DE VEROSIMILITUD ---")

# ==============================================================
# 1. EL UNIVERSO: LA RED BAYESIANA (Tablas de Probabilidad)
# ==============================================================
# P(Cielo Nublado) = 50%
prob_cielo = {'Nublado': 0.5, 'Despejado': 0.5}

# El Regador depende del Cielo (P(Regador | Cielo))
prob_regador = {
    'Nublado': {'Encendido': 0.1, 'Apagado': 0.9},   # Nadie riega si está nublado
    'Despejado': {'Encendido': 0.5, 'Apagado': 0.5}  # 50/50 si hace sol
}

# La Lluvia depende del Cielo (P(Lluvia | Cielo))
prob_lluvia = {
    'Nublado': {'Si': 0.8, 'No': 0.2},
    'Despejado': {'Si': 0.1, 'No': 0.9}
}

# El Césped Mojado depende del Regador y la Lluvia (P(Mojado | Regador, Lluvia))
# Formato: (Regador, Lluvia) -> Probabilidad de que esté mojado
prob_cesped_mojado = {
    ('Encendido', 'Si'): {'Si': 0.99, 'No': 0.01},
    ('Encendido', 'No'): {'Si': 0.90, 'No': 0.10},
    ('Apagado', 'Si'): {'Si': 0.80, 'No': 0.20},
    ('Apagado', 'No'): {'Si': 0.00, 'No': 1.00}
}

# ==============================================================
# 2. FUNCIONES DE AYUDA PARA SIMULAR
# ==============================================================
def tirar_dado(probabilidad_exito):
    """Devuelve True si el evento ocurre basado en su probabilidad."""
    return random.random() < probabilidad_exito

# ==============================================================
# 3. EL ALGORITMO DE PONDERACIÓN 
# ==============================================================
def generar_muestra_ponderada(evidencia):
    """
    Genera UNA simulación del universo.
    fuerza las evidencias y devuelve (resultado_variables, peso_de_la_muestra).
    """
    # Empezamos asumiendo que esta simulación es perfectamente normal (peso = 1.0)
    peso = 1.0
    muestra = {}

    # 1. Simular el Cielo (No hay padres, es el origen)
    # Como no está en nuestra evidencia, lo simulamos libremente.
    if tirar_dado(prob_cielo['Nublado']):
        muestra['Cielo'] = 'Nublado'
    else:
        muestra['Cielo'] = 'Despejado'

    # 2. Variable: Lluvia
    # ¡ALTO! La lluvia ESTÁ en nuestra evidencia (Sabemos que es 'No').
    # No tiramos dados. La forzamos y multiplicamos el peso.
    cielo_actual = muestra['Cielo']
    
    if 'Lluvia' in evidencia:
        valor_forzado = evidencia['Lluvia']
        muestra['Lluvia'] = valor_forzado
        # Actualizamos el peso: ¿Qué tan probable era que no lloviera dado el cielo actual?
        peso *= prob_lluvia[cielo_actual][valor_forzado]
    else:
        # (Si no fuera evidencia, la simularíamos normal)
        pass 

    # 3. Variable: Regador
    # No es evidencia, queremos descubrirlo. Tiramos dados condicionados al cielo.
    prob_regador_encendido = prob_regador[cielo_actual]['Encendido']
    if tirar_dado(prob_regador_encendido):
        muestra['Regador'] = 'Encendido'
    else:
        muestra['Regador'] = 'Apagado'

    # 4. Variable: Césped Mojado
    # ¡ALTO! ESTÁ en nuestra evidencia (Sabemos que es 'Si').
    # Lo forzamos y castigamos/premiamos el peso.
    estado_regador = muestra['Regador']
    estado_lluvia = muestra['Lluvia']
    
    if 'Cesped' in evidencia:
        valor_forzado = evidencia['Cesped']
        muestra['Cesped'] = valor_forzado
        # Actualizamos el peso basado en sus padres (Regador y Lluvia)
        peso *= prob_cesped_mojado[(estado_regador, estado_lluvia)][valor_forzado]

    return muestra, peso

# ==============================================================
# 4. EJECUTANDO LA INFERENCIA PROBABILÍSTICA
# ==============================================================
evidencia_observada = {'Cesped': 'Si', 'Lluvia': 'No'}
num_simulaciones = 10000

# Aquí acumularemos la SUMA DE LOS PESOS para cuando el regador está encendido o apagado
suma_pesos_regador = {'Encendido': 0.0, 'Apagado': 0.0}

print("[*] Evidencia forzada: Césped=Si, Lluvia=No")
print(f"[*] Generando {num_simulaciones} universos paralelos ponderados...\n")

for _ in range(num_simulaciones):
    muestra, peso_muestra = generar_muestra_ponderada(evidencia_observada)
    
    # Anotamos qué pasó con el regador en este universo, y le sumamos SU PESO (no solo contar 1)
    estado_regador_en_muestra = muestra['Regador']
    suma_pesos_regador[estado_regador_en_muestra] += peso_muestra

# ==============================================================
# 5. NORMALIZACIÓN Y RESULTADOS
# ==============================================================
peso_total = sum(suma_pesos_regador.values())

prob_regador_encendido = (suma_pesos_regador['Encendido'] / peso_total) * 100
prob_regador_apagado = (suma_pesos_regador['Apagado'] / peso_total) * 100

print("="*50)
print(" RESULTADOS DE LA PONDERACIÓN DE VEROSIMILITUD ")
print("="*50)
print(f"Probabilidad de que el Regador esté ENCENDIDO: {prob_regador_encendido:.1f}%")
print(f"Probabilidad de que el Regador esté APAGADO:   {prob_regador_apagado:.1f}%")
