import random

print("--- INICIANDO ENTRENAMIENTO Q-LEARNING ---")

# 1. PREPARACIÓN DEL ENTORNO Y DEL CEREBRO DE LA IA
estados = ['Inicio', 'Hielo', 'Tesoro', 'Trampa']
acciones = ['Avanzar', 'Retroceder']
estados_terminales = ['Tesoro', 'Trampa']

def dar_un_paso(estado, accion):
    """El universo físico oculto (Mismo código que ya analizamos)"""
    if estado == 'Inicio':
        if accion == 'Avanzar': return ('Hielo', -1) if random.random() < 0.9 else ('Inicio', -1)
        else: return ('Inicio', -1)
    elif estado == 'Hielo':
        if accion == 'Avanzar': return ('Tesoro', 100) if random.random() < 0.7 else ('Trampa', -100)
        else: return ('Inicio', -1)
    return (estado, 0)

# La Tabla Q es el "Cerebro". Es un diccionario dentro de un diccionario.
# Inicialmente, la IA no sabe nada, así que todos los valores (Calidad) son 0.0.
Q = {s: {a: 0.0 for a in acciones} for s in estados}

# 2. HIPERPARÁMETROS (La personalidad de la IA)
alfa = 0.1      # Tasa de aprendizaje: ¿Qué tanto peso le da a la nueva experiencia frente a la memoria vieja? (10%)
gamma = 0.9     # Factor de descuento: ¿Qué tanto le importa el futuro frente a la recompensa inmediata? (90%)
epsilon = 0.2   # Tasa de exploración: 20% de las veces ignorará su conocimiento y elegirá al azar para descubrir cosas nuevas.
episodios = 1500 # Cuántas "vidas" jugará para aprender.

# 3. EL BUCLE PRINCIPAL DE APRENDIZAJE
for episodio in range(1, episodios + 1):
    
    # En cada nueva vida, la IA reaparece en la casilla de inicio.
    estado_actual = 'Inicio'
    
    # El juego continúa hasta que la IA caiga en una trampa o encuentre el tesoro.
    while estado_actual not in estados_terminales:
        
        # ------------------------------------------------------
        # FASE A: ELEGIR UNA ACCIÓN (Exploración vs Explotación)
        # ------------------------------------------------------
        # Tiramos un dado decimal (de 0.0 a 1.0). Si cae en ese 20% (epsilon)...
        if random.random() < epsilon:
            # Elige 'Avanzar' o 'Retroceder' tirando una moneda al aire.
            accion = random.choice(acciones) 
        else:
            # Revisa su cerebro (Tabla Q) para el estado actual.
            # Usa max() para encontrar la acción que actualmente tiene el puntaje más alto.
            accion = max(Q[estado_actual], key=Q[estado_actual].get)
            
        # ------------------------------------------------------
        # FASE B: EJECUTAR LA ACCIÓN Y OBSERVAR EL UNIVERSO
        # ------------------------------------------------------
        # La IA envía su acción al universo y recibe su nuevo paradero y los puntos ganados/perdidos.
        nuevo_estado, recompensa = dar_un_paso(estado_actual, accion)
        
        # ------------------------------------------------------
        # FASE C: APRENDIZAJE MATEMÁTICO (Actualizar la Tabla Q)
        # ------------------------------------------------------
        # 1. ¿Cuál es el máximo premio posible al que puedo aspirar desde mi nuevo estado?
        if nuevo_estado in estados_terminales:
            # Si llegué al final, el futuro ya no existe, el valor esperado es 0.
            mejor_q_futura = 0.0 
        else:
            # Revisa la Tabla Q del nuevo_estado y extrae el valor más alto posible.
            # Asume que tomará esa ruta perfecta, incluso si luego el "epsilon" la hace tropezar.
            mejor_q_futura = max(Q[nuevo_estado].values()) 
            
        # 2. Rescatamos lo que la IA "creía" que valía la acción que acaba de hacer.
        valor_viejo = Q[estado_actual][accion]
        
        # 3. Calculamos la Diferencia Temporal (El error de predicción):
        # Es la Recompensa Real + (Visión a futuro descontada) - Lo que creíamos antes
        error_prediccion = recompensa + (gamma * mejor_q_futura) - valor_viejo
        
        # 4. Actualizamos el cerebro sumando una fracción (alfa) de ese error al valor viejo.
        Q[estado_actual][accion] = valor_viejo + (alfa * error_prediccion)
        
        # ------------------------------------------------------
        # FASE D: AVANZAR EL TIEMPO
        # ------------------------------------------------------
        # El nuevo estado se convierte en el estado actual para la siguiente vuelta del bucle.
        estado_actual = nuevo_estado

    # Imprimimos el progreso cada cierto tiempo para no saturar la consola.
    if episodio % 300 == 0:
        print(f"[*] Completadas {episodio} vidas. El cerebro se está ajustando...")

# 4. RESULTADOS (El cerebro terminado)
print("\n" + "="*50)
print(" CEREBRO FINAL: VALORES Q APRENDIDOS ")
print("="*50)
for s in ['Inicio', 'Hielo']:
    print(f"Estando en la casilla '{s}':")
    for a in acciones:
        print(f"  -> Si hace '{a}', espera una calidad de: {Q[s][a]:.2f}")

print("\n--- LA MEJOR ESTRATEGIA ENCONTRADA ---")
# Una vez entrenada la IA, ya no necesitamos "epsilon". Solo lee los máximos.
for s in ['Inicio', 'Hielo']:
    mejor_accion = max(Q[s], key=Q[s].get)
    print(f"Si despierta en '{s}' -> Debe {mejor_accion.upper()}")
