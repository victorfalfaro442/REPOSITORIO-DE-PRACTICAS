import random

# 1. Definimos nuestra meta y el "ADN" disponible
META = "DESTINO"
GENES_DISPONIBLES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TAMANO_POBLACION = 100

def generar_gen():
    """Devuelve una letra al azar."""
    return random.choice(GENES_DISPONIBLES)

def generar_individuo():
    """Crea una palabra al azar de la misma longitud que la meta."""
    return [generar_gen() for _ in range(len(META))]

def calcular_aptitud(individuo):
    """
    Función de Fitness: Cuenta cuántas letras están en la posición correcta.
    Si la meta es "DESTINO" (7 letras) y el individuo es "DXXTXXO", su aptitud es 3.
    """
    aptitud = 0
    for i in range(len(META)):
        if individuo[i] == META[i]:
            aptitud += 1
    return aptitud

def cruzar(padre1, padre2):
    """Toma la mitad izquierda del padre1 y la mitad derecha del padre2."""
    punto_corte = random.randint(1, len(META) - 1)
    hijo = padre1[:punto_corte] + padre2[punto_corte:]
    return hijo

def mutar(individuo, tasa_mutacion=0.1):
    """Cambia letras al azar para mantener la diversidad genética."""
    for i in range(len(individuo)):
        # Si el dado cae dentro del porcentaje de mutación, cambiamos la letra
        if random.random() < tasa_mutacion:
            individuo[i] = generar_gen()
    return individuo

def algoritmo_genetico():
    print(f"--- Iniciando Evolución Genética (Meta: '{META}') ---")
    
    # Generación 0: Creamos la población inicial al azar
    poblacion = [generar_individuo() for _ in range(TAMANO_POBLACION)]
    generacion = 1
    
    while True:
        # Evaluamos a toda la población actual
        # Creamos tuplas de (aptitud, individuo) para poder ordenarlos
        poblacion_evaluada = [(calcular_aptitud(ind), ind) for ind in poblacion]
        
        # Ordenamos de mayor a menor aptitud (los mejores arriba)
        poblacion_evaluada.sort(key=lambda x: x[0], reverse=True)
        
        # Obtenemos al campeón de esta generación
        mejor_aptitud, mejor_individuo = poblacion_evaluada[0]
        mejor_palabra = "".join(mejor_individuo)
        
        print(f"Generación {generacion} | Mejor: {mejor_palabra} | Aptitud: {mejor_aptitud}/{len(META)}")
        
        # Condicion de éxito
        if mejor_aptitud == len(META):
            print(f"\n¡ÉXITO ROTUNDO! La evolución ha alcanzado su destino en la generación {generacion}.")
            break
            
        # --- CREACIÓN DE LA NUEVA GENERACIÓN ---
        nueva_poblacion = []
        
        # Elitismo: Pasamos a los mejores individuos directamente para no perder avance
        elite = [ind for aptitud, ind in poblacion_evaluada[:10]]
        nueva_poblacion.extend(elite)
        
        # Selección y Reproducción para rellenar el resto de la población
        while len(nueva_poblacion) < TAMANO_POBLACION:
            # Seleccionamos padres al azar de entre la mitad superior (los más aptos)
            padre1 = random.choice(poblacion_evaluada[:50])[1]
            padre2 = random.choice(poblacion_evaluada[:50])[1]
            
            # Cruzamos y mutamos
            hijo = cruzar(padre1, padre2)
            hijo = mutar(hijo)
            
            nueva_poblacion.append(hijo)
            
        # Reemplazamos la población antigua con la nueva
        poblacion = nueva_poblacion
        generacion += 1

# --- PRUEBA DEL CÓDIGO ---
algoritmo_genetico()
