# Representación del árbol (el mismo de tu diagrama original)
arbol = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E', 'F'],
    'D': ['G', 'H'],
    'E': ['I', 'J'],
    'F': ['K', 'L'],
    'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': []
}

def busqueda_profundidad_dfs_nativa(grafo, origen, meta):
    # 1. Creamos una Pila usando una lista normal de Python. 
    # Guardamos una tupla con (nodo_actual, camino_recorrido)
    pila = [(origen, [origen])]
    
    # Registro de nodos visitados
    visitados = set()

    while pila:
        # a) Sacamos el nodo de HASTA ARRIBA de la pila (LIFO) usando pop() sin índice
        nodo_actual, camino = pila.pop()
        
        print(f"Revisando nodo: {nodo_actual}")

        # b) Si es la meta, terminamos
        if nodo_actual == meta:
            print(f"\n¡Éxito! Nodo Meta '{meta}' encontrado.")
            print(f"Camino recorrido: {camino}")
            return True

        # c) Si no ha sido visitado, lo marcamos
        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            
            # Obtenemos sus hijos
            hijos = grafo.get(nodo_actual, [])
            
            # Volteamos la lista de hijos antes de meterlos a la pila.
            for hijo in reversed(hijos):
                if hijo not in visitados:
                    # Agregamos a la pila (encima de todo lo demás)
                    pila.append((hijo, camino + [hijo]))
                    
    print(f"\nEl nodo Meta '{meta}' no se encuentra en el árbol.")
    return False

# --- PRUEBA DEL CÓDIGO ---
# Vamos a buscar el nodo 'J' empezando desde la raíz 'A'
print("Iniciando Búsqueda en Profundidad (DFS) con Python puro...")
busqueda_profundidad_dfs_nativa(arbol, origen='A', meta='J')
