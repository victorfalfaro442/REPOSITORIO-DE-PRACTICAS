# Representación del árbol (igual que antes)
arbol = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E', 'F'],
    'D': ['G', 'H'],
    'E': ['I', 'J'],
    'F': ['K', 'L'],
    'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': []
}

def busqueda_anchura_bfs_nativa(grafo, origen, meta):
    # 1. Creamos una Cola S usando una lista normal de Python
    S = []
    
    # Llevamos el registro de visitados
    visitados = set()
    
    # 2. Agregamos el origen a la Cola S
    S.append(origen)
    
    # 3. Bucle Mientras S no esté vacío:
    while S:  # Esto evalúa si la lista tiene elementos
        # a) Sacamos el nodo V encima de la cola S
        # Usamos pop(0) para sacar el elemento en la primera posición (el índice cero)
        V = S.pop(0)
        print(f"Revisando nodo: {V}")
        
        # b) Si V es el nodo Meta, devuelve solución. FIN
        if V == meta:
            print(f"\n¡Éxito! Nodo Meta '{meta}' encontrado.")
            return True
            
        # c) Si V no ha sido visitado, marcamos V como visitado
        if V not in visitados:
            visitados.add(V)
            
            # ii. Para cada hijo del nodo V, agrega el nodo hijo en la cola.
            hijos = grafo.get(V, [])
            for hijo in hijos:
                S.append(hijo)
                
    # Si terminamos de revisar todo y no encontramos la meta
    print(f"\nEl nodo Meta '{meta}' no se encuentra en el árbol.")
    return False

# --- PRUEBA DEL CÓDIGO ---
print("Iniciando BFS con Python puro...")
busqueda_anchura_bfs_nativa(arbol, origen='A', meta='J')
