# 1. LA REALIDAD (El Agente NO tiene acceso directo a este diccionario)
# Solo puede descubrir los vecinos si se encuentra físicamente en el nodo.
entorno_real = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E'],
    'D': ['Meta'],
    'E': ['Meta'],
    'Meta': []
}

# 2. LA MENTE DEL AGENTE (Su tabla Heurística H)
memoria_H = {
    'A': 1, 'B': 1, 'C': 1, 
    'D': 1, 'E': 1, 'Meta': 0
}

# Simulamos los "sensores" del agente
def observar_entorno(nodo):
    """El agente usa sus sensores para ver qué caminos salen de donde está parado."""
    return entorno_real.get(nodo, [])

def busqueda_online_lrta(origen, meta):
    print(f"--- Iniciando Búsqueda Online LRTA* (Aterrizando en '{origen}') ---")
    
    estado_actual = origen
    camino_fisico = [estado_actual] # Los pasos reales que da en el mundo
    
    while estado_actual != meta:
        print(f"\n[Físicamente en]: {estado_actual} | Mi estimación actual H({estado_actual}) = {memoria_H[estado_actual]}")
        
        # 1. El agente "mira" a su alrededor usando sus sensores
        vecinos_visibles = observar_entorno(estado_actual)
        
        if not vecinos_visibles:
            print("Error catastrófico: Atrapado sin salida (Esto no debería pasar hoy).")
            return False
            
        print(f"  -> Sensores detectan caminos hacia: {vecinos_visibles}")
        
        # 2. Evaluar a cada vecino usando la fórmula f(s') = costo(s,s') + H(s')
        # Asumiremos que dar el paso cuesta 1 de energía.
        mejor_vecino = None
        mejor_f = float('inf')
        
        for vecino in vecinos_visibles:
            # Si es un nodo nuevo que no está en memoria, asumimos optimismo (1)
            h_vecino = memoria_H.get(vecino, 1)
            costo_paso = 1
            f_vecino = costo_paso + h_vecino
            
            print(f"     * Evalúo '{vecino}': Costo de ir (1) + Su Heurística ({h_vecino}) = {f_vecino}")
            
            if f_vecino < mejor_f:
                mejor_f = f_vecino
                mejor_vecino = vecino
                
        # 3. EL PASO DE APRENDIZAJE (Updating)
        # Antes de movernos, corregimos la estimación del nodo en el que estamos parados.
        if memoria_H[estado_actual] != mejor_f:
            print(f"  [!] ¡AHA! Actualizando mi memoria mental. H({estado_actual}) cambia de {memoria_H[estado_actual]} a {mejor_f}")
            memoria_H[estado_actual] = mejor_f
            
        # 4. EJECUTAR LA ACCIÓN (Moverse físicamente en el mundo real)
        print(f"  >> Caminando físicamente hacia el nodo '{mejor_vecino}'...")
        estado_actual = mejor_vecino
        camino_fisico.append(estado_actual)
        
    print(f"\n¡ÉXITO! Meta '{meta}' alcanzada físicamente.")
    print(f"Pasos reales dados en el mundo: {camino_fisico}")
    print(f"Memoria heurística final tras aprender: {memoria_H}")
    return True

# --- PRUEBA DEL CÓDIGO ---
busqueda_online_lrta('A', 'Meta')
