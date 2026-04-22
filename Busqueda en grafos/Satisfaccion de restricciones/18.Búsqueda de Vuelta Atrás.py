#Tenemos un tablero de ajedrez tradicional de 8x8 (o de NxN). El objetivo es colocar N reinas en el tablero de tal manera que ninguna reina pueda atacar a otra. (Recordemos que la reina ataca en línea recta vertical, horizontal y diagonal).
# Definimos el tamaño del tablero (4x4)
N = 4

def imprimir_tablero(tablero):
    """Muestra el tablero de forma visual en la consola."""
    print("\nTablero Final:")
    for fila in tablero:
        fila_visual = ["[Q]" if celda == 1 else "[ ]" for celda in fila]
        print(" ".join(fila_visual))
    print()

def es_seguro(tablero, fila, col):
    """Verifica si es seguro colocar una reina en tablero[fila][col]."""
    # 1. Comprobar la fila hacia la izquierda
    for i in range(col):
        if tablero[fila][i] == 1:
            return False
            
    # 2. Comprobar la diagonal superior izquierda
    for i, j in zip(range(fila, -1, -1), range(col, -1, -1)):
        if tablero[i][j] == 1:
            return False
            
    # 3. Comprobar la diagonal inferior izquierda
    for i, j in zip(range(fila, N, 1), range(col, -1, -1)):
        if tablero[i][j] == 1:
            return False
            
    return True

def resolver_n_reinas(tablero, col):
    """La función recursiva que aplica la Vuelta Atrás."""
    # 1. Condición de éxito: Si ya pasamos la última columna, hemos colocado todas las reinas
    if col >= N:
        return True

    print(f"\n--- Evaluando la Columna {col} ---")
    
    # 2. Intentar colocar una reina en cada fila de esta columna
    for fila in range(N):
        print(f"  -> Intentando colocar reina en (Fila {fila}, Columna {col})...")
        
        if es_seguro(tablero, fila, col):
            print(f"  [*] ¡Seguro! Colocando reina en ({fila}, {col}).")
            tablero[fila][col] = 1  # Colocamos la reina
            
            # 3. Llamada recursiva: Avanzamos a la SIGUIENTE columna
            if resolver_n_reinas(tablero, col + 1):
                return True
                
            # 4. LA VUELTA ATRÁS (BACKTRACKING)
            # Si la llamada recursiva devolvió False, significa que este camino falló más adelante.
            print(f"  [!] Callejón sin salida detectado. VUELTA ATRÁS: Quitando reina de ({fila}, {col}).")
            tablero[fila][col] = 0  # Quitamos la reina
        else:
            print(f"  [X] Conflicto. La posición ({fila}, {col}) ya está bajo ataque.")

    # 5. Si probamos todas las filas en esta columna y ninguna sirvió, hay que retroceder
    print(f"  [<-] Ninguna fila es segura en la columna {col}. Retrocediendo a la columna anterior...")
    return False

# --- PRUEBA DEL CÓDIGO ---
# Creamos un tablero vacío de 4x4 (lleno de ceros)
tablero_inicial = [[0 for _ in range(N)] for _ in range(N)]

print(f"--- Iniciando Búsqueda de Vuelta Atrás ({N} Reinas) ---")

if resolver_n_reinas(tablero_inicial, col=0):
    print("\n¡ÉXITO! Se encontró una solución válida.")
    imprimir_tablero(tablero_inicial)
else:
    print("\nNo existe solución para este tamaño de tablero.")
