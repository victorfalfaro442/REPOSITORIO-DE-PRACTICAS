import math
import random

print("--- ALGORITMO DE AGRUPAMIENTO NO SUPERVISADO (K-MEANS) ---")

# ==============================================================
# 1. LOS DATOS (Espacio 2D: [Edad, Gasto Mensual])
# ==============================================================
clientes = [
    # Parecen ser jóvenes que gastan mucho
    [25, 80], [22, 90], [28, 85], [24, 88], 
    # Parecen ser adultos mayores que gastan poco
    [65, 20], [60, 15], [70, 30], [68, 25],
    # Parecen ser de mediana edad con gasto moderado
    [40, 50], [45, 45], [38, 55], [42, 48]
]

K = 3 # Queremos encontrar 3 tribus/segmentos

# ==============================================================
# 2. FUNCIONES MATEMÁTICAS
# ==============================================================
def distancia_euclidiana(punto1, punto2):
    """Calcula la distancia en línea recta entre dos puntos 2D."""
    return math.sqrt((punto1[0] - punto2[0])**2 + (punto1[1] - punto2[1])**2)

def calcular_centro(puntos):
    """Calcula el promedio de [Edad, Gasto] para encontrar el nuevo centroide."""
    if not puntos:
        return [0, 0]
    promedio_x = sum(p[0] for p in puntos) / len(puntos)
    promedio_y = sum(p[1] for p in puntos) / len(puntos)
    return [promedio_x, promedio_y]

# ==============================================================
# 3. INICIALIZACIÓN (El punto de partida)
# ==============================================================
# Elegimos 3 clientes al azar para que sean los "Líderes" iniciales (Centroides)
random.seed(42) # Para que el resultado sea reproducible
centroides = random.sample(clientes, K)

print(f"[*] Centroides iniciales (Al azar):")
for i, c in enumerate(centroides):
    print(f"  Tribu {i+1}: Edad {c[0]}, Gasto ${c[1]}")
print("-" * 50)

# ==============================================================
# 4. EL BUCLE DE K-MEANS
# ==============================================================
iteraciones = 10
asignaciones_anteriores = []

for paso in range(1, iteraciones + 1):
    
    # Grupos vacíos para esta ronda
    grupos = [[] for _ in range(K)]
    asignaciones_actuales = []
    
    # --- FASE 1: ASIGNACIÓN ---
    for cliente in clientes:
        # Encontramos el centroide más cercano
        distancias = [distancia_euclidiana(cliente, c) for c in centroides]
        indice_ganador = distancias.index(min(distancias))
        
        grupos[indice_ganador].append(cliente)
        asignaciones_actuales.append(indice_ganador)
        
    # Condición de parada: Si nadie cambió de tribu, hemos terminado
    if asignaciones_actuales == asignaciones_anteriores:
        print(f"\n[*] ¡Convergencia perfecta alcanzada en la iteración {paso}!")
        break
        
    asignaciones_anteriores = asignaciones_actuales
    
    # --- FASE 2: ACTUALIZACIÓN ---
    # Movemos al líder (centroide) al centro exacto de su nueva tribu
    for i in range(K):
        centroides[i] = calcular_centro(grupos[i])

# ==============================================================
# 5. RESULTADOS FINALES (Los Perfiles Descubiertos)
# ==============================================================
print("\n" + "=" * 50)
print("PERFILES DE CLIENTES DESCUBIERTOS:")
print("=" * 50)

nombres_perfiles = ["Perfil A", "Perfil B", "Perfil C"]

for i in range(K):
    c_edad, c_gasto = centroides[i]
    cantidad = len(grupos[i])
    print(f"\n{nombres_perfiles[i]} (Centro exacto: Edad {c_edad:.1f}, Gasto ${c_gasto:.1f})")
    print(f"  -> Total de clientes en este segmento: {cantidad}")
    print(f"  -> Miembros: {grupos[i]}")