import random

print("--- EVOLUCIÓN: PERCEPTRÓN VS ADALINE ---")

# ==============================================================
# 1. DATOS DE ENTRENAMIENTO (Puerta lógica OR usando -1 y 1)
# ==============================================================
# Entradas: [x1, x2] | Salida Esperada (1 o -1)
datos = [
    ([-1, -1], -1),
    ([-1,  1],  1),
    ([ 1, -1],  1),
    ([ 1,  1],  1)
]

tasa_aprendizaje = 0.1
epocas = 10

# ==============================================================
# 2. ENTRENAMIENTO DEL PERCEPTRÓN
# ==============================================================
print("\n[*] ENTRENANDO PERCEPTRÓN (Actualización Discreta)")
w_p1, w_p2, b_p = 0.5, -0.5, 0.0 # Pesos iniciales arbitrarios

for epoca in range(epocas):
    errores_totales = 0
    for (x1, x2), y_real in datos:
        # 1. Suma ponderada
        z = (x1 * w_p1) + (x2 * w_p2) + b_p
        
        # 2. Activación Escalón (Discreta: 1 o -1)
        y_pred = 1 if z >= 0 else -1
        
        # 3. Calcular Error (Será 0, 2 o -2)
        error = y_real - y_pred
        if error != 0: errores_totales += 1
            
        # 4. Actualizar Pesos (Solo si hubo error en clasificación)
        w_p1 += tasa_aprendizaje * error * x1
        w_p2 += tasa_aprendizaje * error * x2
        b_p  += tasa_aprendizaje * error

    if errores_totales == 0:
        print(f"  -> Perceptrón convergió en la época {epoca+1}")
        break

# ==============================================================
# 3. ENTRENAMIENTO DE ADALINE
# ==============================================================
print("\n[*] ENTRENANDO ADALINE (Regla Delta / Gradiente)")
w_a1, w_a2, b_a = 0.5, -0.5, 0.0 # Mismos pesos iniciales

for epoca in range(epocas):
    error_cuadratico_total = 0.0
    for (x1, x2), y_real in datos:
        # 1. Suma ponderada (Salida Lineal)
        z = (x1 * w_a1) + (x2 * w_a2) + b_a
        
        # 2. Calcular Error (Continuo, basado en Z, NO en predicción final)
        error_lineal = y_real - z
        error_cuadratico_total += (error_lineal ** 2)
        
        # 3. Actualizar Pesos (Regla Delta)
        # ADALINE SIEMPRE ajusta los pesos, incluso si la clasificación final sería correcta,
        # para "acercarse" más al valor matemático ideal.
        w_a1 += tasa_aprendizaje * error_lineal * x1
        w_a2 += tasa_aprendizaje * error_lineal * x2
        b_a  += tasa_aprendizaje * error_lineal
        
    print(f"  -> Época {epoca+1} | Error Cuadrático Medio: {error_cuadratico_total/4:.4f}")

# ==============================================================
# 4. COMPARACIÓN FINAL
# ==============================================================
print("\n" + "=" * 50)
print("COMPROBACIÓN DE PESOS FINALES")
print("=" * 50)
print(f"Pesos Perceptrón: w1={w_p1:.2f}, w2={w_p2:.2f}, b={b_p:.2f}")
print(f"Pesos ADALINE:    w1={w_a1:.2f}, w2={w_a2:.2f}, b={b_a:.2f}")

print("\nPredicciones ADALINE:")
for (x1, x2), y_real in datos:
    z_final = (x1 * w_a1) + (x2 * w_a2) + b_a
    pred_final = 1 if z_final >= 0 else -1
    print(f"Entrada [{x1:2}, {x2:2}] -> Z crudo: {z_final:5.2f} | Predicción: {pred_final}")
