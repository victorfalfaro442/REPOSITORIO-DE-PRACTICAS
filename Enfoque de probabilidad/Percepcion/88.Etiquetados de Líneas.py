print("--- PERCEPCIÓN 3D: ETIQUETADO DE LÍNEAS (HUFFMAN-CLOWES) ---")

# ==============================================================
# 1. EL DICCIONARIO DE LA FÍSICA (Catálogo de uniones válidas)
# ==============================================================
# Definimos qué combinaciones de etiquetas (+, -, >) son posibles.
# Las tuplas representan el estado de las líneas que llegan al vértice.

uniones_validas = {
    # Vértice tipo "Y" (Ej. la esquina más cercana de un cubo)
    # Solo hay 5 formas físicas en las que 3 planos pueden unirse en "Y"
    'Y': [
        ('+', '+', '+'),  # Esquina convexa (sale hacia ti)
        ('-', '-', '-'),  # Esquina cóncava (rincón de una caja)
        ('>', '>', '-'),  # Borde de oclusión con un pliegue cóncavo
        ('-', '>', '>'),
        ('>', '-', '>')
    ],
    
    # Vértice tipo "Flecha" (Ej. los bordes exteriores de un cubo)
    # Solo hay 3 formas físicas posibles
    'Flecha': [
        ('-', '+', '-'),  # Pliegue interior
        ('>', '+', '>'),  # Borde externo convexo
        ('>', '-', '>')   # Borde externo cóncavo
    ]
}

# ==============================================================
# 2. EL ALGORITMO DE SATISFACCIÓN DE RESTRICCIONES (Evaluador)
# ==============================================================
def evaluar_vertice(tipo_vertice, etiquetas_propuestas):
    """
    Revisa si una combinación de líneas tiene sentido en el mundo 3D.
    """
    if tipo_vertice not in uniones_validas:
        return False, "Tipo de vértice desconocido."
        
    # Verificamos si la propuesta existe en nuestro diccionario de realidad
    if etiquetas_propuestas in uniones_validas[tipo_vertice]:
        return True, "¡Válido! Esta geometría puede existir en el mundo 3D."
    else:
        return False, "¡Imposible! Esto desafía la física (Figura a lo M.C. Escher)."

# ==============================================================
# 3. PRUEBAS CON FIGURAS
# ==============================================================
print("\n[*] Evaluando geometrías propuestas por el sistema de visión...")

# Prueba 1: La esquina frontal de un cubo (Tres líneas convexas)
etiquetas_cubo_frontal = ('+', '+', '+')
es_valido, mensaje = evaluar_vertice('Y', etiquetas_cubo_frontal)
print(f"\n[Prueba 1] Vértice 'Y' con {etiquetas_cubo_frontal}:")
print(f"-> {mensaje}")

# Prueba 2: Un error del detector de aristas o una ilusión óptica
# Proponemos una 'Y' donde dos líneas salen y una se hunde
etiquetas_ilusion = ('+', '+', '-')
es_valido, mensaje = evaluar_vertice('Y', etiquetas_ilusion)
print(f"\n[Prueba 2] Vértice 'Y' con {etiquetas_ilusion}:")
print(f"-> {mensaje}")

# Prueba 3: El borde exterior de una caja
etiquetas_borde_caja = ('>', '+', '>')
es_valido, mensaje = evaluar_vertice('Flecha', etiquetas_borde_caja)
print(f"\n[Prueba 3] Vértice 'Flecha' con {etiquetas_borde_caja}:")
print(f"-> {mensaje}")
