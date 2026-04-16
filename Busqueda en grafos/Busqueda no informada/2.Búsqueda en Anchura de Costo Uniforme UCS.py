# Representación del árbol con costos (distancias o pesos)
arbol_pesos = {
    'A': [('B', 5), ('C', 1)],
    'B': [('D', 2)],
    'C': [('E', 8), ('F', 3)],
    'D': [('G', 1), ('H', 4)],
    'E': [('I', 2), ('J', 1)],
    'F': [('K', 6), ('L', 2)],
    'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': []
}

def busqueda_costo_uniforme_nativa(grafo, origen, meta):
    # Usamos una lista normal. El formato es (costo, nodo, camino)
    cola = [(0, origen, [origen])]
    
    # Registro de nodos visitados
    visitados = set()

    while cola:
        # Ordenamos la lista basándonos en el costo acumulado.
        # 'lambda x: x[0]' le dice a Python que se fije en el primer elemento de la tupla (el costo)
        cola.sort(key=lambda x: x[0])
        
        # Como ya la ordenamos, el más barato seguro está en la posición 0. Lo sacamos.
        costo_actual, V, camino = cola.pop(0)
        
        print(f"Revisando nodo: {V} (Costo acumulado: {costo_actual})")

        # Si llegamos a la meta, devolvemos el éxito y el camino
        if V == meta:
            print(f"\n¡Éxito! Nodo Meta '{meta}' encontrado.")
            print(f"Camino óptimo: {camino}")
            print(f"Costo total: {costo_actual}")
            return True

        # Si el nodo no ha sido visitado, lo exploramos
        if V not in visitados:
            visitados.add(V)
            
            # Obtenemos sus hijos
            hijos = grafo.get(V, [])
            for hijo, costo_paso in hijos:
                if hijo not in visitados:
                    # Calculamos el costo total hasta este hijo
                    nuevo_costo = costo_actual + costo_paso
                    
                    # Creamos la nueva ruta añadiendo al hijo
                    # Nota: hacemos camino + [hijo] para crear una lista nueva sin modificar la original
                    nuevo_camino = camino + [hijo]
                    
                    # Lo metemos a la lista normal (al final)
                    # En la siguiente vuelta del 'while', el sort() lo acomodará en su lugar correcto
                    cola.append((nuevo_costo, hijo, nuevo_camino))
                    
    print(f"\nEl nodo Meta '{meta}' no se encuentra en el árbol.")
    return False

# --- PRUEBA DEL CÓDIGO ---
print("Iniciando Búsqueda de Costo Uniforme con Python puro...")
busqueda_costo_uniforme_nativa(arbol_pesos, origen='A', meta='L')
