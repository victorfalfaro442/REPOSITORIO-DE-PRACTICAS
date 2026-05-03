import math

print("--- ALGORITMO ESPERANZA-MAXIMIZACIÓN (EM) ---")

# ==============================================================
# 1. LOS DATOS (Calificaciones mezcladas de dos grupos ocultos)
# ==============================================================
# A simple vista vemos notas bajas (10-15) y altas (80-90)
calificaciones = [9, 10, 11, 12, 11, 13, 28, 30, 32, 29, 31, 35, 19, 21]

# ==============================================================
# 2. FUNCIÓN DE APOYO (La Campana de Gauss)
# ==============================================================
def prob_gaussiana(x, media, varianza):
    """Calcula la probabilidad de un punto x en una campana de Gauss."""
    # Evitar divisiones por cero si la varianza es muy pequeña
    varianza = max(varianza, 0.0001) 
    coeficiente = 1.0 / math.sqrt(2 * math.pi * varianza)
    exponente = math.exp(-((x - media) ** 2) / (2 * varianza))
    return coeficiente * exponente

# ==============================================================
# 3. INICIALIZACIÓN "CIEGA" (El huevo de partida)
# ==============================================================
# La IA inventa promedios terribles a propósito para empezar
media_grupo_1 = 40.0
varianza_grupo_1 = 100.0
peso_grupo_1 = 0.5 # Creemos que el 50% de los alumnos son del grupo 1

media_grupo_2 = 60.0
varianza_grupo_2 = 100.0
peso_grupo_2 = 0.5

print(f"[*] Inicio Ciego -> Promedio G1: {media_grupo_1}, Promedio G2: {media_grupo_2}")
print("-" * 60)

# ==============================================================
# 4. EL BUCLE EM (Adivinar y Corregir)
# ==============================================================
iteraciones = 5

for paso in range(1, iteraciones + 1):
    
    # ---------------------------------------------------------
    # PASO E (Esperanza): ¿De quién es cada examen?
    # ---------------------------------------------------------
    responsabilidades_g1 = []
    responsabilidades_g2 = []
    
    for nota in calificaciones:
        # Probabilidad de que la nota venga del Grupo 1
        p1 = peso_grupo_1 * prob_gaussiana(nota, media_grupo_1, varianza_grupo_1)
        # Probabilidad de que la nota venga del Grupo 2
        p2 = peso_grupo_2 * prob_gaussiana(nota, media_grupo_2, varianza_grupo_2)
        
        suma_prob = p1 + p2
        
        # Fracción de responsabilidad (Normalizada a 1)
        resp_1 = p1 / suma_prob
        resp_2 = p2 / suma_prob
        
        responsabilidades_g1.append(resp_1)
        responsabilidades_g2.append(resp_2)

    # ---------------------------------------------------------
    # PASO M (Maximización): Recalcular la realidad
    # ---------------------------------------------------------
    # Suma total de las fracciones de alumnos en cada grupo
    total_resp_g1 = sum(responsabilidades_g1)
    total_resp_g2 = sum(responsabilidades_g2)
    
    # Actualizar Medias (Promedio ponderado)
    nueva_media_g1 = sum(resp * nota for resp, nota in zip(responsabilidades_g1, calificaciones)) / total_resp_g1
    nueva_media_g2 = sum(resp * nota for resp, nota in zip(responsabilidades_g2, calificaciones)) / total_resp_g2
    
    # Actualizar Varianzas (Dispersión ponderada)
    nueva_var_g1 = sum(resp * ((nota - nueva_media_g1) ** 2) for resp, nota in zip(responsabilidades_g1, calificaciones)) / total_resp_g1
    nueva_var_g2 = sum(resp * ((nota - nueva_media_g2) ** 2) for resp, nota in zip(responsabilidades_g2, calificaciones)) / total_resp_g2
    
    # Actualizar Pesos (Qué porcentaje de la clase total es cada grupo)
    n_total = len(calificaciones)
    peso_grupo_1 = total_resp_g1 / n_total
    peso_grupo_2 = total_resp_g2 / n_total
    
    # Aplicar los nuevos valores para el siguiente ciclo
    media_grupo_1, varianza_grupo_1 = nueva_media_g1, nueva_var_g1
    media_grupo_2, varianza_grupo_2 = nueva_media_g2, nueva_var_g2
    
    print(f"Iteración {paso}:")
    print(f"  -> Grupo 1: Promedio = {media_grupo_1:5.1f} | Varianza = {varianza_grupo_1:5.1f}")
    print(f"  -> Grupo 2: Promedio = {media_grupo_2:5.1f} | Varianza = {varianza_grupo_2:5.1f}")

print("-" * 60)
print("[*] ¡Convergencia alcanzada!")