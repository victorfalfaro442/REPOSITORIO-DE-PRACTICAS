print("--- ALGORITMO HACIA ADELANTE-ATRÁS ---")

# ==============================================================
# 1. EL MODELO (Probabilidades de Lluvia)
# ==============================================================
# [0] = Lluvia, [1] = No Lluvia
transicion = [
    [0.7, 0.3], # De Lluvia pasa a: [Lluvia, No Lluvia]
    [0.3, 0.7]  # De No Lluvia pasa a: [Lluvia, No Lluvia]
]

sensor = [
    [0.9, 0.1], # Lluvia: [Paraguas, No Paraguas]
    [0.2, 0.8]  # No Lluvia: [Paraguas, No Paraguas]
]

evidencias = ["Paraguas", "Paraguas", "No Paraguas"]

# ==============================================================
# 2. FUNCIONES DE APOYO 
# ==============================================================
def normalizar(vector):
    suma = sum(vector)
    return [v / suma for v in vector]

def predecir_paso(creencia_actual):
    # Multiplicación manual: creencia * matriz_transicion
    nueva_p_lluvia = (creencia_actual[0] * transicion[0][0]) + (creencia_actual[1] * transicion[1][0])
    nueva_p_no_lluvia = (creencia_actual[0] * transicion[0][1]) + (creencia_actual[1] * transicion[1][1])
    return [nueva_p_lluvia, nueva_p_no_lluvia]

# ==============================================================
# 3. PASADA HACIA ADELANTE (FORWARD / FILTRADO)
# ==============================================================
f = [[0.5, 0.5]] # Empezamos con 50/50 en t=0

for ev in evidencias:
    idx_ev = 0 if ev == "Paraguas" else 1
    
    # A. Predicción
    creencia_p = predecir_paso(f[-1])
    
    # B. Actualización con sensor (Filtrado)
    p_lluvia = creencia_p[0] * sensor[0][idx_ev]
    p_no_lluvia = creencia_p[1] * sensor[1][idx_ev]
    
    f.append(normalizar([p_lluvia, p_no_lluvia]))

print("[*] Pasada Forward (Filtrado) finalizada.")

# ==============================================================
# 4. PASADA HACIA ATRÁS (BACKWARD)
# ==============================================================
# El mensaje inicial hacia atrás (b) siempre es [1, 1] en el tiempo final
b = [[1.0, 1.0]]

# Recorremos las evidencias al revés (del día 3 al 1)
for ev in reversed(evidencias):
    idx_ev = 0 if ev == "Paraguas" else 1
    
    # Calculamos b_k: Probabilidad de las evidencias futuras dado el estado actual
    # b_k(i) = sum_j( P(X_j|X_i) * P(e|X_j) * b_k+1(j) )
    b_actual = [0.0, 0.0]
    for i in range(2): # Para cada estado actual (Lluvia/No Lluvia)
        suma_prob = 0
        for j in range(2): # Para cada estado futuro posible
            suma_prob += transicion[i][j] * sensor[j][idx_ev] * b[0][j]
        b_actual[i] = suma_prob
    
    b.insert(0, b_actual)

print("[*] Pasada Backward finalizada.")

# ==============================================================
# 5. RESULTADO FINAL (SUAVIZADO)
# ==============================================================
print("\n" + "="*55)
print(f"{'Día':<5} | {'Filtrado (Lluvia)':<18} | {'Suavizado (Lluvia)':<18}")
print("-" * 55)

for t in range(1, len(f)):
    # El suavizado es el producto de f (lo que sé del pasado) y b (lo que sé del futuro)
    prob_suavizada_lluvia = f[t][0] * b[t][0]
    prob_suavizada_no_lluvia = f[t][1] * b[t][1]
    
    final = normalizar([prob_suavizada_lluvia, prob_suavizada_no_lluvia])
    
    print(f"t={t}   | {f[t][0]*100:>15.2f}% | {final[0]*100:>15.2f}%")
