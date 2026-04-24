print("--- INICIANDO RASTREADOR POMDP (ESTADO DE CREENCIA) ---")

# 1. EL ENTORNO
estados = ['Casilla_1', 'Casilla_2', 'Casilla_3'] # La puerta está en la Casilla_2

# 2. MODELO DE TRANSICIÓN P(s' | s, a)
# Si el robot intenta moverse a la Derecha, tiene 90% de éxito y 10% de resbalar y no moverse.
def transicion(estado_origen, accion):
    if accion == 'Derecha':
        if estado_origen == 'Casilla_1': return {'Casilla_2': 0.9, 'Casilla_1': 0.1}
        if estado_origen == 'Casilla_2': return {'Casilla_3': 0.9, 'Casilla_2': 0.1}
        if estado_origen == 'Casilla_3': return {'Casilla_3': 1.0} # Choca con el final
    return {estado_origen: 1.0}

# 3. MODELO DE OBSERVACIÓN O(o | s)
# El sensor trata de detectar la puerta (que solo está en la Casilla 2).
def probabilidad_observacion(observacion, estado_real):
    if estado_real == 'Casilla_2':
        # En la puerta, el sensor es 80% preciso
        if observacion == 'Veo_Puerta': return 0.8
        else: return 0.2
    else:
        if observacion == 'Veo_Pared': return 0.9
        else: return 0.1

# 4. INICIALIZACIÓN DEL ESTADO DE CREENCIA b(s)
creencia = {s: 1.0/len(estados) for s in estados}

def actualizar_creencia(creencia_actual, accion, observacion_del_sensor):
    creencia_nueva = {s: 0.0 for s in estados}
    
    # Aplicamos la Ecuación del POMDP
    for estado_destino in estados:
        
        # PASO 1: Predicción (¿A dónde creo que llegué por haberme movido?)
        prob_llegar_a_este_estado = 0
        for estado_origen in estados:
            prob_transicion = transicion(estado_origen, accion).get(estado_destino, 0.0)
            prob_llegar_a_este_estado += prob_transicion * creencia_actual[estado_origen]
            
        # PASO 2: Corrección (¿Qué dice mi sensor sobre este estado?)
        prob_sensor = probabilidad_observacion(observacion_del_sensor, estado_destino)
        
        # Multiplicamos ambas probabilidades
        creencia_nueva[estado_destino] = prob_sensor * prob_llegar_a_este_estado
        
    # PASO 3: Normalización (Alfa)
    suma_total = sum(creencia_nueva.values())
    for s in estados:
        creencia_nueva[s] /= suma_total
        
    return creencia_nueva

# --- SIMULACIÓN DEL ROBOT EN EL PASILLO ---

def imprimir_creencia(paso, c):
    print(f"\n[Paso {paso}] Mapa mental del robot:")
    for s, prob in c.items():
        barra = "█" * int(prob * 20)
        print(f"  {s}: {prob*100:05.2f}% | {barra}")

imprimir_creencia(0, creencia)

# El robot decide moverse a la derecha, y su sensor le dice "Veo una Pared"
accion = 'Derecha'
observacion = 'Veo_Pared'
print(f"\n[*] El robot intenta moverse a la '{accion}'...")
print(f"[*] Beep boop. El sensor reporta: '{observacion}'")

creencia = actualizar_creencia(creencia, accion, observacion)
imprimir_creencia(1, creencia)

# El robot se mueve a la derecha otra vez, ¡y ahora el sensor detecta la puerta!
accion = 'Derecha'
observacion = 'Veo_Puerta'
print(f"\n[*] El robot intenta moverse a la '{accion}'...")
print(f"[*] Beep boop. El sensor reporta: '{observacion}'")

creencia = actualizar_creencia(creencia, accion, observacion)
imprimir_creencia(2, creencia)