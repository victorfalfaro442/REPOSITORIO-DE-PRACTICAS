print("--- FILTRO DE KALMAN (IMPLEMENTACIÓN EN PYTHON NATIVO) ---")

# ==============================================================
# 1. PARÁMETROS DEL SISTEMA
# ==============================================================
# Q: Proceso (Incertidumbre de qué tanto se mueve el barco solo)
proceso_varianza = 1e-5 

# R: Sensor (Ruido típico del sensor ultrasónico)
sensor_varianza = 0.1**2 

# ==============================================================
# 2. ESTADO INICIAL
# ==============================================================
post_estimacion = 0.0      # Nuestra estimación inicial (x)
post_error_estimacion = 1.0 # Nuestra confianza inicial (P)

# ==============================================================
# 3. LECTURAS REALES DEL SENSOR (Con mucho ruido)
# ==============================================================
# El barco está realmente a 10 metros, pero el sensor falla:
mediciones_sensor = [10.12, 9.85, 10.40, 9.60, 10.90, 10.05, 9.20, 10.10]

print(f"{'Medida':<10} | {'Estimación Kalman':<20} | {'Error (Confianza)':<15}")
print("-" * 55)

# ==============================================================
# 4. EL BUCLE DE KALMAN
# ==============================================================
for z in mediciones_sensor:
    # --- PASO 1: PREDICCIÓN (TIME UPDATE) ---
    # En este ejemplo simple, el barco está estático, 
    # pero nuestra incertidumbre crece un poco por el paso del tiempo.
    prior_estimacion = post_estimacion
    prior_error_estimacion = post_error_estimacion + proceso_varianza

    # --- PASO 2: ACTUALIZACIÓN (MEASUREMENT UPDATE) ---
    # A. Calcular la Ganancia de Kalman (K)
    # ¿A quién le creo más? ¿A mi predicción o al sensor?
    ganancia_kalman = prior_error_estimacion / (prior_error_estimacion + sensor_varianza)

    # B. Actualizar la estimación con la medida (z)
    post_estimacion = prior_estimacion + ganancia_kalman * (z - prior_estimacion)

    # C. Actualizar el error de la estimación (P se reduce)
    post_error_estimacion = (1 - ganancia_kalman) * prior_error_estimacion

    print(f"{z:<10.2f} | {post_estimacion:<20.4f} | {post_error_estimacion:<15.6f}")

print("\n[Resultado final] El barco está aproximadamente a: {:.2f} metros".format(post_estimacion))
