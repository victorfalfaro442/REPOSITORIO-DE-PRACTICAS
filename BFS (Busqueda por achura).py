# Representación del árbol de la imagen
arbol = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E', 'F'],
    'D': ['G', 'H'],
    'E': ['I', 'J'],
    'F': ['K', 'L'],
    # Nodos hoja (no tienen hijos)
    'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': []
}

from collections import deque #Librería Double-Ended Queue. Proporciona mayor comodidad al trabajar con colas.

def busqueda_anchura_bfs(grafo, origen, meta):
    # 1. Creamos una Cola S
    # Usamos deque porque permite sacar elementos del inicio de forma muy eficiente
    S = deque()
    
    # Estructura adicional para llevar el registro de visitados (mencionado en el paso 3c)
    visitados = set()
    
    # 2. Agregamos el origen a la Cola S
    S.append(origen)
    
    # 3. Bucle Mientras S no esté vacío:
    while S:
        # a) Sacamos el nodo V encima de la cola S (el primero en entrar)
        V = S.popleft()
        print(f"Revisando nodo: {V}") # Imprimimos para ver el orden real de búsqueda
        
        # b) Si V es el nodo Meta, devuelve solución. FIN
        if V == meta:
            print(f"\n¡Éxito! Nodo Meta '{meta}' encontrado.")
            return True
            
        # c) Si V no ha sido visitado, marcamos V como visitado
        if V not in visitados:
            visitados.add(V)
            
            # ii. Para cada hijo del nodo V, agrega el nodo hijo en la cola.
            hijos = grafo.get(V, [])
            for hijo in hijos:
                S.append(hijo)
                
    # Si la cola se vacía y no se activó el paso 'b'
    print(f"\nEl nodo Meta '{meta}' no se encuentra en el árbol.")
    return False

# --- PRUEBA DEL CÓDIGO ---
# Vamos a buscar el nodo 'J' empezando desde la raíz 'A'
print("Iniciando Búsqueda en Anchura (BFS)...")
busqueda_anchura_bfs(arbol, origen='A', meta='J')