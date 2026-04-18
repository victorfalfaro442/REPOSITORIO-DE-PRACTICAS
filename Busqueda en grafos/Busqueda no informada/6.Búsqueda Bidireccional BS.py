# Nuestro grafo profundo transformado a NO DIRIGIDO (Doble sentido)
grafo_bidireccional = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B', 'G', 'H'],
    'E': ['B', 'I'],
    'F': ['C', 'J', 'K'],
    'G': ['D', 'L'],
    'H': ['D'],
    'I': ['E', 'M', 'N'],
    'J': ['F'],
    'K': ['F', 'O'],
    'L': ['G', 'P'],
    'M': ['I'],
    'N': ['I', 'Q'],
    'O': ['K'],
    'P': ['L'],
    'Q': ['N', 'R'],
    'R': ['Q']
}

def busqueda_bidireccional_nativa(grafo, origen, meta):
    # Colas de búsqueda
    cola_frente = [origen]
    cola_atras = [meta]
    
    # Registramos de dónde venimos para poder dibujar la ruta final
    padres_frente = {origen: None}
    padres_atras = {meta: None}

    print(f"Iniciando Búsqueda Bidireccional de '{origen}' a '{meta}'...")

    while cola_frente and cola_atras:
        
        # --- 1. PASO HACIA ADELANTE ---
        actual_frente = cola_frente.pop(0)
        print(f"[Frente] Revisando: {actual_frente}")
        
        # Comprobamos intersección
        if actual_frente in padres_atras:
            print(f"\n¡INTERSECCIÓN ENCONTRADA EN EL NODO '{actual_frente}'!")
            return construir_camino(actual_frente, padres_frente, padres_atras)
            
        # Expandimos hacia adelante
        for vecino in grafo.get(actual_frente, []):
            if vecino not in padres_frente:
                padres_frente[vecino] = actual_frente
                cola_frente.append(vecino)

        # --- 2. PASO HACIA ATRÁS ---
        actual_atras = cola_atras.pop(0)
        print(f"[Atrás ] Revisando: {actual_atras}")
        
        # Comprobamos intersección
        if actual_atras in padres_frente:
            print(f"\n¡INTERSECCIÓN ENCONTRADA EN EL NODO '{actual_atras}'!")
            return construir_camino(actual_atras, padres_frente, padres_atras)
            
        # Expandimos hacia atrás
        for vecino in grafo.get(actual_atras, []):
            if vecino not in padres_atras:
                padres_atras[vecino] = actual_atras
                cola_atras.append(vecino)

    print("\nNo se encontró ningún camino.")
    return False

# --- FUNCIÓN AUXILIAR PARA UNIR LOS TÚNELES ---
def construir_camino(nodo_interseccion, padres_frente, padres_atras):
    # 1. Construimos desde el origen hasta la intersección
    camino_frente = []
    nodo_actual = nodo_interseccion
    while nodo_actual is not None:
        camino_frente.append(nodo_actual)
        nodo_actual = padres_frente[nodo_actual]
    camino_frente.reverse() # Lo volteamos porque lo armamos de atrás para adelante

    # 2. Construimos desde la intersección hasta la meta
    camino_atras = []
    nodo_actual = padres_atras[nodo_interseccion] # Empezamos un nodo después para no duplicar la intersección
    while nodo_actual is not None:
        camino_atras.append(nodo_actual)
        nodo_actual = padres_atras[nodo_actual]
        
    # Unimos ambos caminos
    camino_total = camino_frente + camino_atras
    
    print(f"Camino Final: {camino_total}")
    return camino_total

# --- PRUEBA DEL CÓDIGO ---
# Vamos a buscar el camino desde 'A' hasta 'Q' (que está lejos, en el nivel 5)
busqueda_bidireccional_nativa(grafo_bidireccional, origen='A', meta='Q')
