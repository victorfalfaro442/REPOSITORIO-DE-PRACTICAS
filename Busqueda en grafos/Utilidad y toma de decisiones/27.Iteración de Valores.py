import copy

print("--- INICIANDO ALGORITMO DE ITERACIÓN DE VALORES ---")

# Lista de estados posibles
estados = ['Inicio', 'Hielo', 'Tesoro', 'Trampa']

# Recompensas inmediatas R(s) por pisar cada estado.
recompensas = {
    'Inicio': -1,
    'Hielo': -1,
    'Tesoro': 100,  # Estado Terminal Ganador
    'Trampa': -100  # Estado Terminal Perdedor
}

# Estados donde el juego se acaba 
estados_terminales = ['Tesoro', 'Trampa']

# Las acciones que la IA puede intentar
acciones = ['Avanzar', 'Retroceder']

# El Modelo de Transición P(s' | s, a)
# Formato: transiciones[estado_actual][accion] = [(probabilidad, estado_destino), ...]
transiciones = {
    'Inicio': {
        # Si avanza desde Inicio, 90% llega al Hielo, 10% tropieza y se queda en Inicio
        'Avanzar': [(0.9, 'Hielo'), (0.1, 'Inicio')],
        # Si retrocede, se choca con la pared y se queda en Inicio 100%
        'Retroceder': [(1.0, 'Inicio')]
    },
    'Hielo': {
        # ¡Peligro! Si avanza desde el Hielo, 70% llega al Tesoro, pero 30% resbala a la Trampa
        'Avanzar': [(0.7, 'Tesoro'), (0.3, 'Trampa')],
        # Si se asusta y retrocede, vuelve al Inicio a salvo (100%)
        'Retroceder': [(1.0, 'Inicio')]
    }
}

# Gamma (Factor de descuento). 
gamma = 0.9

# Epsilon (Umbral de convergencia). Cuando los cambios sean menores a esto, nos detenemos.
epsilon = 0.001

def iteracion_de_valores():
    # Paso A: Inicializamos las utilidades de todos los estados en 0
    U = {estado: 0.0 for estado in estados}
    
    iteracion = 0
    
    # Bucle infinito hasta que el mapa converja
    while True:
        delta = 0 # Reiniciamos el medidor de cambios para esta iteración
        U_nueva = copy.deepcopy(U) # Copia de trabajo para la Ecuación de Bellman
        
        print(f"\n[Iteración {iteracion}] Valores actuales: " + 
              ", ".join([f"{k}: {v:.2f}" for k,v in U.items()]))
        
        # Iteramos sobre cada estado del tablero
        for s in estados:
            # Paso B: Si el estado es terminal, su utilidad es fija (es su recompensa)
            if s in estados_terminales:
                U_nueva[s] = recompensas[s]
                continue
            
            # Paso C: Evaluamos todas las acciones posibles para encontrar la mejor
            max_utilidad_esperada = float('-inf')
            
            for a in acciones:
                utilidad_esperada_accion = 0
                
                # Sumamos: Probabilidad * Utilidad del estado destino
                for probabilidad, s_destino in transiciones[s][a]:
                    utilidad_esperada_accion += probabilidad * U[s_destino]
                    
                # Si esta acción es mejor que las que hemos revisado, la guardamos
                if utilidad_esperada_accion > max_utilidad_esperada:
                    max_utilidad_esperada = utilidad_esperada_accion
                    
            # Paso D: Aplicamos la Ecuación de Bellman Completa
            # U(s) = R(s) + gamma * MAX(Utilidad_Esperada)
            nuevo_valor = recompensas[s] + (gamma * max_utilidad_esperada)
            U_nueva[s] = nuevo_valor
            
            # Paso E: Calculamos la diferencia entre el valor viejo y el nuevo
            cambio_en_este_estado = abs(nuevo_valor - U[s])
            
            # Actualizamos delta si este es el cambio más grande de toda la iteración
            if cambio_en_este_estado > delta:
                delta = cambio_en_este_estado
                
        # Actualizamos la tabla maestra con los nuevos valores calculados
        U = U_nueva
        iteracion += 1
        
        # Paso F: Condición de Parada. Si los números apenas cambiaron, hemos terminado.
        if delta < epsilon:
            print(f"\n[*] CONVERGENCIA ALCANZADA en la iteración {iteracion}.")
            break
            
    return U

utilidades_finales = iteracion_de_valores()

print("\n" + "="*50)
print(" RESULTADO: UTILIDADES FINALES DEL MAPA ")
print("="*50)
for estado, valor in utilidades_finales.items():
    print(f" Estado '{estado}': {valor:.2f} puntos")

print("\n--- LA POLÍTICA ÓPTIMA (Qué debe hacer la IA) ---")
# Una vez tenemos las utilidades, la IA sabe exactamente qué hacer mirando a su alrededor
for s in estados:
    if s in estados_terminales:
        print(f" En '{s}': FIN DEL JUEGO.")
        continue
        
    mejor_accion = None
    mejor_valor = float('-inf')
    
    for a in acciones:
        valor_accion = 0
        for prob, s_destino in transiciones[s][a]:
            valor_accion += prob * utilidades_finales[s_destino]
            
        if valor_accion > mejor_valor:
            mejor_valor = valor_accion
            mejor_accion = a
            
    print(f" Si estoy en '{s}' -> Lo más inteligente es: {mejor_accion.upper()}")