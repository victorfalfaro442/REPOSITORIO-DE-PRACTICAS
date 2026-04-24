print("--- INICIANDO BUSCADOR DE EQUILIBRIOS DE NASH ---")

# 1. DEFINICIÓN DEL JUEGO (Forma Normal)
jugadores = ['Aerolinea_A', 'Aerolinea_B']
estrategias_A = ['Precio_Alto', 'Precio_Bajo']
estrategias_B = ['Precio_Alto', 'Precio_Bajo']

# Matriz de Pagos: (Estrategia_A, Estrategia_B) -> (Utilidad_A, Utilidad_B)
# Los valores representan millones de dólares de ganancia.
matriz_pagos = {
    ('Precio_Alto', 'Precio_Alto'): (50, 50),  # Cooperación mutua (Cártel)
    ('Precio_Alto', 'Precio_Bajo'): (0, 80),   # A es traicionada por B
    ('Precio_Bajo', 'Precio_Alto'): (80, 0),   # A traiciona a B
    ('Precio_Bajo', 'Precio_Bajo'): (20, 20)   # Guerra de precios (Traición mutua)
}

def encontrar_equilibrios_nash():
    print("\n[Fase 1] Buscando las Mejores Respuestas (Best Responses) de cada jugador...")
    
    mejores_respuestas_A = set()
    mejores_respuestas_B = set()

    # A) ¿Qué debe hacer la Aerolínea A para cada jugada posible de la Aerolínea B?
    for est_B in estrategias_B:
        mejor_utilidad = float('-inf')
        mejor_jugada_A = None
        
        for est_A in estrategias_A:
            utilidad_A = matriz_pagos[(est_A, est_B)][0] # El índice 0 es la ganancia de A
            if utilidad_A > mejor_utilidad:
                mejor_utilidad = utilidad_A
                mejor_jugada_A = est_A
                
        # Guardamos la combinación ganadora desde la perspectiva de A
        mejores_respuestas_A.add((mejor_jugada_A, est_B))
        print(f"  -> Si B elige '{est_B}', lo mejor para A es '{mejor_jugada_A}' (Gana {mejor_utilidad}M)")

    print("\n  --------------------------------------------------")

    # B) ¿Qué debe hacer la Aerolínea B para cada jugada posible de la Aerolínea A?
    for est_A in estrategias_A:
        mejor_utilidad = float('-inf')
        mejor_jugada_B = None
        
        for est_B in estrategias_B:
            utilidad_B = matriz_pagos[(est_A, est_B)][1] # El índice 1 es la ganancia de B
            if utilidad_B > mejor_utilidad:
                mejor_utilidad = utilidad_B
                mejor_jugada_B = est_B
                
        # Guardamos la combinación ganadora desde la perspectiva de B
        mejores_respuestas_B.add((est_A, mejor_jugada_B))
        print(f"  -> Si A elige '{est_A}', lo mejor para B es '{mejor_jugada_B}' (Gana {mejor_utilidad}M)")

    print("\n[Fase 2] Cruzando datos para encontrar la tregua matemática...")
    equilibrios = mejores_respuestas_A.intersection(mejores_respuestas_B)
    
    return equilibrios

# --- EJECUCIÓN DEL ANÁLISIS ---
resultados_nash = encontrar_equilibrios_nash()

print("\n" + "="*55)
print(" RESULTADO: EQUILIBRIOS DE NASH (ESTRATEGIAS PURAS) ")
print("="*55)

if not resultados_nash:
    print("No se encontraron equilibrios puros en este juego.")
    print("(Se requeriría jugar con probabilidades / Estrategias Mixtas).")
else:
    for eq in resultados_nash:
        pago_A = matriz_pagos[eq][0]
        pago_B = matriz_pagos[eq][1]
        print(f"[*] El juego se estancará inevitablemente en: {eq[0]} vs {eq[1]}")
        print(f"    Ganancias finales: Aerolínea A ({pago_A}M), Aerolínea B ({pago_B}M)")