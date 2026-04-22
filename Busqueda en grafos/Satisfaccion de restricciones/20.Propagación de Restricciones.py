# 1. Componentes del CSP
variables = ['Region_1', 'Region_2', 'Region_3']

# Dominios iniciales. La Región 1 ya está fijada en 'Rojo'.
# Las demás tienen los 3 colores disponibles.
dominios = {
    'Region_1': ['Rojo'], 
    'Region_2': ['Rojo', 'Verde', 'Azul'],
    'Region_3': ['Rojo', 'Verde', 'Azul']
}

# Todas son vecinas entre sí (forman un triángulo)
vecinos = {
    'Region_1': ['Region_2', 'Region_3'],
    'Region_2': ['Region_1', 'Region_3'],
    'Region_3': ['Region_1', 'Region_2']
}

def revisar(dominios, xi, xj):
    """
    Revisa si el dominio de 'xi' es consistente con 'xj'.
    Elimina colores de 'xi' que no tengan ninguna opción compatible en 'xj'.
    """
    revisado = False
    
    # Iteramos sobre una copia del dominio para poder eliminar elementos del original
    for color_x in dominios[xi][:]:
        # Buscamos si existe AL MENOS UN color en xj que sea diferente a color_x
        tiene_opcion_compatible = False
        for color_y in dominios[xj]:
            if color_x != color_y:
                tiene_opcion_compatible = True
                break
                
        # Si no hay ninguna opción compatible en el vecino, este color_x es inútil
        if not tiene_opcion_compatible:
            print(f"     [Poda] El color '{color_x}' se elimina de {xi} porque no deja opciones válidas para {xj}.")
            dominios[xi].remove(color_x)
            revisado = True
            
    return revisado

def propagacion_ac3(variables, dominios, vecinos):
    print("--- Iniciando Propagación de Restricciones (AC-3) ---")
    
    # 1. Llenamos la cola inicial con TODOS los arcos bidireccionales
    # Un arco es una tupla (Region_A, Region_B)
    cola_arcos = []
    for xi in variables:
        for xj in vecinos[xi]:
            cola_arcos.append((xi, xj))
            
    print(f"Cola inicial de arcos a revisar: {len(cola_arcos)} arcos.")
    
    # 2. Mientras haya arcos en la cola, los procesamos
    paso = 1
    while cola_arcos:
        # Sacamos el primer arco de la cola
        xi, xj = cola_arcos.pop(0)
        
        # Revisamos si necesitamos borrar opciones de xi basándonos en xj
        if revisar(dominios, xi, xj):
            # Si el dominio de xi se queda vacío, el problema no tiene solución
            if len(dominios[xi]) == 0:
                print(f"\n[!] ALERTA CRÍTICA: {xi} se quedó sin opciones. ¡Inconsistencia insalvable!")
                return False
                
            # Agregamos a la cola todos los arcos (Vecino, xi) para que los vecinos se re-evalúen
            print(f"  [Propagación] El dominio de {xi} cambió a {dominios[xi]}. Avisando a sus vecinos...")
            for xk in vecinos[xi]:
                # No tiene sentido volver a meter el arco (xj, xi) de donde acabamos de venir
                if xk != xj:
                    cola_arcos.append((xk, xi))
                    print(f"    -> Arco ({xk}, {xi}) añadido a la cola.")
        paso += 1

    print("\n¡Propagación terminada! La red es consistente.")
    return True

# --- PRUEBA DEL CÓDIGO ---
print("Dominios ANTES de AC-3:")
for v, d in dominios.items():
    print(f"  {v}: {d}")
print("-" * 40)

if propagacion_ac3(variables, dominios, vecinos):
    print("-" * 40)
    print("Dominios DESPUÉS de AC-3 (Listos para asignar o ya resueltos):")
    for v, d in dominios.items():
        print(f"  {v}: {d}")
