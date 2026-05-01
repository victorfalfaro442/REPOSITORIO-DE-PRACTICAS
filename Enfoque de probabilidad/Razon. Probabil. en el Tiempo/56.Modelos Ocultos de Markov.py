print("--- MODELO OCULTO DE MARKOV (HMM) ---")

# ==============================================================
# 1. DEFINICIÓN DEL MODELO
# ==============================================================
estados = ['Soleado', 'Lluvioso']
observaciones = ['Seco', 'Seco', 'Mojado', 'Mojado'] # Lo que vemos llegar

# P(X_t | X_{t-1})
transicion = {
    'Soleado':  {'Soleado': 0.8, 'Lluvioso': 0.2},
    'Lluvioso': {'Soleado': 0.3, 'Lluvioso': 0.7}
}

# P(E_t | X_t)
emision = {
    'Soleado':  {'Seco': 0.9, 'Mojado': 0.1},
    'Lluvioso': {'Seco': 0.2, 'Mojado': 0.8}
}

prob_inicial = {'Soleado': 0.5, 'Lluvioso': 0.5}

# ==============================================================
# 2. ALGORITMO DE VITERBI (Encuentra el camino más probable)
# ==============================================================
def viterbi(obs_seq):
    # viterbi_table[t][estado] almacenará la probabilidad máxima para llegar ahí
    viterbi_table = [{}]
    camino = {}

    # Paso 1: Inicialización (t=0)
    for estado in estados:
        viterbi_table[0][estado] = prob_inicial[estado] * emision[estado][obs_seq[0]]
        camino[estado] = [estado]

    # Paso 2: Recurrencia (t=1 a T)
    for t in range(1, len(obs_seq)):
        viterbi_table.append({})
        nuevo_camino = {}

        for estado_actual in estados:
            # Buscamos de qué estado previo venimos para maximizar la prob
            # (Prob_anterior * Prob_transicion * Prob_emision_actual)
            (prob, estado_previo) = max(
                (viterbi_table[t-1][e_prev] * transicion[e_prev][estado_actual] * emision[estado_actual][obs_seq[t]], e_prev)
                for e_prev in estados
            )
            
            viterbi_table[t][estado_actual] = prob
            nuevo_camino[estado_actual] = camino[estado_previo] + [estado_actual]

        camino = nuevo_camino

    # Paso 3: Conclusión (Elegir el final más probable)
    (prob_final, mejor_estado_final) = max((viterbi_table[-1][e], e) for e in estados)
    
    return camino[mejor_estado_final], prob_final

# ==============================================================
# 3. RESULTADOS
# ==============================================================
secuencia_clima, probabilidad = viterbi(observaciones)

print(f"\nObservaciones (Zapatos): {observaciones}")
print("-" * 50)
print(f"Secuencia de clima más probable: {' -> '.join(secuencia_clima)}")
print(f"Probabilidad de esta secuencia:  {probabilidad:.6f}")
