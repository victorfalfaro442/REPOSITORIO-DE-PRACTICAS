import random

print("--- FILTRADO DE PARTÍCULAS (PYTHON NATIVO) ---")

# ==============================================================
# 1. EL MUNDO
# ==============================================================
pasillo_longitud = 100
puertas = [20, 50, 80] # Posición de las puertas en metros

# ==============================================================
# 2. CONFIGURACIÓN DEL FILTRO
# ==============================================================
num_particulas = 500
# Creamos 500 hipótesis al azar por todo el pasillo
particulas = [random.uniform(0, pasillo_longitud) for _ in range(num_particulas)]

def mover_particulas(lista, movimiento):
    """Predicción: Movemos cada partícula y añadimos un poco de ruido (incertidumbre)."""
    return [(p + movimiento + random.gauss(0, 1)) % pasillo_longitud for p in lista]

def calcular_pesos(lista, sensor_ve_puerta):
    """Pesado: ¿Qué partícula tiene sentido según lo que el robot ve"""
    pesos = []
    for p in lista:
        # Distancia a la puerta más cercana
        distancia_puerta = min(abs(p - d) for d in puertas)
        
        if sensor_ve_puerta:
            # Si el sensor ve puerta, las partículas cerca de puertas pesan más
            peso = 1.0 if distancia_puerta < 2 else 0.1
        else:
            # Si ve pared, las partículas lejos de puertas pesan más
            peso = 0.1 if distancia_puerta < 2 else 1.0
        pesos.append(peso)
    return pesos

def resamplear(lista, pesos):
    """Selección: Creamos una nueva generación basada en los pesos."""
    nueva_gen = random.choices(lista, weights=pesos, k=num_particulas)
    return nueva_gen

# ==============================================================
# 3. SIMULACIÓN
# ==============================================================
# El robot se mueve 10 metros y dice que "Ve una Puerta"
movimiento_real = 10
sensor_dice_puerta = True

print(f"[*] El robot se mueve {movimiento_real}m y detecta: {'PUERTA' if sensor_dice_puerta else 'PARED'}")

# Paso 1: Mover (Predicción)
particulas = mover_particulas(particulas, movimiento_real)

# Paso 2: Pesar (Evidencia)
pesos = calcular_pesos(particulas, sensor_dice_puerta)

# Paso 3: Resamplear (Evolución)
particulas = resamplear(particulas, pesos)

# ==============================================================
# 4. RESULTADO
# ==============================================================
estimacion_posicion = sum(particulas) / num_particulas
print("-" * 50)
print(f"Posición estimada del robot: {estimacion_posicion:.2f} metros")
print(f"Incertidumbre (Desviación): {abs(max(particulas) - min(particulas)):.2f}")