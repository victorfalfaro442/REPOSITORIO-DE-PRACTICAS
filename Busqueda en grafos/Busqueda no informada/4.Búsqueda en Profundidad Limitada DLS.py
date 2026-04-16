arbol_profundo = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': ['G', 'H'],
    'E': ['I'],
    'F': ['J', 'K'],
    'G': ['L'],
    'I': ['M', 'N'],
    'K': ['O'],
    'L': ['P'],
    'N': ['Q'],
    'Q': ['R'],
    # Nodos hoja
    'H': [], 'J': [], 'M': [], 'O': [], 'P': [], 'R': []
}

def busqueda_profundidad_limitada_recursiva(grafo, nodo_actual, meta, limite, camino_actual=[]):
    """
    Implementación recursiva nativa de DLS.
    """
    # Actualizamos el camino recorrido hasta este nodo
    nuevo_camino = camino_actual + [nodo_actual]
    profundidad_actual = len(camino_actual)
    
    # Imprimimos para visualizar el rastro
    print(f"Revisando: {nodo_actual} (Profundidad: {profundidad_actual}, Límite: {limite})")

    # 1. Condición Base: ¿Es la Meta?
    if nodo_actual == meta:
        return "ÉXITO", nuevo_camino

    # 2. Condición Base: ¿Alcanzamos el Límite?
    if profundidad_actual >= limite:
        # Checamos si el nodo tiene hijos a los que no podemos bajar
        if grafo.get(nodo_actual, []):
            return "CORTE", None # Hubo un corte de rama
        else:
            return "FALLO", None # Es una hoja normal dentro del límite

    # 3. Paso Recursivo: Explorar hijos
    hijos = grafo.get(nodo_actual, [])
    hubo_corte_abajo = False
    
    for hijo in hijos:
        # Llamada recursiva bajando un nivel
        resultado, camino_final = busqueda_profundidad_limitada_recursiva(
            grafo, hijo, meta, limite, nuevo_camino
        )
        
        if resultado == "ÉXITO":
            return "ÉXITO", camino_final
        
        if resultado == "CORTE":
            # Recordamos que hubo un corte en alguna rama inferior
            hubo_corte_abajo = True 

    # Si terminamos de ver los hijos y no hubo éxito
    if hubo_corte_abajo:
        return "CORTE", None
    else:
        return "FALLO", None

# --- FUNCIÓN AUXILIAR (WRAPPER) PARA FORMATEAR LA SALIDA ---
def ejecutar_dls(grafo, origen, meta, limite):
    print(f"\n--- Iniciando DLS (Meta: '{meta}', Límite: {limite}) ---")
    resultado, camino = busqueda_profundidad_limitada_recursiva(grafo, origen, meta, limite)
    
    if resultado == "ÉXITO":
        print(f"RESULTADO: ¡ÉXITO! Meta encontrada.")
        print(f"Camino: {camino}")
    elif resultado == "CORTE":
        print(f"RESULTADO: CORTE (Cutoff). El límite de {limite} es demasiado bajo.")
    else:
        print(f"RESULTADO: FALLO. La meta no existe en las zonas accesibles.")

# --- PRUEBAS DEL CÓDIGO ---
# Recordamos que la Meta 'Q' está en profundidad 5.

# PRUEBA 1: Límite muy bajo (Nivel 3). Debería dar CORTE.
ejecutar_dls(arbol_profundo, 'A', 'Q', limite=3)

# PRUEBA 2: Límite exacto (Nivel 5). Debería dar ÉXITO.
ejecutar_dls(arbol_profundo, 'A', 'Q', limite=5)
