import heapq
import time

# Intentamos importar las librerías gráficas. 
# Si el usuario no las tiene, el programa no fallará, solo omitirá el dibujo.
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    GRAFICOS_DISPONIBLES = True
except ImportError:
    GRAFICOS_DISPONIBLES = False


def simulador_dijkstra_consola(grafo, nodo_inicio, nodo_destino):
    """
    Simulador paso a paso del Algoritmo de Dijkstra.
    Encuentra el camino más corto en un grafo ponderado y explica cada decisión.
    """
    print(f"\n[{nodo_inicio}] --- INICIANDO SIMULACIÓN DE DIJKSTRA --- [{nodo_destino}]")
    
    # 1. INICIALIZACIÓN
    # Guardamos la distancia mínima conocida desde el inicio hasta cada nodo.
    # Al principio, todas son "infinito" (float('inf')) porque no conocemos los caminos.
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[nodo_inicio] = 0 # La distancia del inicio a sí mismo es 0.
    
    # Este diccionario nos ayudará a rastrear de dónde venimos para reconstruir la ruta al final.
    padres = {nodo: None for nodo in grafo}
    
    # El Min-Heap actúa como nuestra "lista de tareas pendientes", priorizando 
    # automáticamente los nodos que están más cerca (menor distancia acumulada).
    cola_prioridad = [(0, nodo_inicio)]
    
    # Un conjunto para no volver a evaluar nodos que ya cerramos (nodos visitados).
    visitados = set()
    
    paso = 1 # Contador para que la consola se vea ordenada

    # 2. BUCLE PRINCIPAL DE BÚSQUEDA
    while cola_prioridad:
        # Extraemos el nodo con la menor distancia acumulada en nuestra cola
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        # Si el nodo ya fue visitado previamente de forma más eficiente, lo saltamos
        if nodo_actual in visitados:
            continue
            
        print(f"\n--- PASO {paso} ---")
        print(f"-> Visitando nodo: '{nodo_actual}' (Distancia acumulada actual: {distancia_actual})")
        paso += 1
        
        # Lo marcamos como visitado (cerramos este nodo)
        visitados.add(nodo_actual)
        
        # Si llegamos al destino, ¡terminamos! Dijkstra garantiza que es la ruta más corta.
        if nodo_actual == nodo_destino:
            print(f"¡DESTINO '{nodo_destino}' ALCANZADO! Búsqueda finalizada.")
            break
            
        # 3. EVALUACIÓN DE VECINOS
        # Revisamos a dónde podemos ir desde el nodo en el que estamos parados
        for vecino, peso_arista in grafo[nodo_actual].items():
            if vecino in visitados:
                continue # Si el vecino ya está cerrado, no lo volvemos a evaluar
                
            # Calculamos cuánto nos costaría llegar a este vecino pasando por el nodo actual
            nueva_distancia = distancia_actual + peso_arista
            
            print(f"   Evaluando ruta hacia '{vecino}' (Costo del tramo: {peso_arista})")
            
            # Si esta nueva ruta es más barata/rápida que la mejor ruta que conocíamos antes...
            if nueva_distancia < distancias[vecino]:
                print(f"   * ¡NUEVO ATAJO ENCONTRADO! Mejoramos la ruta a '{vecino}'. "
                      f"Antes costaba {distancias[vecino]}, ahora cuesta {nueva_distancia}.")
                
                # Actualizamos nuestra tabla de distancias récord
                distancias[vecino] = nueva_distancia
                # Registramos que para llegar a este vecino, el mejor paso previo es el nodo actual
                padres[vecino] = nodo_actual
                
                # Añadimos este vecino a la cola de prioridades para evaluarlo en el futuro
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))
                
            else:
                print(f"   - La ruta conocida a '{vecino}' sigue siendo mejor o igual. Se descarta este camino.")
                
        # Una pequeña pausa artificial (0.5 seg) para que puedas leer la consola como si fuera una simulación en vivo
        time.sleep(0.5)

    # 4. RECONSTRUCCIÓN DEL CAMINO
    # Ahora que terminamos, leemos el diccionario de 'padres' de atrás hacia adelante
    ruta_optima = []
    nodo_rastreador = nodo_destino
    
    # Vamos saltando del destino hacia atrás hasta llegar al inicio
    while nodo_rastreador is not None:
        ruta_optima.append(nodo_rastreador)
        nodo_rastreador = padres[nodo_rastreador]
        
    # Como lo leímos al revés, volteamos la lista para que quede del inicio al fin
    ruta_optima.reverse()
    
    costo_total = distancias[nodo_destino]
    
    print("\n" + "="*50)
    print("RESULTADOS FINALES DE LA SIMULACIÓN")
    print("="*50)
    
    if distancias[nodo_destino] == float('inf'):
        print(f"ERROR: No existe un camino posible entre {nodo_inicio} y {nodo_destino}.")
        return None, float('inf')
    else:
        print(f"Ruta óptima encontrada: {' -> '.join(ruta_optima)}")
        print(f"Costo total (Tiempo/Distancia): {costo_total} unidades.")
        return ruta_optima, costo_total


def dibujar_grafo_resultado(grafo, ruta_optima):
    """
    Función que da los puntos extras. Dibuja el grafo en una ventana gráfica
    y resalta la ruta óptima encontrada por el simulador.
    """
    if not GRAFICOS_DISPONIBLES:
        print("\n[Aviso Gráfico] Las librerías 'networkx' y/o 'matplotlib' no están instaladas.")
        print("Para ver el dibujo de la planta, instala las librerías ejecutando en tu terminal:")
        print("pip install networkx matplotlib")
        return

    print("\nGenerando visualización gráfica de la planta...")
    
    # Creamos un objeto de Grafo de NetworkX
    G = nx.Graph()
    
    # Añadimos los nodos y aristas a partir de nuestro diccionario
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos.items():
            G.add_edge(nodo, vecino, weight=peso)
            
    # Usamos un algoritmo de resorte (spring_layout) para acomodar los nodos de forma bonita
    posiciones = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(10, 7))
    plt.title("Simulador de Enrutamiento Industrial (Algoritmo de Dijkstra)", fontsize=14, fontweight='bold')
    
    # 1. Dibujamos todos los nodos y conexiones de la planta en colores neutros
    nx.draw_networkx_nodes(G, posiciones, node_color='lightgray', node_size=2000, edgecolors='black')
    nx.draw_networkx_labels(G, posiciones, font_size=10, font_weight='bold')
    
    aristas_todas = G.edges()
    nx.draw_networkx_edges(G, posiciones, edgelist=aristas_todas, edge_color='gray', width=1.5, alpha=0.5)
    
    # Mostramos los pesos (distancia/tiempo) en cada arista
    etiquetas_pesos = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, posiciones, edge_labels=etiquetas_pesos, font_color='blue')
    
    # 2. Resaltamos la RUTA ÓPTIMA en color rojo intenso
    if ruta_optima:
        # Extraemos los pares de conexiones de nuestra ruta (Ej: [A->B, B->C])
        aristas_optimas = [(ruta_optima[i], ruta_optima[i+1]) for i in range(len(ruta_optima)-1)]
        
        # Pintamos los nodos de la ruta de verde
        nx.draw_networkx_nodes(G, posiciones, nodelist=ruta_optima, node_color='lightgreen', node_size=2000, edgecolors='black')
        
        # Pintamos el camino óptimo de rojo grueso
        nx.draw_networkx_edges(G, posiciones, edgelist=aristas_optimas, edge_color='red', width=4)
        
        # Pintamos el nodo de inicio y fin para distinguirlos
        nx.draw_networkx_nodes(G, posiciones, nodelist=[ruta_optima[0]], node_color='yellow', node_size=2500)
        nx.draw_networkx_nodes(G, posiciones, nodelist=[ruta_optima[-1]], node_color='orange', node_size=2500)

    # Quitamos los ejes cartesianos para que parezca un diagrama limpio
    plt.axis('off')
    plt.tight_layout()
    # Mostramos la ventana gráfica
    plt.show()


# ==========================================
# CONFIGURACIÓN DE LA FÁBRICA Y EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    
    # Definimos el mapa de nuestra planta industrial como un diccionario de diccionarios.
    # Los números representan el tiempo en minutos que tarda un robot (AGV) en recorrer ese pasillo.
    planta_industrial = {
        'Almacen': {'Corte': 5, 'Ensamblaje_A': 10},
        'Corte': {'Almacen': 5, 'Soldadura': 3, 'Pintura': 8},
        'Ensamblaje_A': {'Almacen': 10, 'Pintura': 2, 'Empaque': 7},
        'Soldadura': {'Corte': 3, 'Calidad': 4},
        'Pintura': {'Corte': 8, 'Ensamblaje_A': 2, 'Calidad': 6},
        'Calidad': {'Soldadura': 4, 'Pintura': 6, 'Empaque': 3},
        'Empaque': {'Ensamblaje_A': 7, 'Calidad': 3}
    }
    
    origen = 'Almacen'
    destino = 'Empaque'
    
    # 1. Ejecutamos el simulador en consola
    ruta_final, costo_final = simulador_dijkstra_consola(planta_industrial, origen, destino)
    
    # 2. Desplegamos el plano gráfico (Puntos extras)
    if ruta_final:
        dibujar_grafo_resultado(planta_industrial, ruta_final)
