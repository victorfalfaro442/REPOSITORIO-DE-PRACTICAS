# Nuestro grafo con la trampa en 'D' (Máximo Local)
grafo_haz = {
    'Inicio': ['A', 'B'],
    'A': ['Inicio', 'C', 'D'],
    'B': ['Inicio', 'E', 'G'], 
    'C': ['A'],
    'D': ['A', 'F'],      
    'F': ['D', 'G'],
    'G': ['F', 'B'],      
    'E': ['B', 'Z'],
    'Z': []               # META
}

# Heurística (Queremos llegar a 0)
heuristica = {
    'Inicio': 10, 'A': 7, 'B': 9, 'C': 8, 
    'D': 4,       
    'F': 5, 'G': 6, 'E': 3, 'Z': 0
}

def busqueda_haz_local(grafo, h, nodos_iniciales, meta, k=2):
    print(f"--- Búsqueda de Haz Local (k={k} exploradores) ---")
    print(f"Meta a encontrar: '{meta}'\n")
    
    # El "haz" es nuestra lista de estados actuales
    haz = nodos_iniciales.copy()
    
    iteracion = 1
    while True:
        print(f"[Iteración {iteracion}] Posiciones de los {k} exploradores: {haz}")
        
        # 1. Verificar si alguien ya está en la meta
        if meta in haz:
            print(f"\n¡ÉXITO! Uno de los exploradores encontró la meta '{meta}'.")
            return True
            
        # 2. Recolectar TODOS los vecinos de TODOS los exploradores
        todos_los_sucesores = []
        for nodo in haz:
            vecinos = grafo.get(nodo, [])
            for vecino in vecinos:
                valor_vecino = h.get(vecino, float('inf'))
                # Guardamos una tupla: (valor, nombre_del_vecino, origen_de_donde_vino)
                todos_los_sucesores.append((valor_vecino, vecino, nodo))
                
        if not todos_los_sucesores:
            print("Ningún explorador tiene a dónde ir. Búsqueda estancada.")
            return False
            
        # 3. Eliminar duplicados (si dos exploradores ven el mismo nodo, cuenta como uno)
        # Usamos un diccionario temporal para esto
        sucesores_unicos = {}
        for valor, vecino, origen in todos_los_sucesores:
            if vecino not in sucesores_unicos:
                sucesores_unicos[vecino] = (valor, origen)
                
        # Convertimos de vuelta a una lista para ordenar
        lista_ordenada = []
        for vecino, (valor, origen) in sucesores_unicos.items():
            lista_ordenada.append((valor, vecino, origen))
            
        # 4. Ordenar a todos los candidatos de mejor a peor (menor a mayor heurística)
        lista_ordenada.sort(key=lambda x: x[0])
        
        print("  -> Opciones descubiertas por el equipo (ordenadas de mejor a peor):")
        for valor, vecino, origen in lista_ordenada:
            print(f"     * '{vecino}' (Valor: {valor}) descubierto desde '{origen}'")
            
        # 5. EL NÚCLEO DEL HAZ: Nos quedamos SOLO con los 'k' mejores
        mejores_k = lista_ordenada[:k]
        
        # Actualizamos las posiciones de nuestros exploradores
        nuevo_haz = [vecino for valor, vecino, origen in mejores_k]
        
        # Verificamos si nos quedamos exactamente en los mismos nodos (estancamiento)
        if set(nuevo_haz) == set(haz):
            print("\n¡ALTO! Los exploradores no encontraron ninguna opción que los saque de su posición actual.")
            print("El equipo se ha quedado atrapado en Máximos Locales.")
            return False
            
        haz = nuevo_haz
        print("-" * 50)
        iteracion += 1

# --- PRUEBA DEL CÓDIGO ---
nodos_de_arranque = ['A', 'C']
busqueda_haz_local(grafo_haz, heuristica, nodos_iniciales=nodos_de_arranque, meta='Z', k=2)
