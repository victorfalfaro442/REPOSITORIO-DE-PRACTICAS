import heapq
import time

# Intentamos importar las librerías gráficas para el plano de la fábrica.
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    GRAFICOS_DISPONIBLES = True
except ImportError:
    GRAFICOS_DISPONIBLES = False


def simulador_prim_consola(grafo, nodo_inicio):
    """
    Simulador paso a paso del Algoritmo de Prim.
    Encuentra el Árbol de Expansión Mínima (MST) para conectar toda la red al menor costo.
    """
    print(f"\n[{nodo_inicio}] --- INICIANDO SIMULACIÓN DE PRIM (Tendido de Red) ---")
    
    # 1. INICIALIZACIÓN
    # Llevamos un registro de los nodos que ya conectamos a nuestra red.
    # Empezamos solo con el nodo base (Ej. El compresor principal).
    nodos_conectados = set([nodo_inicio])
    
    # Aquí guardaremos las tuberías definitivas que sí vamos a instalar
    aristas_mst = []
    costo_total_red = 0
    
    # La "cola de prioridad" (Min-Heap) guardará todas las opciones de conexión posibles
    # desde los nodos que ya tenemos en la red hacia los que aún no están.
    # Formato: (Costo, Nodo_Origen, Nodo_Destino)
    opciones_conexion = []
    
    # Revisamos las conexiones disponibles desde el nodo de inicio y las metemos al heap
    for vecino, costo in grafo[nodo_inicio].items():
        heapq.heappush(opciones_conexion, (costo, nodo_inicio, vecino))
        
    paso = 1
    total_nodos = len(grafo)

    # 2. BUCLE PRINCIPAL DE EXPANSIÓN
    # El algoritmo termina cuando hemos conectado todos los nodos de la fábrica
    while len(nodos_conectados) < total_nodos and opciones_conexion:
        
        # Extraemos la conexión MÁS BARATA disponible en todo el borde de nuestra red
        costo_actual, origen, destino = heapq.heappop(opciones_conexion)
        
        # REGLA DE ORO DE PRIM: Evitar ciclos.
        # Si el destino ya está conectado a la red, ignoramos esta tubería para no gastar material a lo tonto.
        if destino in nodos_conectados:
            continue
            
        # Si el destino no estaba conectado, ¡lo agregamos a la red!
        print(f"\n--- PASO {paso} ---")
        print(f"-> Conectando: '{origen}' con '{destino}'")
        print(f"   Metros de tubería utilizados: {costo_actual}")
        
        # Registramos la conexión
        nodos_conectados.add(destino)
        aristas_mst.append((origen, destino, costo_actual))
        costo_total_red += costo_actual
        paso += 1
        
        # Como acabamos de integrar un nuevo nodo ('destino') a la red,
        # ahora tenemos acceso a nuevas rutas desde ese nodo. Las evaluamos:
        for nuevo_vecino, nuevo_costo in grafo[destino].items():
            # Solo agregamos las rutas hacia nodos que AÚN NO están en la red
            if nuevo_vecino not in nodos_conectados:
                heapq.heappush(opciones_conexion, (nuevo_costo, destino, nuevo_vecino))
                
        # Pequeña pausa para que el texto fluya como una simulación
        time.sleep(0.5)

    # 3. RESULTADOS FINALES
    print("\n" + "="*50)
    print("RESULTADOS DE LA INSTALACIÓN DE LA RED")
    print("="*50)
    
    if len(nodos_conectados) < total_nodos:
        print("ERROR: El diseño de la planta está fragmentado. No se pudieron conectar todas las máquinas.")
    else:
        print("¡Red neumática instalada con éxito en toda la planta!")
        print(f"Total de tubería utilizada: {costo_total_red} metros.")
        print("Conexiones realizadas:")
        for o, d, c in aristas_mst:
            print(f"  * {o} <--> {d} ({c}m)")
            
    return aristas_mst, costo_total_red


def dibujar_arbol_prim(grafo, aristas_mst):
    """
    Función para visualizar el plano de la fábrica.
    Dibuja todas las conexiones posibles en gris y resalta el Árbol Mínimo (MST) en azul grueso.
    """
    if not GRAFICOS_DISPONIBLES:
        return

    print("\nGenerando plano de instalación de red...")
    
    G = nx.Graph()
    
    # Construimos el grafo completo con todas las opciones
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos.items():
            G.add_edge(nodo, vecino, weight=peso)
            
    # Algoritmo para posicionar los nodos estéticamente
    posiciones = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(10, 7))
    plt.title("Plano de Instalación (Algoritmo de Prim - Árbol Parcial Mínimo)", fontsize=14, fontweight='bold')
    
    # 1. Dibujamos el escenario base (Todas las rutas posibles en gris claro)
    nx.draw_networkx_nodes(G, posiciones, node_color='lightgray', node_size=2000, edgecolors='black')
    nx.draw_networkx_labels(G, posiciones, font_size=10, font_weight='bold')
    
    todas_las_aristas = G.edges()
    nx.draw_networkx_edges(G, posiciones, edgelist=todas_las_aristas, edge_color='lightgray', style='dashed', width=1.5)
    
    etiquetas_pesos = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, posiciones, edge_labels=etiquetas_pesos, font_color='gray')
    
    # 2. Resaltamos las conexiones elegidas por el Algoritmo de Prim (La red instalada)
    if aristas_mst:
        # Extraemos solo los pares de nodos elegidos
        enlaces_red = [(o, d) for o, d, c in aristas_mst]
        
        # Pintamos los nodos ya conectados de un color vivo
        nx.draw_networkx_nodes(G, posiciones, node_color='lightblue', node_size=2000, edgecolors='black')
        
        # Dibujamos las tuberías definitivas con líneas azules gruesas
        nx.draw_networkx_edges(G, posiciones, edgelist=enlaces_red, edge_color='blue', width=4)

    plt.axis('off')
    plt.tight_layout()
    plt.show()


# ==========================================
# CONFIGURACIÓN DE LA FÁBRICA Y EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    
    # Plano de distancias (en metros) entre las máquinas de la nave industrial.
    # Al ser un grafo no dirigido (las tuberías van en ambas direcciones), 
    # las conexiones son simétricas.
    planta_red = {
        'Compresor_Principal': {'Robot_Soldadura': 12, 'Prensa_Hidraulica': 25},
        'Robot_Soldadura': {'Compresor_Principal': 12, 'Prensa_Hidraulica': 9, 'Brazo_Pintura': 18},
        'Prensa_Hidraulica': {'Compresor_Principal': 25, 'Robot_Soldadura': 9, 'Brazo_Pintura': 14, 'Banda_Transporte': 22},
        'Brazo_Pintura': {'Robot_Soldadura': 18, 'Prensa_Hidraulica': 14, 'Banda_Transporte': 8, 'Ensamblaje_Final': 15},
        'Banda_Transporte': {'Prensa_Hidraulica': 22, 'Brazo_Pintura': 8, 'Ensamblaje_Final': 11},
        'Ensamblaje_Final': {'Brazo_Pintura': 15, 'Banda_Transporte': 11}
    }
    
    # Iniciamos la red desde el nodo que genera la energía/aire
    inicio_red = 'Compresor_Principal'
    
    # 1. Ejecutamos la simulación paso a paso en consola
    rutas_definitivas, costo_total = simulador_prim_consola(planta_red, inicio_red)
    
    # 2. Mostramos el plano gráfico (Puntos extras)
    dibujar_arbol_prim(planta_red, rutas_definitivas)
