import math
import random

# Nuestro grafo con la trampa en 'D'
grafo_temple = {
    'Inicio': ['A', 'B'],
    'A': ['Inicio', 'C', 'D'],
    'B': ['Inicio', 'E', 'G'], 
    'C': ['A'],
    'D': ['A', 'F'],      # Máximo local. La salida es 'F'
    'F': ['D', 'G'],
    'G': ['F', 'B'],      
    'E': ['B', 'Z'],
    'Z': ['E']            # META
}

# Heurística (Queremos llegar a 0)
heuristica = {
    'Inicio': 10, 'A': 7, 'B': 9, 'C': 8, 
    'D': 4,       
    'F': 5, 'G': 6, 'E': 3, 'Z': 0
}

def temple_simulado(grafo, h, origen, meta, temp_inicial=10.0, factor_enfriamiento=0.85):
    print(f"--- Iniciando Temple Simulado (Origen: '{origen}') ---")
    
    nodo_actual = origen
    camino = [nodo_actual]
    T = temp_inicial
    
    # Mientras la temperatura no sea cercana a cero (congelado)
    while T > 0.1:
        valor_actual = h[nodo_actual]
        print(f"\n[T={T:.2f}] Actual: {nodo_actual} (Valor: {valor_actual})")
        
        if nodo_actual == meta:
            print(f"\n¡ÉXITO! Meta '{meta}' encontrada.")
            print(f"Camino recorrido: {camino}")
            return True
            
        vecinos = grafo.get(nodo_actual, [])
        if not vecinos:
            return False
            
        # 1. Elegimos un vecino COMPLETAMENTE AL AZAR
        vecino_aleatorio = random.choice(vecinos)
        valor_vecino = h.get(vecino_aleatorio, float('inf'))
        
        print(f"  -> Vecino elegido al azar: '{vecino_aleatorio}' (Valor: {valor_vecino})")
        
        # Calculamos qué tanto empeoramos (Delta E)
        # Como queremos minimizar, si valor_vecino es mayor, Delta_E será positivo.
        delta_e = valor_vecino - valor_actual
        
        # 2. Si el vecino es MEJOR (o igual), damos el paso sin pensarlo
        if delta_e <= 0:
            print("  [*] El paso es mejor. ¡Lo tomamos!")
            nodo_actual = vecino_aleatorio
            camino.append(nodo_actual)
            
        # 3. Si el vecino es PEOR, lanzamos los dados
        else:
            probabilidad_aceptar = math.exp(-delta_e / T)
            dado = random.uniform(0, 1) # Un número al azar entre 0 y 1
            
            print(f"  [!] El paso es peor. Probabilidad de aceptarlo: {probabilidad_aceptar*100:.1f}%")
            print(f"      (Dado tirado: {dado:.3f})")
            
            if dado <= probabilidad_aceptar:
                print("  [*] ¡Paso aceptado por probabilidad! Empeoramos estratégicamente.")
                nodo_actual = vecino_aleatorio
                camino.append(nodo_actual)
            else:
                print("  [X] Paso rechazado. Nos quedamos donde estamos.")
                
        # 4. Enfriamos el sistema un poco para la siguiente iteración
        T = T * factor_enfriamiento
        print("-" * 40)
        
    print("\nEl sistema se ha congelado (T llegó a 0) y no encontramos la meta.")
    print(f"Nos quedamos atrapados en: {nodo_actual}")
    return False

# --- PRUEBA DEL CÓDIGO ---
temple_simulado(grafo_temple, heuristica, origen='Inicio', meta='Z')
