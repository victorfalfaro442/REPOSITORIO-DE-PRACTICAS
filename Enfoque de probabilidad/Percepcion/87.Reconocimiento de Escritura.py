import math

print("--- RECONOCIMIENTO DE ESCRITURA: K-VECINOS MÁS CERCANOS (K-NN) ---")

# ==============================================================
# 1. LA BASE DE DATOS DE ENTRENAMIENTO (Nuestra "Biblioteca")
# ==============================================================
# Cada número es una imagen de 5x5 aplanada en una lista de 25 valores.

# Formas de escribir un "0"
cero_redondo = [
    0,1,1,1,0,
    1,0,0,0,1,
    1,0,0,0,1,
    1,0,0,0,1,
    0,1,1,1,0
]
cero_delgado = [
    0,0,1,0,0,
    0,1,0,1,0,
    1,0,0,0,1,
    0,1,0,1,0,
    0,0,1,0,0
]

# Formas de escribir un "1"
uno_con_base = [
    0,0,1,0,0,
    0,1,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,1,1,1,0
]
uno_simple = [
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0
]

# Unimos todo en nuestro dataset (X = los datos, Y = las etiquetas/respuestas)
dataset_imagenes = [cero_redondo, cero_delgado, uno_con_base, uno_simple]
etiquetas = ["Cero (0)", "Cero (0)", "Uno (1)", "Uno (1)"]

# ==============================================================
# 2. EL ALGORITMO K-NN (Matemática Pura)
# ==============================================================
def distancia_euclidiana(img1, img2):
    """Calcula qué tan diferentes son dos imágenes en el hiperespacio."""
    suma_cuadrados = sum((p1 - p2)**2 for p1, p2 in zip(img1, img2))
    return math.sqrt(suma_cuadrados)

def clasificar_numero(imagen_nueva, k=3):
    """Encuentra las 'k' imágenes más parecidas y vota para decidir qué número es."""
    distancias = []
    
    # 1. Comparar el garabato con TODAS las imágenes de la biblioteca
    for i in range(len(dataset_imagenes)):
        dist = distancia_euclidiana(imagen_nueva, dataset_imagenes[i])
        distancias.append((dist, etiquetas[i]))
        
    # 2. Ordenar las distancias de menor a mayor (los más parecidos primero)
    distancias.sort(key=lambda x: x[0])
    
    # 3. Tomar los "k" vecinos más cercanos
    vecinos_cercanos = distancias[:k]
    
    # 4. Votación Democrática
    votos = {}
    for dist, etiqueta in vecinos_cercanos:
        votos[etiqueta] = votos.get(etiqueta, 0) + 1
        
    # Gana el que tenga más votos
    prediccion_final = max(votos, key=votos.get)
    return prediccion_final, distancias

# ==============================================================
# 3. PRUEBA: ESCRIBIENDO UN NÚMERO DESCONOCIDO Y DEFORME
# ==============================================================
# Imagina que alguien dibujó esto rápido y le salió torcido y con ruido
numero_misterioso = [
    0,0,0,1,0,
    0,0,1,1,0,
    0,0,0,1,0,
    0,0,1,0,0,
    0,1,1,0,0
]

def dibujar_consola(imagen):
    """Función de ayuda para ver el número en la terminal"""
    for i in range(0, 25, 5):
        fila = ["██" if pixel == 1 else ".." for pixel in imagen[i:i+5]]
        print("".join(fila))

print("\n[*] Este es el número misterioso que la IA debe reconocer:")
dibujar_consola(numero_misterioso)

print("\n[*] Analizando en un espacio de 25 dimensiones...")

# Elegimos k=1 (Solo buscará el vecino absoluto más cercano en este caso)
prediccion, detalles = clasificar_numero(numero_misterioso, k=1)

print(f"\n[!] RESULTADO DE LA IA: ¡Estoy casi segura de que es un {prediccion}!")
print("-" * 50)
print(f"Distancia matemática al 'Uno con base': {detalles[0][0]:.2f}")
print(f"Distancia matemática al 'Cero delgado': {detalles[2][0]:.2f}")
