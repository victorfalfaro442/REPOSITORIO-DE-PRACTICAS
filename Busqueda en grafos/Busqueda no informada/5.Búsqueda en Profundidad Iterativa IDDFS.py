# Nuestro grafo ampliado
arbol_profundo = {
    'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F'],
    'D': ['G', 'H'], 'E': ['I'], 'F': ['J', 'K'],
    'G': ['L'], 'I': ['M', 'N'], 'K': ['O'],
    'L': ['P'], 'N': ['Q'], 'Q': ['R'],
    'H': [], 'J': [], 'M': [], 'O': [], 'P': [], 'R': []
}

# 1. La función de Búsqueda Limitada (El motor interno)
def busqueda_limitada(grafo, nodo_actual, meta, limite, camino_actual=[]):
    nuevo_camino = camino_actual + [nodo_actual]
    profundidad_actual = len(camino_actual)
    
    # Condición de éxito
    if nodo_actual == meta:
        return "ÉXITO", nuevo_camino

    # Condición de límite
    if profundidad_actual >= limite:
        if grafo.get(nodo_actual, []):
            return "CORTE", None 
        else:
            return "FALLO", None 

    # Exploración
    hijos = grafo.get(nodo_actual, [])
    hubo_corte_abajo = False
    
    for hijo in hijos:
        resultado, camino_final = busqueda_limitada(grafo, hijo, meta, limite, nuevo_camino)
        
        if resultado == "ÉXITO":
            return "ÉXITO", camino_final
        if resultado == "CORTE":
            hubo_corte_abajo = True 

    if hubo_corte_abajo:
        return "CORTE", None
    else:
        return "FALLO", None


# 2. La función Iterativa (El controlador)
def busqueda_profundidad_iterativa(grafo, origen, meta, limite_maximo=10):
    print(f"Iniciando Búsqueda en Profundidad Iterativa (Meta: '{meta}')")
    
    # El ciclo que aumenta el límite de 0 hasta el límite máximo
    for limite_actual in range(limite_maximo + 1):
        print(f"\n--- Iniciando iteración con Límite de Profundidad: {limite_actual} ---")
        
        # Llamamos a nuestro motor de búsqueda limitada
        resultado, camino = busqueda_limitada(grafo, origen, meta, limite_actual)
        
        if resultado == "ÉXITO":
            print(f">>> ¡ÉXITO! Meta '{meta}' encontrada en el nivel {limite_actual}.")
            print(f">>> Camino óptimo: {camino}")
            return True
            
        elif resultado == "FALLO":
            # Si una búsqueda con un límite devuelve FALLO puro (sin cortes),
            # significa que exploró TODO el árbol y la meta simplemente no existe.
            # No tiene sentido seguir iterando, así que detenemos todo.
            print(">>> FALLO. Se exploró todo el árbol accesible y no existe la meta.")
            return False
            
        # Si el resultado es "CORTE", el ciclo 'for' continuará normalmente 
        # hacia la siguiente iteración, aumentando el límite.
        else:
            print(">>> CORTE. No se encontró la meta, aumentando el límite para la siguiente iteración...")

    # Si se agota el límite máximo establecido
    print(f"\nSe alcanzó el límite máximo general ({limite_maximo}) sin encontrar la meta.")
    return False


# --- PRUEBA DEL CÓDIGO ---
# Vamos a buscar la meta 'Q' que está en el nivel 5.
busqueda_profundidad_iterativa(arbol_profundo, origen='A', meta='Q', limite_maximo=8)
