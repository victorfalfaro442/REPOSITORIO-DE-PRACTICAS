import math

print("--- ALGORITMO k-NEAREST NEIGHBORS (k-NN) ---")

# ==============================================================
# 1. DATOS DE ENTRENAMIENTO (Etiquetados)
# ==============================================================
# [Peso en gramos, Textura (1-10)], Clase
datos_conocidos = [
    ([150, 7], "Naranja"),
    ([160, 8], "Naranja"),
    ([170, 9], "Naranja"),
    ([140, 7], "Naranja"),
    ([250, 4], "Toronja"),
    ([260, 5], "Toronja"),
    ([240, 3], "Toronja"),
    ([270, 4], "Toronja")
]

# ==============================================================
# 2. LÓGICA DEL ALGORITMO
# ==============================================================
def distancia_euclidiana(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def clasificar_knn(punto_nuevo, k=3):
    distancias = []
    
    # A. Calcular distancia a todos los puntos conocidos
    for caracteristicas, etiqueta in datos_conocidos:
        d = distancia_euclidiana(punto_nuevo, caracteristicas)
        distancias.append((d, etiqueta))
    
    # B. Ordenar por distancia (los más cercanos primero)
    distancias.sort(key=lambda x: x[0])
    
    # C. Tomar los k vecinos más cercanos
    vecinos = distancias[:k]
    
    # D. Votación de etiquetas
    votos = {}
    for _, etiqueta in vecinos:
        votos[etiqueta] = votos.get(etiqueta, 0) + 1
    
    # El que tenga más votos gana
    ganador = max(votos, key=votos.get)
    return ganador, vecinos

# ==============================================================
# 3. PREDICCIÓN
# ==============================================================
fruta_misteriosa = [230, 5] # Pesada y textura media-baja
K_VALOR = 3

resultado, mis_vecinos = clasificar_knn(fruta_misteriosa, k=K_VALOR)

print(f"[*] Analizando fruta: Peso={fruta_misteriosa[0]}g, Textura={fruta_misteriosa[1]}/10")
print(f"[*] Usando K = {K_VALOR}")
print("-" * 50)
print(f"Los {K_VALOR} vecinos más cercanos fueron:")
for d, etiqueta in mis_vecinos:
    print(f"  - A {d:.2f} unidades de distancia: {etiqueta}")

print("-" * 50)
print(f"🤖 DECISIÓN: La fruta es una -> {resultado.upper()}")
