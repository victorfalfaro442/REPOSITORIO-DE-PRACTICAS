# Nuestro grafo con conexiones de doble sentido (contiene ciclos)
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

def busqueda_en_grafos(grafo, origen, meta):
    print(f"--- Iniciando Búsqueda en Grafos (Origen: {origen}, Meta: {meta}) ---")
    
    # 1. Cola para guardar el estado (nodo_actual, camino_recorrido)
    cola = [(origen, [origen])]
    
    # 2. El conjunto de memoria
    visitados = set()

    while cola:
        nodo_actual, camino = cola.pop(0)

        # Si llegamos a la meta, terminamos
        if nodo_actual == meta:
            print(f"\n¡ÉXITO! Meta '{meta}' encontrada.")
            print(f"Camino final: {camino}")
            return True

        # ¿Ya estuve aquí?
        if nodo_actual not in visitados:
            # Lo marcamos como visitado (lo anotamos en la memoria)
            visitados.add(nodo_actual)
            print(f"\n[+] Explorando nodo nuevo: {nodo_actual}")
            
            # Revisamos a sus vecinos
            vecinos = grafo.get(nodo_actual, [])
            for vecino in vecinos:
                # Si el vecino ya está en nuestra memoria, lo ignoramos para evitar ciclos
                if vecino in visitados:
                    print(f"    -> Ignorando '{vecino}' (Ya está en la memoria/visitados)")
                else:
                    # Si es nuevo, lo agregamos a la cola para explorarlo después
                    print(f"    -> Agregando '{vecino}' a la cola")
                    cola.append((vecino, camino + [vecino]))
                    
    print(f"\nLa meta '{meta}' no se pudo alcanzar.")
    return False

# --- PRUEBA DEL CÓDIGO ---
# Vamos a buscar un nodo cercano, por ejemplo 'I', para no saturar la pantalla, 
# pero lo suficiente para ver cómo evita regresar a 'A' o a 'B'.
busqueda_en_grafos(grafo_bidireccional, origen='A', meta='I')
