# Grafo
grafo_complejo = {
    'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A', 'F'],
    'D': ['B', 'G', 'H'], 'E': ['B', 'I'], 'F': ['C', 'J', 'K'],
    'G': ['D', 'L'], 'H': ['D'], 'I': ['E', 'M', 'N'],
    'J': ['F'], 'K': ['F', 'O'], 'L': ['G', 'P'],
    'M': ['I'], 'N': ['I', 'Q'], 'O': ['K'],
    'P': ['L'], 'Q': ['N', 'R'], 'R': ['Q']
}

# Distancia estimada hacia 'Q'
heuristica = {
    'Q': 0, 'N': 1, 'R': 1, 'I': 2, 'E': 3, 'M': 3, 
    'B': 4, 'A': 5, 'D': 5, 'C': 6, 'G': 6, 'H': 6, 
    'F': 7, 'L': 7, 'J': 8, 'K': 8, 'P': 8, 'O': 9
}

def busqueda_voraz_primero_el_mejor(grafo, h, origen, meta):
    print(f"--- Búsqueda Voraz Primero el Mejor (Origen: {origen}, Meta: {meta}) ---")
    
    # La cola de prioridad manual. Guardamos: (f(n), nodo, camino)
    # Como es Voraz, f(n) es simplemente h(n)
    cola_prioridad = [(h[origen], origen, [origen])]
    
    visitados = set()

    while cola_prioridad:
        # Ordenamos para asegurar el comportamiento "Primero el Mejor"
        cola_prioridad.sort(key=lambda x: x[0])
        
        # Extraemos el nodo más prometedor 
        fn_actual, nodo_actual, camino = cola_prioridad.pop(0)
        
        print(f"Evaluando: {nodo_actual} (Valor f(n) = h(n) = {fn_actual})")

        if nodo_actual == meta:
            print(f"\n¡ÉXITO! Meta '{meta}' encontrada.")
            print(f"Ruta Voraz: {camino}")
            return True

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            
            vecinos = grafo.get(nodo_actual, [])
            for vecino in vecinos:
                if vecino not in visitados:
                    # Calculamos el valor f(n) para el vecino
                    fn_vecino = h.get(vecino, float('inf'))
                    cola_prioridad.append((fn_vecino, vecino, camino + [vecino]))
                    
    print(f"\nLa meta '{meta}' no es alcanzable.")
    return False

# --- PRUEBA DEL CÓDIGO ---
busqueda_voraz_primero_el_mejor(grafo_complejo, heuristica, origen='A', meta='Q')
