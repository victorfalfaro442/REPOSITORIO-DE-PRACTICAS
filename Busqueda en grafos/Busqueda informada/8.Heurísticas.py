# 1. Grafo a trabajar
grafo_complejo = {
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

# 2. La Heurística: Distancia estimada hacia 'Q'
heuristica_hacia_Q = {
    'Q': 0,   # meta
    'N': 1, 'R': 1, 
    'I': 2, 
    'E': 3, 'M': 3, 
    'B': 4, 
    'A': 5, 'D': 5, 
    'C': 6, 'G': 6, 'H': 6, 
    'F': 7, 'L': 7, 
    'J': 8, 'K': 8, 'P': 8, 
    'O': 9
}

def busqueda_heuristica_voraz(grafo, heuristica, origen, meta):
    print(f"--- Búsqueda Heurística Voraz (Origen: {origen}, Meta: {meta}) ---")
    
    # Cola: (valor_heuristico, nodo, camino_recorrido)
    cola = [(heuristica[origen], origen, [origen])]
    
    # Memoria para Búsqueda en Grafos 
    visitados = set()

    while cola:
        # Ordenamos la cola para que el nodo con la heurística más baja (más cercano) quede al frente
        cola.sort(key=lambda x: x[0])
        
        # Sacamos al mejor candidato actual
        h_actual, nodo_actual, camino = cola.pop(0)
        
        print(f"Revisando nodo: {nodo_actual} (Estimación a meta: {h_actual})")

        # Preguntar si llegamos a la meta
        if nodo_actual == meta:
            print(f"\n¡ÉXITO! Meta '{meta}' encontrada rápidamente.")
            print(f"Ruta óptima tomada: {camino}")
            return True

        # Si es un nodo nuevo, lo exploramos
        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            
            # Obtenemos sus vecinos
            vecinos = grafo.get(nodo_actual, [])
            for vecino in vecinos:
                if vecino not in visitados:
                    # Buscamos su heurística. Si un nodo no está en el diccionario, 
                    # le damos infinito para no ir hacia allá (float('inf')).
                    h_vecino = heuristica.get(vecino, float('inf'))
                    cola.append((h_vecino, vecino, camino + [vecino]))
                    
    print(f"\nLa meta '{meta}' no se pudo encontrar.")
    return False

# --- PRUEBA DEL CÓDIGO ---
busqueda_heuristica_voraz(grafo_complejo, heuristica_hacia_Q, origen='A', meta='Q')
