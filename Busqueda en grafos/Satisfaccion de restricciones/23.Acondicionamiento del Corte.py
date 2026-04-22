import copy

# 1. Componentes del CSP
colores_base = ['Rojo', 'Verde', 'Azul']

# Grafo con un CICLO CERRADO: 1-2-3-4-1
vecinos = {
    'Nodo_1': ['Nodo_2', 'Nodo_4'],
    'Nodo_2': ['Nodo_1', 'Nodo_3'],
    'Nodo_3': ['Nodo_2', 'Nodo_4'],
    'Nodo_4': ['Nodo_3', 'Nodo_1']
}

# 2. DEFINIMOS NUESTRA ESTRATEGIA DE CORTE
# Si "aislamos" el Nodo_1, el ciclo se rompe.
variable_corte = 'Nodo_1'
variables_arbol = ['Nodo_2', 'Nodo_3', 'Nodo_4'] # Esto ahora es una línea recta libre de ciclos

def resolver_arbol_lineal(indice_actual, variables, asignacion, dominios):
    """Resuelve el resto del problema sabiendo que ya NO hay ciclos."""
    # Condición de éxito: Si ya recorrimos toda la línea
    if indice_actual >= len(variables):
        return True
        
    var_actual = variables[indice_actual]
    
    for color in dominios[var_actual]:
        # Verificamos si este color choca con algún vecino ya pintado en la asignación
        conflicto = False
        for vecino in vecinos[var_actual]:
            if vecino in asignacion and asignacion[vecino] == color:
                conflicto = True
                break
                
        if not conflicto:
            asignacion[var_actual] = color
            print(f"      [Árbol] -> {var_actual} pintado de {color}.")
            
            # Avanzamos al siguiente nodo en la línea recta
            if resolver_arbol_lineal(indice_actual + 1, variables, asignacion, dominios):
                return True
                
            # Si falla, despintamos
            del asignacion[var_actual]
            
    return False

def acondicionamiento_del_corte():
    print("--- Iniciando Acondicionamiento del Corte (Cutset Conditioning) ---")
    print(f"[*] Detectamos un ciclo. Variable elegida como Corte: {variable_corte}")
    
    dominios_iniciales = {v: colores_base.copy() for v in vecinos.keys()}
    
    # 3. Prueba los colores en la Variable de Corte
    for color_corte in colores_base:
        print(f"\n[Fase 1: El Corte] Congelando {variable_corte} con el color '{color_corte}'...")
        
        # Iniciamos la asignación con nuestra variable congelada
        asignacion = {variable_corte: color_corte}
        dominios_temporales = copy.deepcopy(dominios_iniciales)
        
        # Como ya fijamos el Nodo 1, le quitamos este color a sus vecinos directos
        falla_inmediata = False
        for vecino in vecinos[variable_corte]:
            if color_corte in dominios_temporales[vecino]:
                dominios_temporales[vecino].remove(color_corte)
                print(f"  -> Advirtiendo al vecino {vecino}: Se le prohíbe usar {color_corte}.")
                if not dominios_temporales[vecino]:
                    falla_inmediata = True # Si un vecino se queda sin opciones, este color de corte no sirve
                    
        if falla_inmediata:
            print(f"  [X] Congelar con {color_corte} causa un fallo inmediato. Probando otro color...")
            continue
            
        # 4. Mandamos a resolver el árbol restante
        print(f"  [*] ¡El ciclo se ha roto! Resolviendo el resto como un árbol lineal ({variables_arbol})...")
        exito = resolver_arbol_lineal(0, variables_arbol, asignacion, dominios_temporales)
        
        if exito:
            print(f"\n¡ÉXITO ROTUNDO! Problema resuelto dividiendo y conquistando.")
            return asignacion
            
    print("\n[!] No se encontró solución.")
    return None

# --- PRUEBA DEL CÓDIGO ---
solucion_final = acondicionamiento_del_corte()

if solucion_final:
    print("\nMapa Final:")
    for nodo, color in solucion_final.items():
        print(f"  {nodo} : {color}")
