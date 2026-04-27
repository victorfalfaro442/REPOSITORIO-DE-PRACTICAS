import random

print("--- APRENDIZAJE POR REFUERZO ACTIVO (SARSA) ---")

# 1. EL ENTORNO 
estados = ['Inicio', 'Hielo', 'Tesoro', 'Trampa']
acciones = ['Avanzar', 'Retroceder']
estados_terminales = ['Tesoro', 'Trampa']

def dar_un_paso(estado, accion):
    """
    Simula la transición del entorno.
    Recibe:
        - estado (str): La casilla donde se encuentra la IA actualmente.
        - accion (str): La acción que la IA intenta realizar ('Avanzar' o 'Retroceder').
    Devuelve:
        - Una tupla (nuevo_estado, recompensa_inmediata)
    """
    if estado == 'Inicio':
        
        # Si la IA intenta ir hacia adelante...
        if accion == 'Avanzar': 
            # random.random() genera un decimal aleatorio entre 0.0 y 1.0.
            # - Si sale menos de 0.9 (90% de éxito), la IA llega al 'Hielo' y gasta 1 de energía (-1).
            # - Si sale 0.9 o más (10% de fracaso), la IA tropieza, se queda en 'Inicio' y gasta 1 de energía.
            return ('Hielo', -1) if random.random() < 0.9 else ('Inicio', -1)
            
        # Si la IA intenta 'Retroceder' (u otra acción que no sea avanzar)...
        else: 
            # Como no hay nada detrás del inicio, choca con la pared.
            # Se queda en 'Inicio' y el esfuerzo le cuesta 1 punto de energía (-1).
            return ('Inicio', -1)
            
    elif estado == 'Hielo':
        
        # Si la IA es valiente e intenta ir hacia adelante...
        if accion == 'Avanzar': 
            # - 70% de probabilidad (< 0.7) de cruzar con éxito y llegar al 'Tesoro' (Premio: +100).
            # - 30% de probabilidad (>= 0.7) de resbalar en el hielo y caer en la 'Trampa' (Castigo: -100).
            return ('Tesoro', 100) if random.random() < 0.7 else ('Trampa', -100)
            
        # Si la IA es precavida e intenta 'Retroceder'...
        else: 
            # Vuelve a la casilla segura de 'Inicio' al 100% de probabilidad.
            # Solo pierde 1 punto de energía (-1) por el esfuerzo de moverse.
            return ('Inicio', -1)
        
    # Si la función es llamada y la IA ya estaba en 'Tesoro' o 'Trampa',
    # el juego ya ha terminado. No puede moverse a ningún lado ni ganar más puntos.
    return (estado, 0)

# 2. EL CEREBRO DE LA IA (Tabla Q vacía)
Q = {s: {a: 0.0 for a in acciones} for s in estados}

# Hiperparámetros
alfa = 0.1      # Tasa de aprendizaje
gamma = 0.9     # Factor de descuento
epsilon = 0.2   # 20% de las veces explora al azar
episodios = 1500

def elegir_accion(estado):
    """Política Épsilon-Codiciosa: El motor de la Exploración vs Explotación"""
    if random.random() < epsilon:
        return random.choice(acciones) # Exploración ciega
    else:
        # Explotación: Elige la acción con mayor valor Q
        return max(Q[estado], key=Q[estado].get)

# 3. EL BUCLE DE ENTRENAMIENTO SARSA
for episodio in range(1, episodios + 1):
    estado_actual = 'Inicio'
    
    # En SARSA, elegimos la acción ANTES de entrar al bucle o evaluar
    accion_actual = elegir_accion(estado_actual)
    
    while estado_actual not in estados_terminales:
        # S-A-R-S: Ejecutamos la acción y vemos qué pasa
        nuevo_estado, recompensa = dar_un_paso(estado_actual, accion_actual)
        
        # A: Elegimos la SIGUIENTE acción desde el nuevo estado (esto es clave en SARSA)
        if nuevo_estado in estados_terminales:
            nueva_accion = None
            valor_q_futuro = 0.0
        else:
            nueva_accion = elegir_accion(nuevo_estado)
            valor_q_futuro = Q[nuevo_estado][nueva_accion] # No usamos MAX, usamos la acción real elegida
            
        # ACTUALIZACIÓN MATEMÁTICA (La Ecuación SARSA)
        valor_viejo = Q[estado_actual][accion_actual]
        diferencia_temporal = recompensa + (gamma * valor_q_futuro) - valor_viejo
        
        Q[estado_actual][accion_actual] = valor_viejo + (alfa * diferencia_temporal)
        
        # Avanzamos al siguiente paso de tiempo
        estado_actual = nuevo_estado
        accion_actual = nueva_accion # Mantenemos la acción que ya decidimos

    if episodio % 300 == 0:
        print(f"[*] Entrenamiento: {episodio}/{episodios} vidas completadas...")

# 4. RESULTADOS FINALES
print("\n" + "="*50)
print(" CEREBRO FINAL DE LA IA (TABLA Q APRENDIDA CON SARSA) ")
print("="*50)
for s in ['Inicio', 'Hielo']:
    print(f"En '{s}':")
    for a in acciones:
        print(f"  - Si decide {a.upper()} -> Calidad (Q): {Q[s][a]:.2f}")

print("\n--- LA POLÍTICA DESCUBIERTA ---")
for s in ['Inicio', 'Hielo']:
    mejor_accion = max(Q[s], key=Q[s].get)
    print(f"Si estoy en '{s}' -> El instinto me dice que debo: {mejor_accion.upper()}")
