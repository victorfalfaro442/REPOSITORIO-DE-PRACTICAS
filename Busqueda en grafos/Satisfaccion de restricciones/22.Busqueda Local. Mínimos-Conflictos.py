import random

# 1. Componentes del CSP
variables = ['Region_1', 'Region_2', 'Region_3', 'Region_4']
colores = ['Rojo', 'Verde', 'Azul']

vecinos = {
    'Region_1': ['Region_2', 'Region_3', 'Region_4'],
    'Region_2': ['Region_1', 'Region_3'],
    'Region_3': ['Region_1', 'Region_2', 'Region_4'],
    'Region_4': ['Region_1', 'Region_3']
}

def contar_conflictos(variable, color_propuesto, asignacion_actual):
    """Cuenta cuántos vecinos de la variable tienen el mismo color propuesto."""
    conflictos = 0
    for vecino in vecinos[variable]:
        if asignacion_actual[vecino] == color_propuesto:
            conflictos += 1
    return conflictos

def minimos_conflictos(max_pasos=100):
    print("--- Iniciando Búsqueda Local: Mínimos-Conflictos ---")
    
    # 1. Generar una asignación inicial TOTALMENTE AL AZAR
    asignacion = {var: random.choice(colores) for var in variables}
    print(f"Estado inicial aleatorio: {asignacion}\n")
    
    for paso in range(1, max_pasos + 1):
        # 2. Identificar qué variables están en conflicto actualmente
        variables_conflictivas = []
        for var in variables:
            # Si el color actual de la variable choca con 1 o más vecinos, está en conflicto
            if contar_conflictos(var, asignacion[var], asignacion) > 0:
                variables_conflictivas.append(var)
                
        # Si la lista está vacía, no hay conflictos.
        if not variables_conflictivas:
            print(f"\n¡ÉXITO! Solución encontrada en el paso {paso - 1}.")
            return asignacion
            
        # 3. Elegir una variable conflictiva al azar para arreglarla
        var_a_arreglar = random.choice(variables_conflictivas)
        print(f"[Paso {paso}] Conflicto detectado. Intentando arreglar: {var_a_arreglar} (Color actual: {asignacion[var_a_arreglar]})")
        
        # 4. Probar todos los colores para encontrar el que cause MENOS conflictos
        mejor_color = asignacion[var_a_arreglar]
        min_conflictos_encontrados = float('inf')
        
        # Guardamos los mejores colores en una lista para desempatar al azar si es necesario
        mejores_colores = []
        
        for color in colores:
            conflictos = contar_conflictos(var_a_arreglar, color, asignacion)
            print(f"  -> Si la pinto de {color}, causaría {conflictos} conflictos.")
            
            if conflictos < min_conflictos_encontrados:
                min_conflictos_encontrados = conflictos
                mejores_colores = [color] # Reiniciamos la lista con el nuevo campeón
            elif conflictos == min_conflictos_encontrados:
                mejores_colores.append(color) # Empate, lo agregamos a la lista
                
        # Elegimos al azar entre los colores que empataron con el menor número de conflictos
        color_final = random.choice(mejores_colores)
        
        if color_final != asignacion[var_a_arreglar]:
            print(f"  [*] ¡Cambio realizado! {var_a_arreglar} cambia a {color_final}.")
            asignacion[var_a_arreglar] = color_final
        else:
            print(f"  [-] Se queda igual (ningún otro color mejora la situación).")
            
        print("-" * 50)
        
    print("\n[!] Fracaso. Se alcanzó el límite máximo de pasos sin encontrar solución.")
    return None

# --- PRUEBA DEL CÓDIGO ---
solucion = minimos_conflictos(max_pasos=20)

if solucion:
    print("Mapa final sin conflictos:")
    for region, color in solucion.items():
        print(f"  {region} : {color}")
