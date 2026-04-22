# 1. Definimos los componentes del CSP
variables = ['Region_1', 'Region_2', 'Region_3', 'Region_4']

# Dominios: Los colores disponibles para cada región
dominios = {
    'Region_1': ['Rojo', 'Verde', 'Azul'],
    'Region_2': ['Rojo', 'Verde', 'Azul'],
    'Region_3': ['Rojo', 'Verde', 'Azul'],
    'Region_4': ['Rojo', 'Verde', 'Azul']
}

# Restricciones: No pueden compartir color
# Region_1 está en el centro y toca a todas las demás.
vecinos = {
    'Region_1': ['Region_2', 'Region_3', 'Region_4'],
    'Region_2': ['Region_1', 'Region_3'],
    'Region_3': ['Region_1', 'Region_2', 'Region_4'],
    'Region_4': ['Region_1', 'Region_3']
}

def es_asignacion_valida(variable, color_propuesto, asignacion_actual):
    """Verifica que el color propuesto no rompa las reglas con los vecinos ya pintados."""
    for vecino in vecinos[variable]:
        # Si el vecino ya está pintado y tiene el mismo color, ¡regla rota!
        if vecino in asignacion_actual and asignacion_actual[vecino] == color_propuesto:
            return False
    return True

def resolver_csp_backtracking(asignacion_actual):
    # 1. Condición de éxito: Si ya pintamos todas las regiones, ganamos.
    if len(asignacion_actual) == len(variables):
        return asignacion_actual
        
    # 2. Elegimos la siguiente región que aún no tiene color
    variable_no_asignada = None
    for var in variables:
        if var not in asignacion_actual:
            variable_no_asignada = var
            break
            
    print(f"\n[Turno de: {variable_no_asignada}]")
    
    # 3. Probamos los colores disponibles para esta región
    for color in dominios[variable_no_asignada]:
        print(f"  -> Intentando pintar {variable_no_asignada} de color {color}...")
        
        if es_asignacion_valida(variable_no_asignada, color, asignacion_actual):
            print(f"  [*] ¡Válido! {variable_no_asignada} se pinta de {color}.")
            # Asignamos el color
            asignacion_actual[variable_no_asignada] = color
            
            # 4. Llamada recursiva (avanzamos a la siguiente región)
            resultado = resolver_csp_backtracking(asignacion_actual)
            
            # Si el resultado no es None, significa que encontramos la solución final
            if resultado is not None:
                return resultado
                
            # 5. EL RETROCESO (Backtracking)
            # Borramos nuestro color y probamos con el siguiente del ciclo 'for'.
            print(f"  [!] Callejón sin salida detectado adelante. Despintando {variable_no_asignada} ({color}) y retrocediendo...")
            del asignacion_actual[variable_no_asignada]
        else:
            print(f"  [X] Conflicto. El color {color} rompe las reglas con un vecino.")
            
    # Si probamos todos los colores y ninguno funcionó, retornamos None para forzar el retroceso anterior
    return None

# --- PRUEBA DEL CÓDIGO ---
print("--- Iniciando Solución de CSP (Coloreado de Mapas) ---")
solucion = resolver_csp_backtracking({})

if solucion:
    print("\n¡ÉXITO! El mapa ha sido coloreado cumpliendo todas las reglas:")
    for region, color in solucion.items():
        print(f"  {region} : {color}")
else:
    print("\nNo existe ninguna solución posible con estas reglas y colores.")
