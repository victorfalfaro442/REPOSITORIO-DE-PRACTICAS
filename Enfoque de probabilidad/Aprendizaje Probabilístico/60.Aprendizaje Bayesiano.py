print("--- ALGORITMO DE APRENDIZAJE BAYESIANO ---")

# ==============================================================
# 1. EL ESPACIO DE HIPÓTESIS (Las reglas de la fábrica)
# ==============================================================
# P(D|h): Probabilidad de sacar un sabor dado el tipo de bolsa
hipotesis = {
    'h1 (100% C)': {'Cereza': 1.00, 'Lima': 0.00},
    'h2 (75% C)':  {'Cereza': 0.75, 'Lima': 0.25},
    'h3 (50/50)':  {'Cereza': 0.50, 'Lima': 0.50},
    'h4 (25% C)':  {'Cereza': 0.25, 'Lima': 0.75},
    'h5 (100% L)': {'Cereza': 0.00, 'Lima': 1.00}
}

# ==============================================================
# 2. LA CREENCIA PREVIA (Prior)
# ==============================================================
# P(h): Lo que la IA cree antes de abrir la bolsa.
# (Asumimos que las bolsas 50/50 son las más comunes en la fábrica)
creencia = {
    'h1 (100% C)': 0.10,
    'h2 (75% C)':  0.20,
    'h3 (50/50)':  0.40,
    'h4 (25% C)':  0.20,
    'h5 (100% L)': 0.10
}

# ==============================================================
# 3. EL MOTOR DE APRENDIZAJE (Actualización Bayesiana)
# ==============================================================
def aprender_de_dato(dato, creencias_actuales):
    nuevas_creencias = {}
    prob_dato_total = 0.0
    
    # Paso A: Calcular el numerador (Verosimilitud * Previa) para cada hipótesis
    for h, prob_h in creencias_actuales.items():
        verosimilitud = hipotesis[h][dato]
        numerador = verosimilitud * prob_h
        nuevas_creencias[h] = numerador
        prob_dato_total += numerador  # Vamos sumando para el denominador
        
    # Paso B: Normalizar (Dividir entre el denominador)
    for h in nuevas_creencias:
        if prob_dato_total > 0:
            nuevas_creencias[h] /= prob_dato_total
        else:
            nuevas_creencias[h] = 0.0
            
    return nuevas_creencias

def predecir_siguiente(sabor, creencias_actuales):
    """Pide a todas las hipótesis que voten ponderadamente por el próximo sabor."""
    prob_predicha = sum(hipotesis[h][sabor] * prob_h for h, prob_h in creencias_actuales.items())
    return prob_predicha

# ==============================================================
# 4. SIMULACIÓN: OBSERVANDO LOS DATOS
# ==============================================================
# Sacamos 5 caramelos de la bolsa. ¡Todos resultan ser Cereza!
secuencia_datos = ["Cereza", "Lima", "Cereza", "Lima", "Cereza"]

print(f"Estado Inicial:")
print(f"  Predicción de sacar Cereza en el turno 1: {predecir_siguiente('Cereza', creencia)*100:.1f}%")
print("-" * 55)

for turno, dato in enumerate(secuencia_datos, 1):
    # La IA aprende del nuevo dato
    creencia = aprender_de_dato(dato, creencia)
    
    print(f"\nTurno {turno} | Extraído: {dato}")
    
    # Mostramos cómo cambia la mente de la IA
    for h, prob in creencia.items():
        if prob > 0.01: # Solo mostramos las hipótesis que aún tienen peso
            print(f"  -> Prob. de estar en {h:<12}: {prob*100:>6.1f}%")
            
    # Hacemos una predicción para el futuro basada en el aprendizaje actual
    prob_futura = predecir_siguiente('Cereza', creencia)
    print(f"  [!] Certeza de que el próximo sea Cereza: {prob_futura*100:.1f}%")

print("\n" + "="*55)
print("CONCLUSIÓN DEL APRENDIZAJE:")
hipotesis_ganadora = max(creencia, key=creencia.get)
print(f"La IA concluye que casi seguro estamos en la bolsa: {hipotesis_ganadora}")