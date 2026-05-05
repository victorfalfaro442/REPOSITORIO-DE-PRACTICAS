import math

print("--- SVM CON TRUCO DEL NÚCLEO (RBF KERNEL) ---")

# ==============================================================
# 1. DATOS (No lineales: Círculo dentro de otro)
# ==============================================================
# [x, y], Etiqueta (1 o -1)
datos = [
    ([0, 0], 1), ([1, 1], 1), ([1, -1], 1), ([-1, 1], 1), # Centro (Clase 1)
    ([4, 4], -1), ([4, -4], -1), ([-4, 4], -1), ([-4, -4], -1) # Periferia (Clase -1)
]

# ==============================================================
# 2. EL KERNEL RBF (La lente mágica)
# ==============================================================
def kernel_rbf(x1, x2, gamma=0.1):
    """Calcula la similitud entre dos puntos en una dimensión superior."""
    dist_sq = sum((a - b) ** 2 for a, b in zip(x1, x2))
    return math.exp(-gamma * dist_sq)

# ==============================================================
# 3. PREDICCIÓN (Simplificación del modelo entrenado)
# ==============================================================
# En una SVM real, el entrenamiento nos daría 'alphas' (pesos) 
# para cada vector de soporte. Aquí simularemos esos pesos.
vectores_soporte = datos 
alphas = [1.0] * len(datos) # Pesos de los vectores
sesgo = -0.5 # El 'bias' que ajusta la carretera

def predecir(punto_nuevo):
    f_x = 0
    for i in range(len(vectores_soporte)):
        punto_sv, etiqueta = vectores_soporte[i]
        # La decisión es una suma ponderada de similitudes
        f_x += alphas[i] * etiqueta * kernel_rbf(punto_nuevo, punto_sv)
    
    return 1 if (f_x + sesgo) >= 0 else -1

# ==============================================================
# 4. PRUEBA
# ==============================================================
puntos_prueba = [[0.5, 0.5], [5, 5]]

for p in puntos_prueba:
    resultado = predecir(p)
    clase = "CENTRO" if resultado == 1 else "PERIFERIA"
    print(f"[*] Punto {p}: Clasificado como -> {clase}")
