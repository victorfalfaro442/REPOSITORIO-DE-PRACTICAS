# Nuestro grafo bidireccional
grafo_complejo = {
    'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F'],
    'D': ['B', 'G', 'H'], 'E': ['B', 'I'], 'F': ['C', 'J', 'K'],
    'G': ['D', 'L'], 'H': ['D'], 'I': ['E', 'M', 'N'],
    'J': ['F'], 'K': ['F', 'O'], 'L': ['G', 'P'],
    'M': ['I'], 'N': ['I', 'Q'], 'O': ['K'],
    'P': ['L'], 'Q': ['N', 'R'], 'R': ['Q']
}

# La Heurística: Distancia estimada hacia 'Q'
heuristica = {
    'Q': 0, 'N': 1, 'R': 1, 'I': 2, 'E': 3, 'M': 3, 
    'B': 4, 'A': 5, 'D': 5, 'C': 6, 'G': 6, 'H': 6, 
    'F': 7, 'L': 7, 'J': 8, 'K': 8, 'P': 8, 'O': 9
}

def busqueda_a_estrella(grafo, h, origen, meta):
    print(f"--- Iniciando Algoritmo A* (Origen: {origen}, Meta: {meta}) ---")
    
    # Cola: (f_n, g_n, nodo_actual, camino_recorrido)
    # Inicialmente: g(A) = 0, h(A) = 5 -> f(A) = 5
    g_origen = 0
    f_origen = g_origen + h[origen]
    cola = [(f_origen, g_origen, origen, [origen])]
    
    visitados = set()

    while cola:
        # Ordenamos por f(n), que es el primer elemento de la tupla
        cola.sort(key=lambda x: x[0])
        
        f_actual, g_actual, nodo_actual, camino = cola.pop(0)
        
        print(f"Evaluando: {nodo_actual} (Costo real g={g_actual}, Estimación h={h[nodo_actual]} -> f={f_actual})")

        if nodo_actual == meta:
            print(f"\n¡ÉXITO! Meta '{meta}' encontrada con la ruta más corta garantizada.")
            print(f"Ruta A*: {camino}")
            print(f"Costo total del viaje: {g_actual}")
            return True

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            
            for vecino in grafo.get(nodo_actual, []):
                if vecino not in visitados:
                    # El costo de dar un paso más siempre es 1 en este ejemplo
                    g_vecino = g_actual + 1
                    h_vecino = h.get(vecino, float('inf'))
                    f_vecino = g_vecino + h_vecino
                    
                    cola.append((f_vecino, g_vecino, vecino, camino + [vecino]))
                    
    return False

busqueda_a_estrella(grafo_complejo, heuristica, origen='A', meta='Q')
