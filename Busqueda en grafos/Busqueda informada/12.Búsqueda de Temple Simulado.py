# Nuestro grafo 

grafo_tabu = {
    'Inicio': ['A', 'B'],
    'A': ['Inicio', 'C', 'D'],
    'B': ['Inicio', 'E', 'G'], 
    'C': ['A'],
    'D': ['A', 'F'],      # 'D' es el máximo local. Su única salida nueva es 'F'
    'F': ['D', 'G'],
    'G': ['F', 'B'],      
    'E': ['B', 'Z'],
    'Z': ['E']            # META
}

# Distancia estimada a la meta (Queremos llegar a 0)
heuristica = {
    'Inicio': 10,
    'A': 7,
    'B': 9,    # 'B' se ve muy mal al principio
    'C': 8,
    'D': 4,    # El Máximo Local (Trampa)
    'F': 5,    # Peor que D
    'G': 6,    # Peor que F
    'E': 3,
    'Z': 0     # El Máximo Global (Meta)
}

def busqueda_tabu(grafo, h, origen, meta, tamano_memoria=2, max_iteraciones=15):
    print(f"--- Iniciando Búsqueda Tabú (Origen: '{origen}', Meta: '{meta}') ---")
    print(f"Tamaño de la lista Tabú: {tamano_memoria}\n")
    
    nodo_actual = origen
    camino = [nodo_actual]
    lista_tabu = []  # Nuestra memoria a corto plazo
    
    for iteracion in range(max_iteraciones):
        valor_actual = h[nodo_actual]
        print(f"[Iteración {iteracion+1}] Nodo actual: {nodo_actual} (Valor: {valor_actual})")
        print(f"  Memoria Tabú actual: {lista_tabu}")
        
        # 1. Condición de éxito
        if nodo_actual == meta:
            print(f"\n¡ÉXITO! Meta '{meta}' encontrada esquivando los máximos locales.")
            print(f"Camino final: {camino}")
            return True
            
        # 2. Obtener vecinos disponibles
        vecinos = grafo.get(nodo_actual, [])
        if not vecinos:
            print("Callejón sin salida absoluto.")
            return False
            
        # 3. Buscar el mejor vecino QUE NO SEA TABÚ
        mejor_vecino = None
        mejor_valor = float('inf') # Buscamos el valor más bajo (cercano a 0)
        
        for vecino in vecinos:
            # Regla de oro: Ignorar a los vecinos en la lista Tabú
            if vecino in lista_tabu:
                print(f"    -> Vecino '{vecino}' es TABÚ (Ignorado)")
                continue
                
            valor_vecino = h.get(vecino, float('inf'))
            print(f"    -> Evaluando vecino '{vecino}' (Valor: {valor_vecino})")
            
            if valor_vecino < mejor_valor:
                mejor_valor = valor_vecino
                mejor_vecino = vecino
                
        # 4. ¿Qué pasa si todos los vecinos son Tabú?
        if mejor_vecino is None:
            print("\nTodos los caminos posibles están bloqueados por la memoria Tabú. Fin de la búsqueda.")
            return False
            
        # 5. NOS MOVEMOS (Incluso si el mejor vecino es PEOR que mi nodo actual)
        if mejor_valor > valor_actual:
            print(f"  [*] ¡Tomando una mala decisión estratégica! Empeorando de {valor_actual} a {mejor_valor} para escapar.")
            
        # Actualizamos la memoria Tabú añadiendo EL NODO QUE ACABAMOS DE DEJAR
        lista_tabu.append(nodo_actual)
        if len(lista_tabu) > tamano_memoria:
            lista_tabu.pop(0) # Olvidamos el recuerdo más antiguo
            
        # Damos el paso
        nodo_actual = mejor_vecino
        camino.append(nodo_actual)
        print("-" * 40)
        
    print(f"\nSe alcanzó el límite de iteraciones ({max_iteraciones}) sin encontrar la meta.")
    return False

# --- PRUEBA DEL CÓDIGO ---
busqueda_tabu(grafo_tabu, heuristica, origen='Inicio', meta='Z', tamano_memoria=2)
