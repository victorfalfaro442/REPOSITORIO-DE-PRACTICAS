import random

print("--- INICIANDO EL DILEMA: EXPLORACIÓN VS EXPLOTACIÓN ---")

# ==============================================================
# 1. EL ENTORNO: LAS MÁQUINAS TRAGAMONEDAS (Valores Ocultos)
# ==============================================================
# La IA NO conoce estos porcentajes de éxito. Tendrá que descubrirlos.
# - Máquina A: Te engaña, parece buena pero solo paga el 30% de las veces.
# - Máquina B: Paga el 80% de las veces.
# - Máquina C: Paga el 50% de las veces (mediocre).
probabilidades_ocultas = {
    'Maquina_A': 0.3,
    'Maquina_B': 0.1,
    'Maquina_C': 0.9
}
maquinas = list(probabilidades_ocultas.keys())

def tirar_palanca(maquina):
    """El Casino: Si el número al azar es menor que la prob. oculta, ganas 1 punto."""
    if random.random() < probabilidades_ocultas[maquina]:
        return 1.0 # ¡Premio!
    else:
        return 0.0 # Perdiste

# ==============================================================
# 2. EL CEREBRO DE LA IA (Registros y Creencias)
# ==============================================================
# Q: ¿Cuánto creo que paga en promedio cada máquina? (Empieza en 0)
Q = {m: 0.0 for m in maquinas}

# K: ¿Cuántas veces he jugado en cada máquina? (Empieza en 0)
K = {m: 0 for m in maquinas}

# ==============================================================
# 3. HIPERPARÁMETROS
# ==============================================================
# epsilon = 0.10 significa que el 10% del tiempo hará locuras (Explorar).
# El 90% del tiempo elegirá la mejor opción conocida (Explotar).
epsilon = 0.10 
monedas_totales = 1000
premios_ganados = 0

# ==============================================================
# 4. EL BUCLE DE DECISIÓN (Gastando las monedas)
# ==============================================================
for tirada in range(1, monedas_totales + 1):
    
    # ------------------------------------------------------
    # FASE A: ¿EXPLORAR O EXPLOTAR?
    # ------------------------------------------------------
    if random.random() < epsilon:
        # ¡MODO EXPLORADOR! (10% de las veces)
        # La IA ignora todo lo que sabe y elige una máquina totalmente al azar.
        # A veces esto le hace perder dinero, pero le permite descubrir cosas nuevas.
        maquina_elegida = random.choice(maquinas)
    else:
        # ¡MODO EXPLOTADOR! (90% de las veces)
        # La IA revisa su diccionario 'Q' y elige la máquina con el puntaje más alto.
        # (Si hay empate al principio, max() devuelve la primera de la lista).
        maquina_elegida = max(Q, key=Q.get)
        
    # ------------------------------------------------------
    # FASE B: TIRAR DE LA PALANCA
    # ------------------------------------------------------
    recompensa = tirar_palanca(maquina_elegida)
    premios_ganados += recompensa
    
    # ------------------------------------------------------
    # FASE C: APRENDIZAJE (Actualizar la creencia de la máquina)
    # ------------------------------------------------------
    # 1. Sumamos 1 al contador de uso de esta máquina específica.
    K[maquina_elegida] += 1
    
    # 2. Aplicamos la Ecuación de Promedio Incremental.
    creencia_vieja = Q[maquina_elegida]
    veces_jugada = K[maquina_elegida]
    
    error_prediccion = recompensa - creencia_vieja
    
    Q[maquina_elegida] = creencia_vieja + (1 / veces_jugada) * error_prediccion

# ==============================================================
# 5. RESULTADOS DEL EXPERIMENTO
# ==============================================================
print("\n" + "="*50)
print(" RESULTADOS TRAS 1000 MONEDAS JUGADAS ")
print("="*50)

print(f"Premios totales ganados: {int(premios_ganados)} de 1000 posibles.\n")

print("Lo que la IA descubrió (Sus estimaciones Q):")
for m in maquinas:
    prob_real = probabilidades_ocultas[m] * 100
    creencia_ia = Q[m] * 100
    veces = K[m]
    print(f"  - {m}: Creía que pagaba {creencia_ia:05.2f}% (Real: {prob_real:05.2f}%) | Jugada {veces} veces.")

mejor_maquina_segun_ia = max(Q, key=Q.get)
print(f"\n[*] Conclusión de la IA: 'La mejor máquina es la {mejor_maquina_segun_ia}'")
