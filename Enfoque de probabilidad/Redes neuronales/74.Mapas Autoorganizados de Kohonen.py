import math
import random

print("--- MAPAS AUTOORGANIZADOS DE KOHONEN (SOM) ---")

# ==============================================================
# 1. PARÁMETROS Y DATOS
# ==============================================================
# Colores de entrenamiento: Rojo, Verde, Azul, Amarillo, Magenta, Cian
colores_entrenamiento = [
    [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], 
    [1.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0]
]

nombres_colores = ["Rojo", "Verde", "Azul", "Amarillo", "Magenta", "Cian"]

# Tamaño del mapa: Cuadrícula de 3x3 neuronas
filas, columnas = 3, 3
epocas = 1000
tasa_aprendizaje_inicial = 0.5

# Inicializamos el mapa con colores (pesos) aleatorios entre 0 y 1
mapa = []
for f in range(filas):
    fila_neuronas = []
    for c in range(columnas):
        pesos_rgb = [random.uniform(0, 1) for _ in range(3)]
        fila_neuronas.append(pesos_rgb)
    mapa.append(fila_neuronas)

# ==============================================================
# 2. FUNCIONES DE DISTANCIA
# ==============================================================
def distancia_euclidiana(v1, v2):
    return math.sqrt(sum((a - b)**2 for a, b in zip(v1, v2)))

def encontrar_bmu(vector_entrada):
    """Encuentra la neurona (fila, col) más parecida a la entrada."""
    distancia_minima = float('inf')
    bmu_idx = (0, 0)
    
    for f in range(filas):
        for c in range(columnas):
            dist = distancia_euclidiana(vector_entrada, mapa[f][c])
            if dist < distancia_minima:
                distancia_minima = dist
                bmu_idx = (f, c)
    return bmu_idx

# ==============================================================
# 3. ENTRENAMIENTO DEL MAPA
# ==============================================================
print("[*] Entrenando el mapa de Kohonen...")

for epoca in range(epocas):
    # Seleccionamos un color de entrenamiento al azar
    color_actual = random.choice(colores_entrenamiento)
    
    # 1. Encontrar la BMU (La ganadora)
    bmu_f, bmu_c = encontrar_bmu(color_actual)
    
    # Decaimiento del aprendizaje y del radio de vecindad
    tasa_aprendizaje = tasa_aprendizaje_inicial * math.exp(-epoca / epocas)
    radio_vecindad = max(1.0, (max(filas, columnas) / 2) * math.exp(-epoca / (epocas/2)))
    
    # 2. Actualizar la BMU y sus vecinas
    for f in range(filas):
        for c in range(columnas):
            # Distancia física en la cuadrícula 2D
            distancia_fisica = math.sqrt((f - bmu_f)**2 + (c - bmu_c)**2)
            
            if distancia_fisica <= radio_vecindad:
                # Factor de influencia (más fuerte cerca de la BMU)
                influencia = math.exp(-(distancia_fisica**2) / (2 * (radio_vecindad**2)))
                
                # Ajuste de pesos
                for i in range(3):
                    ajuste = tasa_aprendizaje * influencia * (color_actual[i] - mapa[f][c][i])
                    mapa[f][c][i] += ajuste

print("[*] ¡Entrenamiento completado!")
print("-" * 50)

# ==============================================================
# 4. CLASIFICACIÓN (MAPEO FINAL)
# ==============================================================
print("UBICACIÓN DE LOS COLORES EN EL MAPA 3x3:")
cuadricula_visual = [["Vacío" for _ in range(columnas)] for _ in range(filas)]

for i, color in enumerate(colores_entrenamiento):
    bmu_f, bmu_c = encontrar_bmu(color)
    cuadricula_visual[bmu_f][bmu_c] = nombres_colores[i]

for f in range(filas):
    fila_formateada = [f"{nodo:^10}" for nodo in cuadricula_visual[f]]
    print(f"| {fila_formateada[0]} | {fila_formateada[1]} | {fila_formateada[2]} |")
