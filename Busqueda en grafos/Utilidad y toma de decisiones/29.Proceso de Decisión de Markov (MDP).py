import random

print("--- INICIANDO Q-LEARNING (APRENDIZAJE POR REFUERZO) ---")

# 1. EL ENTORNO OCULTO (La IA no puede ver estas probabilidades)
estados = ['Inicio', 'Hielo', 'Tesoro', 'Trampa']
acciones = ['Avanzar', 'Retroceder']
estados_terminales = ['Tesoro', 'Trampa']

def dar_un_paso(estado, accion):
    """El 'Motor Físico' del universo. La IA llama a esto y reza."""
    if estado == 'Inicio':
        if accion == 'Avanzar':
            if random.random() < 0.9: return 'Hielo', -1
            else: return 'Inicio', -1
        else: return 'Inicio', -1
            
    elif estado == 'Hielo':
        if accion == 'Avanzar':
            if random.random() < 0.7: return 'Tesoro', 100
            else: return 'Trampa', -100
        else: return 'Inicio', -1
    
    return estado, 0 # Fallback

# 2. EL CEREBRO DE LA IA (La Tabla Q)
# Empieza totalmente en blanco (ceros)
Q = {s: {a: 0.0 for a in acciones} for s in estados}

# 3. HIPERPARÁMETROS DEL APRENDIZAJE
alfa = 0.1      # Tasa de aprendizaje (qué tanto caso hace a la nueva info)
gamma = 0.9     # Factor de descuento (visión a largo plazo)
epsilon = 0.2   # Probabilidad de explorar a lo loco (20% del tiempo)
episodios = 1000 # Cuántas "vidas" jugará la IA para aprender

# 4. EL BUCLE DE ENTRENAMIENTO
for episodio in range(1, episodios + 1):
    estado_actual = 'Inicio' # La IA siempre reaparece aquí
    
    while estado_actual not in estados_terminales:
        # A) Exploración vs Explotación
        # El 20% de las veces elige al azar, el 80% elige lo mejor que sabe
        if random.random() < epsilon:
            accion_elegida = random.choice(acciones) # Modo Explorador
        else:
            # Modo Explotador: Elige la acción con el Q-Value más alto
            accion_elegida = max(Q[estado_actual], key=Q[estado_actual].get)
            
        # B) La IA ejecuta la acción en el mundo real
        nuevo_estado, recompensa = dar_un_paso(estado_actual, accion_elegida)
        
        # C) Aprende de lo que acaba de pasar (Ecuación de Actualización Q)
        # Busca cuál sería su mejor jugada en el estado al que acaba de llegar
        mejor_q_futura = max(Q[nuevo_estado].values()) if nuevo_estado not in estados_terminales else 0.0
        
        # Actualiza su creencia sobre el estado y acción anteriores
        valor_viejo = Q[estado_actual][accion_elegida]
        temporal_difference = recompensa + (gamma * mejor_q_futura) - valor_viejo
        
        Q[estado_actual][accion_elegida] = valor_viejo + (alfa * temporal_difference)
        
        # D) Avanza al siguiente paso
        estado_actual = nuevo_estado
        
    if episodio % 250 == 0:
        print(f"[*] Entrenamiento: {episodio}/{episodios} vidas completadas...")

# 5. RESULTADOS DEL APRENDIZAJE
print("\n" + "="*50)
print(" CEREBRO FINAL DE LA IA (TABLA Q) ")
print("="*50)
for s in ['Inicio', 'Hielo']:
    print(f"En '{s}':")
    for a in acciones:
        print(f"  - Si decide {a.upper()} -> Calidad (Q): {Q[s][a]:.2f}")

print("\n--- LA POLÍTICA DESCUBIERTA A GOLPES ---")
for s in ['Inicio', 'Hielo']:
    mejor_accion = max(Q[s], key=Q[s].get)
    print(f"Si estoy en '{s}' -> El instinto me dice que debo: {mejor_accion.upper()}")