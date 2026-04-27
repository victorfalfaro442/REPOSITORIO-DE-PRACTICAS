print("--- INICIANDO MOTOR DE INFERENCIA BAYESIANA ---")

# ==============================================================
# 1. EL CONOCIMIENTO PREVIO DE LA IA (Prior)
# ==============================================================
# El coche va por una autopista solitaria de noche. 
# La IA sabe que, históricamente, la probabilidad de que haya 
# un peatón (Hipótesis) en esta zona exacta es muy baja: 10%.
prob_peaton_real = 0.10      # P(H)
prob_no_peaton_real = 0.90   # P(~H)

# ==============================================================
# 2. EL MANUAL TÉCNICO DEL SENSOR (Likelihood)
# ==============================================================
# El fabricante del radar de niebla le dio a la IA estas especificaciones:
# - Verdadero Positivo: Si HAY un peatón, el sensor lo detecta el 90% de las veces.
prob_sensor_pita_dado_peaton = 0.90  # P(E|H)

# - Falso Positivo: Si NO hay un peatón, la niebla confunde al sensor y pita el 20% de las veces.
prob_sensor_pita_dado_nada = 0.20    # P(E|~H)

# ==============================================================
# 3. LA FUNCIÓN DE ACTUALIZACIÓN BAYESIANA
# ==============================================================
def actualizar_creencia(prior_H, prior_no_H, likelihood_H, likelihood_no_H):
    """
    Calcula la nueva creencia usando el Teorema de Bayes.
    """
    # Paso A: Calcular la Probabilidad Marginal P(E)
    # ¿Cuál es la probabilidad total de que el sensor pite en general?
    # (Pita porque hay peatón) + (Pita porque se confundió)
    prob_total_evidencia = (likelihood_H * prior_H) + (likelihood_no_H * prior_no_H)
    
    # Paso B: Aplicar la Ecuación de Bayes P(H|E) = (P(E|H) * P(H)) / P(E)
    posterior_H = (likelihood_H * prior_H) / prob_total_evidencia
    
    return posterior_H, prob_total_evidencia

# ==============================================================
# 4. EL EVENTO: EL SENSOR SE ACTIVA
# ==============================================================
print("\n[Evento en tiempo real] El coche va a 80 km/h en la niebla...")
print("[Sensor] -> ¡BIP BIP BIP! ¡Posible obstáculo detectado!")

# La IA calcula instantáneamente qué tan real es la amenaza
nueva_creencia_peaton, prob_total_pitar = actualizar_creencia(
    prob_peaton_real, 
    prob_no_peaton_real, 
    prob_sensor_pita_dado_peaton, 
    prob_sensor_pita_dado_nada
)

# ==============================================================
# 5. RESULTADOS DEL PENSAMIENTO DE LA IA
# ==============================================================
print("\n" + "="*50)
print(" ANÁLISIS DE INCERTIDUMBRE (RESULTADO BAYESIANO) ")
print("="*50)

print(f"Probabilidad de que el sensor pite en esta carretera: {prob_total_pitar * 100:.1f}%")
print(f"Precisión técnica del radar (Verdadero Positivo):     {prob_sensor_pita_dado_peaton * 100:.1f}%")

print("\n--- LA CONCLUSIÓN DE LA IA ---")
print(f"Probabilidad FINAL de que realmente haya un peatón:   {nueva_creencia_peaton * 100:.1f}%")

if nueva_creencia_peaton > 0.50:
    print("[Acción de la IA] -> FRENADO DE EMERGENCIA ACTIVADO.")
else:
    print("[Acción de la IA] -> Ignorar alerta (Falso positivo altamente probable). Mantener velocidad.")
