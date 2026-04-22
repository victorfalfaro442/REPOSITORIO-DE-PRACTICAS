# Nuestro grafo de prueba
grafo_colinas = {
    'Inicio': ['A', 'B'],
    'A': ['C', 'D'],      # 'A' lleva a una colina falsa
    'B': ['E'],           # 'B' lleva al camino correcto, pero parece peor al principio
    'C': [], 
    'D': ['F'],           # 'D' es la cima de la colina falsa
    'E': ['Z'],           
    'F': [],
    'Z': []               # La verdadera meta
}

# La heurística: Distancia a la meta (Queremos el valor MÁS BAJO)
heuristica = {
    'Inicio': 10,
    'A': 7,    
    'B': 9,    
    'C': 8,
    'D': 4,    # El Máximo Local (Ningún vecino es mejor que 4)
    'F': 5,
    'E': 3,
    'Z': 0  
}

def ascension_de_colinas(grafo, h, nodo_actual):
    print(f"--- Iniciando Ascensión de Colinas desde '{nodo_actual}' ---")
    
    camino = [nodo_actual]

    while True:
        valor_actual = h[nodo_actual]
        print(f"\nUbicación actual: {nodo_actual} (Valor: {valor_actual})")
        
        # Si llegamos a la meta perfecta, ganamos
        if valor_actual == 0:
            print("¡ÉXITO! Hemos alcanzado el Máximo Global (La meta).")
            print(f"Camino recorrido: {camino}")
            return True

        vecinos = grafo.get(nodo_actual, [])
        
        # Si no hay a dónde ir, estamos en un callejón sin salida
        if not vecinos:
            print("Nos quedamos sin camino. ¡Atrapados en un Máximo Local!")
            return False

        # Buscamos al MEJOR vecino
        mejor_vecino = None
        mejor_valor = float('inf') # Como buscamos el 0, infinito es el peor valor posible
        
        for vecino in vecinos:
            valor_vecino = h.get(vecino, float('inf'))
            print(f"  -> Mirando vecino '{vecino}' con valor {valor_vecino}")
            
            if valor_vecino < mejor_valor:
                mejor_valor = valor_vecino
                mejor_vecino = vecino

        # Si el mejor vecino es PEOR o IGUAL a donde estoy, me detengo.
        if mejor_valor >= valor_actual:
            print(f"\n¡ALTO! El mejor vecino ('{mejor_vecino}' con {mejor_valor}) no es mejor que mi posición actual ({valor_actual}).")
            print("El algoritmo se detiene asumiendo que llegó a la cima.")
            print(f"Camino final: {camino} (Atrapado en un Máximo Local)")
            return False
            
        # Si el vecino es mejor, damos el paso
        print(f"Tomando el paso hacia '{mejor_vecino}'...")
        nodo_actual = mejor_vecino
        camino.append(nodo_actual)

# --- PRUEBA DEL CÓDIGO ---
ascension_de_colinas(grafo_colinas, heuristica, 'Inicio')
