# 1. Componentes del CSP
variables = ['A', 'B', 'C', 'D', 'E']

# Dominios: 'E' está encaprichado y solo tiene la opción 'Rojo'
dominios = {
    'A': ['Rojo', 'Azul'],
    'B': ['Verde', 'Lima'],
    'C': ['Blanco', 'Gris'],
    'D': ['Negro', 'Cafe'],
    'E': ['Rojo']  
}

# Restricciones: Solo 'A' y 'E' se odian. Los demás son libres.
vecinos = {
    'A': ['E'], 'B': [], 'C': [], 'D': [], 'E': ['A']
}

def salto_atras_dirigido(indice_var, asignacion):
    # 1. Condición de Éxito
    if indice_var >= len(variables):
        return True, None

    var_actual = variables[indice_var]
    print(f"\n[Turno de: {var_actual}]")

    # Esta es nuestra "Lista Negra" temporal
    conflictos_de_esta_variable = []

    # 2. Probamos los colores disponibles
    for color in dominios[var_actual]:
        print(f"  -> Probando color {color}...")

        # Chequeamos restricciones con las variables que YA pintamos
        conflicto_con = None
        for var_previa in asignacion:
            if var_previa in vecinos[var_actual] and asignacion[var_previa] == color:
                conflicto_con = var_previa
                break

        if conflicto_con:
            print(f"  [X] Conflicto: El color '{color}' choca con {conflicto_con}.")
            # Anotamos el culpable del conflicto
            conflictos_de_esta_variable.append(conflicto_con)
        else:
            print(f"  [*] ¡Válido! Asignando '{color}' a {var_actual}.")
            asignacion[var_actual] = color

            # 3. Llamada Recursiva (Avanzamos a la siguiente variable)
            exito, var_destino_salto = salto_atras_dirigido(indice_var + 1, asignacion)

            if exito:
                return True, None

            if var_destino_salto and var_destino_salto != var_actual:
                # Detectamos valores innecesarios 
                print(f"  [>>] Salto Atrás en proceso. Ignorando a {var_actual}. Saltando hacia {var_destino_salto}...")
                del asignacion[var_actual]
                return False, var_destino_salto # Paso el salto hacia atrás

            if var_destino_salto == var_actual:
                # Borramos el generador del conflicto 
                print(f"  [!] Aterrizamos en el culpable ({var_actual}). Despintando y buscando mi siguiente color...")
                del asignacion[var_actual]

    # 5. Si llegamos aquí, NINGÚN color funcionó. (Callejón sin salida)
    if conflictos_de_esta_variable:
        # Buscamos al culpable MÁS RECIENTE en nuestra lista negra
        culpable = max(conflictos_de_esta_variable, key=lambda x: variables.index(x))
        print(f"  [<-] ¡Callejón sin salida en {var_actual}! El culpable fue {culpable}.")
        print(f"       ¡INICIANDO SALTO DIRECTO HACIA {culpable}!")
        return False, culpable
    else:
        return False, None

# --- PRUEBA DEL CÓDIGO ---
print("--- Iniciando Salto Atrás Dirigido por Conflictos (CBJ) ---")
asignacion_final = {}
exito, _ = salto_atras_dirigido(0, asignacion_final)

if exito:
    print("\n¡ÉXITO! Solución encontrada:")
    for var, color in asignacion_final.items():
        print(f"  {var} : {color}")
