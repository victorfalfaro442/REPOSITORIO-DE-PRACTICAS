import math

print("--- APRENDIZAJE DE HMM: ALGORITMO DE BAUM-WELCH ---")

# ==============================================================
# 1. DATOS DE ENTRENAMIENTO (La secuencia que la IA debe aprender)
# ==============================================================
# Imagina que esto es una secuencia de "Sol" (0) y "Lluvia" (1) observada
observaciones = [0, 0, 1, 1, 0, 1, 1, 0]
n_estados = 2
n_simbolos = 2

# ==============================================================
# 2. INICIALIZACIÓN (Empezamos con sospechas al azar)
# ==============================================================
# P(X_t | X_t-1)
A = [[0.5, 0.5], [0.5, 0.5]] 
# P(E_t | X_t)
B = [[0.4, 0.6], [0.6, 0.4]] 
# P(X_0)
pi = [0.5, 0.5]

# ==============================================================
# 3. FUNCIONES DEL ALGORITMO
# ==============================================================

def forward(obs, A, B, pi):
    T = len(obs)
    alpha = [[0] * n_estados for _ in range(T)]
    for i in range(n_estados):
        alpha[0][i] = pi[i] * B[i][obs[0]]
    for t in range(1, T):
        for j in range(n_estados):
            alpha[t][j] = sum(alpha[t-1][i] * A[i][j] for i in range(n_estados)) * B[j][obs[t]]
    return alpha

def backward(obs, A, B):
    T = len(obs)
    beta = [[0] * n_estados for _ in range(T)]
    for i in range(n_estados):
        beta[T-1][i] = 1
    for t in range(T-2, -1, -1):
        for i in range(n_estados):
            beta[t][i] = sum(A[i][j] * B[j][obs[t+1]] * beta[t+1][j] for j in range(n_estados))
    return beta

# ==============================================================
# 4. BUCLE DE APRENDIZAJE (Baum-Welch / EM)
# ==============================================================
for iteracion in range(5):
    # --- PASO E: Calcular probabilidades con el modelo actual ---
    alpha = forward(observaciones, A, B, pi)
    beta = backward(observaciones, A, B)
    T = len(observaciones)
    
    # Probabilidad total de la observación
    P_obs = sum(alpha[T-1][i] for i in range(n_estados))
    
    # xi[t][i][j] = Prob de estar en i en t y j en t+1
    xi = [[[0] * n_estados for _ in range(n_estados)] for _ in range(T-1)]
    for t in range(T-1):
        for i in range(n_estados):
            for j in range(n_estados):
                numerador = alpha[t][i] * A[i][j] * B[j][observaciones[t+1]] * beta[t+1][j]
                xi[t][i][j] = numerador / P_obs

    # gamma[t][i] = Prob de estar en estado i en tiempo t
    gamma = [[sum(xi[t][i]) for i in range(n_estados)] for t in range(T-1)]
    gamma.append([alpha[T-1][i] * beta[T-1][i] / P_obs for i in range(n_estados)])

    # --- PASO M: Actualizar parámetros para maximizar probabilidad ---
    # Actualizar Pi
    pi = [gamma[0][i] for i in range(n_estados)]
    
    # Actualizar Transiciones A
    for i in range(n_estados):
        denom = sum(gamma[t][i] for t in range(T-1))
        for j in range(n_estados):
            A[i][j] = sum(xi[t][i][j] for t in range(T-1)) / denom
            
    # Actualizar Emisiones B
    for i in range(n_estados):
        denom = sum(gamma[t][i] for t in range(T))
        for k in range(n_simbolos):
            B[i][k] = sum(gamma[t][i] for t in range(T) if observaciones[t] == k) / denom

    print(f"Iteración {iteracion+1} completada...")

# ==============================================================
# 5. RESULTADOS
# ==============================================================
print("-" * 50)
print("MATRIZ DE TRANSICIÓN APRENDIDA (A):")
for fila in A: print([round(x, 4) for x in fila])
print("\nMATRIZ DE EMISIÓN APRENDIDA (B):")
for fila in B: print([round(x, 4) for x in fila])
