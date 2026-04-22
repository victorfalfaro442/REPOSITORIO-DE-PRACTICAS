# Grafo AND/OR. Definimos si los hijos de un nodo son opciones (OR) o requisitos (AND)
grafo_and_or = {
    'A': {'tipo': 'OR',  'hijos': ['B', 'C']},
    'B': {'tipo': 'AND', 'hijos': ['D', 'E']}, # D y E son obligatorios para B
    'C': {'tipo': 'OR',  'hijos': ['F']},
    # Nodos terminales (las sub-tareas más pequeñas ya resueltas)
    'D': {'tipo': 'OR', 'hijos': []},
    'E': {'tipo': 'OR', 'hijos': []},
    'F': {'tipo': 'OR', 'hijos': []}
}

# Heurística: ¿Cuánto estimamos que cuesta resolver cada sub-tarea por sí sola?
# Valores más bajos indican sub-tareas más fáciles/baratas.
h_costos = {
    'A': 10, 'B': 8, 'C': 5, 
    'D': 2,  'E': 3, 'F': 6
}

def resolver_ao_estrella(grafo, h, nodo):
    # Condición base: Si el nodo es terminal (no tiene hijos), retornamos su costo heurístico
    info_nodo = grafo.get(nodo, {'tipo': 'OR', 'hijos': []})
    if not info_nodo['hijos']:
        print(f"  [Hoja] Tarea '{nodo}' completada. Costo: {h[nodo]}")
        return h[nodo]
        
    print(f"Evaluando cómo resolver '{nodo}' (Tipo: {info_nodo['tipo']})")
    costos_hijos = []
    
    # Llamamos a la función recursivamente para cada hijo
    for hijo in info_nodo['hijos']:
        costos_hijos.append(resolver_ao_estrella(grafo, h, hijo))
        
    if info_nodo['tipo'] == 'AND':
        # Si es AND, sumamos los costos, porque necesitamos TODO
        costo_total = sum(costos_hijos) + 1 # +1 por el costo de unirlos
        print(f"  -> Para resolver '{nodo}' (AND), se requiere resolver todos sus hijos. Costo calculado: {costo_total}")
        return costo_total
        
    elif info_nodo['tipo'] == 'OR':
        # Si es OR, tomamos el mínimo, porque solo necesitamos la ruta más barata
        costo_total = min(costos_hijos) + 1 # +1 por el esfuerzo de elegir/bajar un nivel
        print(f"  -> Para resolver '{nodo}' (OR), tomamos la mejor opción. Costo calculado: {costo_total}")
        return costo_total

print("--- Iniciando Resolución de Problema con AO* ---")
costo_final = resolver_ao_estrella(grafo_and_or, h_costos, 'A')
print(f"\nEl costo óptimo total para resolver el problema raíz 'A' es: {costo_final}")
