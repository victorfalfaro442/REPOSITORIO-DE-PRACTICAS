import time

# Intentamos importar las librerías gráficas
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    GRAFICOS_DISPONIBLES = True
except ImportError:
    GRAFICOS_DISPONIBLES = False

# ==========================================
# ESTRUCTURA MAESTRA: UNION-FIND
# ==========================================
class UnionFind:
    """
    Estructura de datos 'Conjuntos Disjuntos'. 
    Es el cerebro de Kruskal. Le dice al algoritmo instantáneamente si dos máquinas 
    ya están conectadas por alguna ruta indirecta para evitar crear bucles inútiles.
    """
    def __init__(self, nodos):
        # Al inicio, cada máquina es su propio "jefe" (están desconectadas)
        self.padre = {nodo: nodo for nodo in nodos}
        # El rango ayuda a mantener el árbol equilibrado al unir conjuntos
        self.rango = {nodo: 0 for nodo in nodos}

    def buscar(self, nodo):
        """Encuentra al 'jefe supremo' del grupo al que pertenece este nodo."""
        if self.padre[nodo] != nodo:
            # Compresión de ruta: conecta los nodos directamente al jefe supremo para futuras búsquedas rápidas
            self.padre[nodo] = self.buscar(self.padre[nodo])
        return self.padre[nodo]

    def unir(self, nodo1, nodo2):
        """
        Intenta unir los grupos de dos nodos.
        Retorna True si la unión fue exitosa. Retorna False si ya pertenecían al mismo grupo (forma ciclo).
        """
        raiz1 = self.buscar(nodo1)
        raiz2 = self.buscar(nodo2)

        # Si tienen el mismo jefe, ya están conectados. ¡Peligro de bucle cerrado!
        if raiz1 == raiz2:
            return False

        # Si son de grupos distintos, los unimos basándonos en su rango (tamaño)
        if self.rango[raiz1] > self.rango[raiz2]:
            self.padre[raiz2] = raiz1
        elif self.rango[raiz1] < self.rango[raiz2]:
            self.padre[raiz1] = raiz2
        else:
            self.padre[raiz2] = raiz1
            self.rango[raiz1] += 1
            
        return True


# ==========================================
# ALGORITMO PRINCIPAL: KRUSKAL
# ==========================================
def simulador_kruskal_consola(nodos, aristas, tipo="minimo"):
    """
    Simula el algoritmo de Kruskal paso a paso.
    - tipo="minimo": Busca el costo más bajo (ej. ahorrar cables).
    - tipo="maximo": Busca el costo más alto (ej. maximizar ancho de banda).
    """
    print(f"\n--- INICIANDO SIMULACIÓN KRUSKAL ({tipo.upper()} COSTE) ---")
    
    # 1. ORDENAMIENTO
    # Si es mínimo, ordenamos de menor a mayor. Si es máximo, de mayor a menor (reverse=True).
    es_maximo = (tipo == "maximo")
    aristas_ordenadas = sorted(aristas, key=lambda x: x[2], reverse=es_maximo)
    
    print("Catálogo de conexiones ordenado por peso:")
    for o, d, p in aristas_ordenadas:
        print(f"   [{p} uds] {o} - {d}")
        
    time.sleep(1)
    print("\nIniciando evaluación de conexiones...")
    
    # Inicializamos nuestro detector de ciclos
    detector_ciclos = UnionFind(nodos)
    
    aristas_finales = []
    costo_total = 0
    paso = 1
    
    # 2. BUCLE DE EVALUACIÓN
    for origen, destino, peso in aristas_ordenadas:
        print(f"\nPaso {paso} -> Evaluando tramo: {origen} -- {destino} (Peso: {peso})")
        
        # Le preguntamos al Union-Find si podemos unir estas máquinas sin hacer un bucle
        if detector_ciclos.unir(origen, destino):
            print("   [APROBADO] Las máquinas estaban separadas. Se instala la conexión.")
            aristas_finales.append((origen, destino, peso))
            costo_total += peso
        else:
            print("   [RECHAZADO] Estas máquinas ya tienen una vía de comunicación. Instalar esto crearía un bucle redundante.")
            
        paso += 1
        time.sleep(0.5)
        
        # Optimización: Un Árbol Parcial siempre tiene exactamente (N - 1) conexiones.
        # Si ya llegamos a esa cantidad, la fábrica entera está conectada.
        if len(aristas_finales) == len(nodos) - 1:
            print("\n   ¡INFO: Se alcanzó la interconexión total de la planta! Se ignoran las conexiones restantes.")
            break

    # 3. RESULTADOS
    print("\n" + "="*50)
    print(f"RESULTADOS FINALES DEL DISEÑO DE RED ({tipo.upper()})")
    print("="*50)
    print(f"Acumulado total de la métrica (Peso): {costo_total}")
    print("Tramos instalados:")
    for o, d, p in aristas_finales:
        print(f"  * {o} <--> {d} ({p})")
        
    return aristas_finales


def dibujar_kruskal(nodos, aristas_totales, aristas_elegidas, tipo):
    """Genera la vista gráfica de la red optimizada."""
    if not GRAFICOS_DISPONIBLES:
        return

    print("\nGenerando plano interactivo de Kruskal...")
    G = nx.Graph()
    
    # Añadimos todos los nodos y la topología base
    for o, d, p in aristas_totales:
        G.add_edge(o, d, weight=p)
        
    posiciones = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 7))
    titulo = "Red Troncal de Datos (Ancho de Banda Máximo)" if tipo == "maximo" else "Red de Seguridad (Cableado Mínimo)"
    plt.title(f"Simulador Kruskal - {titulo}", fontsize=14, fontweight='bold')
    
    # Dibujar base
    nx.draw_networkx_nodes(G, posiciones, node_color='lightgray', node_size=2000, edgecolors='black')
    nx.draw_networkx_labels(G, posiciones, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, posiciones, edge_color='gray', style='dotted', alpha=0.5)
    
    etiquetas_pesos = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, posiciones, edge_labels=etiquetas_pesos, font_color='gray')
    
    # Resaltar la red de Kruskal
    if aristas_elegidas:
        enlaces = [(o, d) for o, d, p in aristas_elegidas]
        color_linea = 'purple' if tipo == "maximo" else 'green'
        
        nx.draw_networkx_nodes(G, posiciones, node_color='lightyellow', node_size=2000, edgecolors='black')
        nx.draw_networkx_edges(G, posiciones, edgelist=enlaces, edge_color=color_linea, width=4)

    plt.axis('off')
    plt.tight_layout()
    plt.show()


# ==========================================
# CONFIGURACIÓN DE LA FÁBRICA Y EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    # Lista de máquinas en la planta
    maquinas = ['Servidor', 'Ensamblaje', 'Soldadura', 'Pintura', 'Empaque', 'Almacen']
    
    # Todas las canaletas disponibles para pasar cables y su capacidad en Gbps (Gigabits por segundo)
    # Formato: (Origen, Destino, Capacidad_Gbps)
    conexiones_disponibles = [
        ('Servidor', 'Ensamblaje', 10),
        ('Servidor', 'Pintura', 100),    # Cable súper rápido
        ('Servidor', 'Almacen', 25),
        ('Ensamblaje', 'Soldadura', 50),
        ('Ensamblaje', 'Pintura', 15),
        ('Soldadura', 'Empaque', 40),
        ('Pintura', 'Empaque', 10),      # Cable muy lento y viejo
        ('Pintura', 'Almacen', 60),
        ('Empaque', 'Almacen', 20)
    ]
    
    # Para el ejemplo, simularemos un diseño de MÁXIMO COSTE.
    # El objetivo es interconectar todos los nodos priorizando las conexiones de mayor Gbps
    # para tener la red más rápida posible sin crear bucles en el switch de red.
    modo = "maximo" # Cambia esto a "minimo" si deseas probar el comportamiento inverso
    
    rutas_instaladas = simulador_kruskal_consola(maquinas, conexiones_disponibles, tipo=modo)
    dibujar_kruskal(maquinas, conexiones_disponibles, rutas_instaladas, tipo=modo)
