print("--- INICIANDO RED BAYESIANA DINÁMICA (DBN) ---")

# 1. DEFINICIÓN DEL ESTADO
# Nuestro estado oculto es una combinación de (Lluvia, Viento)
# Pueden ser: (True, True), (True, False), (False, True), (False, False)

# 2. EL MODELO DE TRANSICIÓN P(X_t | X_{t-1})
def prob_transicion(lluvia_hoy, viento_hoy, lluvia_ayer, viento_ayer):
    # Probabilidad de lluvia hoy depende de la lluvia de ayer
    if lluvia_ayer: p_lluvia = 0.7 if lluvia_hoy else 0.3
    else:           p_lluvia = 0.3 if lluvia_hoy else 0.7
        
    # Probabilidad de viento hoy depende del viento de ayer
    if viento_ayer: p_viento = 0.8 if viento_hoy else 0.2
    else:           p_viento = 0.4 if viento_hoy else 0.6
        
    # Asumimos que evolucionan independientemente de un día a otro
    return p_lluvia * p_viento

# 3. EL MODELO DE OBSERVACIÓN P(E_t | X_t)
def prob_observacion(trae_paraguas, lluvia_hoy, viento_hoy):
    if lluvia_hoy and viento_hoy:
        prob = 0.5
    elif lluvia_hoy and not viento_hoy:
        prob = 0.9
    elif not lluvia_hoy and viento_hoy:
        prob = 0.05
    else:
        prob = 0.01
        
    return prob if trae_paraguas else (1.0 - prob)

# 4. CREENCIAS INICIALES P(X_0)
# Día 0: Asumimos que todo es un volado (25% cada combinación)
creencia = {
    (True, True): 0.25,
    (True, False): 0.25,
    (False, True): 0.25,
    (False, False): 0.25
}

def imprimir_creencia(dia, evidencia, c):
    print(f"\n[Día {dia}] Evidencia observada: {'PARAGUAS' if evidencia else 'NADA'}")
    print("Probabilidades del estado real (Lluvia, Viento):")
    for estado, prob in sorted(c.items(), key=lambda item: item[1], reverse=True):
        llueve = "Llueve" if estado[0] else "Seco  "
        viento = "Viento" if estado[1] else "Calma "
        barra = "█" * int(prob * 30)
        print(f"  {llueve} & {viento} | {prob*100:05.2f}% | {barra}")
        
    prob_lluvia_total = sum(prob for (ll, v), prob in c.items() if ll)
    print(f"  -> Probabilidad consolidada de Lluvia: {prob_lluvia_total*100:.1f}%")

def actualizar_dbn(creencia_ayer, trae_paraguas_hoy):
    creencia_hoy = {}
    
    # Iteramos sobre todos los estados posibles de HOY
    for lluvia_hoy in [True, False]:
        for viento_hoy in [True, False]:
            
            # FASE 1: PREDICCIÓN (Calculamos la sumatoria del pasado)
            prob_predicha = 0.0
            for lluvia_ayer in [True, False]:
                for viento_ayer in [True, False]:
                    # P(X_t | X_{t-1}) * P(X_{t-1})
                    transicion = prob_transicion(lluvia_hoy, viento_hoy, lluvia_ayer, viento_ayer)
                    prob_pasada = creencia_ayer[(lluvia_ayer, viento_ayer)]
                    prob_predicha += transicion * prob_pasada
                    
            # FASE 2: ACTUALIZACIÓN (Multiplicamos por la evidencia de hoy)
            observacion = prob_observacion(trae_paraguas_hoy, lluvia_hoy, viento_hoy)
            creencia_hoy[(lluvia_hoy, viento_hoy)] = observacion * prob_predicha
            
    # FASE 3: NORMALIZACIÓN (Alfa)
    suma_total = sum(creencia_hoy.values())
    for estado in creencia_hoy:
        creencia_hoy[estado] /= suma_total
        
    return creencia_hoy

# --- EJECUCIÓN DE LA RED BAYESIANA DINÁMICA ---

# Observaciones de los próximos 3 días
dias = [
    (1, True),  # Día 1: El director trae paraguas
    (2, True),  # Día 2: Vuelve a traer paraguas
    (3, False)  # Día 3: Hoy llega sin paraguas
]

print("Estado Inicial (Día 0): Total incertidumbre.")

for numero_dia, evidencia_paraguas in dias:
    creencia = actualizar_dbn(creencia, evidencia_paraguas)
    imprimir_creencia(numero_dia, evidencia_paraguas, creencia)