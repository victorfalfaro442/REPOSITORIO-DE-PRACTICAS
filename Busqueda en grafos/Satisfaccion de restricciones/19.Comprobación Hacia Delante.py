import copy

# 1. Componentes del CSP
variables = ['Region_1', 'Region_2', 'Region_3', 'Region_4']

# La memoria dinámica: Las opciones que le quedan a cada región
dominios_iniciales = {
    'Region_1': ['Rojo', 'Verde', 'Azul'],
    'Region_2': ['Rojo', 'Verde', 'Azul'],
    'Region_3': ['Rojo', 'Verde', 'Azul'],
    'Region_4': ['Rojo', 'Verde', 'Azul']
}

vecinos = {
    'Region_1': ['Region_2', 'Region_3', 'Region_4'],
    'Region_2': ['Region_1', 'Region_3'],
    'Region_3': ['Region_1', 'Region_2', 'Region_4'],
    'Region_4': ['Region_1', 'Region_3']
}

def comprobacion_hacia_delante(asignacion, dominios_actuales):
    # 1. Condición de éxito
    if len(asignacion) == len(variables):
        return asignacion
        
    # 2. Elegimos la siguiente región sin pintar
    var_actual = None
    for var in variables:
        if var not in asignacion:
            var_actual = var
            break
            
    print(f"\n[Turno de: {var_actual}]")
    print(f"  Colores disponibles para elegir: {dominios_actuales[var_actual]}")
    
    # 3. Probamos los colores disponibles en el dominio de esta variable
    for color in dominios_actuales[var_actual]:
        print(f"  -> Probando color {color}...")
        
        # Hacemos una copia de los dominios, por si tenemos que retroceder más tarde
        nuevos_dominios = copy.deepcopy(dominios_actuales)
        
        # 4. EL RADAR (Forward Checking): Miramos hacia el futuro
        falla_futura = False
        
        for vecino in vecinos[var_actual]:
            # Solo afectamos a los vecinos que AÚN NO han sido pintados
            if vecino not in asignacion:
                # Si el color que elegí está en las opciones de mi vecino, se lo quito
                if color in nuevos_dominios[vecino]:
                    nuevos_dominios[vecino].remove(color)
                    print(f"     [Radar] Quitamos el {color} de las opciones de {vecino}. Le queda: {nuevos_dominios[vecino]}")
                    
                    # Si al quitarle la opción, el vecino se queda en cero
                    if len(nuevos_dominios[vecino]) == 0:
                        falla_futura = True
                        print(f"     [!] ALERTA CRÍTICA: {vecino} se quedó sin opciones. Este camino fallará.")
                        break # Dejamos de mirar vecinos, este color no sirve
                        
        # 5. Si el radar dice que todo está bien, avanzamos
        if not falla_futura:
            print(f"  [*] Radar limpio. Pintando {var_actual} de {color}.")
            asignacion[var_actual] = color
            
            # Llamada recursiva mandando los dominios encogidos
            resultado = comprobacion_hacia_delante(asignacion, nuevos_dominios)
            
            if resultado is not None:
                return resultado
                
            # Backtracking tradicional si fallamos más abajo
            print(f"  [!] Retrocediendo y despintando {var_actual}...")
            del asignacion[var_actual]
        else:
            print(f"  [X] Rechazamos el {color} en {var_actual} para evitar un error futuro.")
            
    return None

# --- PRUEBA DEL CÓDIGO ---
print("--- Iniciando CSP con Comprobación Hacia Delante ---")
solucion = comprobacion_hacia_delante({}, dominios_iniciales)

if solucion:
    print("\n¡ÉXITO! El mapa ha sido coloreado:")
    for region, color in solucion.items():
        print(f"  {region} : {color}")
