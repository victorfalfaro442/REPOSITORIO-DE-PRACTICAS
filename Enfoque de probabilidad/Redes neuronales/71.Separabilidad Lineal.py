import random

print("--- SEPARABILIDAD LINEAL: LA PRUEBA DEFINITIVA ---")

# ==============================================================
# 1. LOS CONJUNTOS DE DATOS
# ==============================================================
# Formato: [x1, x2], Salida Esperada

# OR: Es 1 si al menos una entrada es 1 (Linealmente separable)
datos_OR = [
    ([0, 0], 0),
    ([0, 1], 1),
    ([1, 0], 1),
    ([1, 1], 1)
]

# XOR: Es 1 SOLO si las entradas son diferentes (NO linealmente separable)
datos_XOR = [
    ([0, 0], 0),
    ([0, 1], 1),
    ([1, 0], 1),
    ([1, 1], 0)
]

# ==============================================================
# 2. EL ENTRENADOR (Un Perceptrón Simple)
# ==============================================================
def entrenar_perceptron(datos, nombre_problema, max_epocas=1000):
    # Inicializamos pesos y sesgo en 0
    w1, w2, b = 0.0, 0.0, 0.0
    tasa_aprendizaje = 0.1
    
    print(f"\n[*] Intentando resolver el problema: {nombre_problema}")
    
    for epoca in range(max_epocas):
        errores = 0
        
        for (x1, x2), y_real in datos:
            # 1. Suma lineal
            z = (x1 * w1) + (x2 * w2) + b
            # 2. Activación escalón
            y_pred = 1 if z > 0 else 0
            
            # 3. Cálculo de error
            error = y_real - y_pred
            
            # 4. Actualización si hay error
            if error != 0:
                errores += 1
                w1 += tasa_aprendizaje * error * x1
                w2 += tasa_aprendizaje * error * x2
                b  += tasa_aprendizaje * error
                
        # Si logramos 0 errores, la frontera de decisión perfecta fue encontrada
        if errores == 0:
            print(f"  -> ¡ÉXITO! Convergió en la época {epoca + 1}.")
            print(f"  -> Ecuación de la línea: {w1:.1f}*x1 + {w2:.1f}*x2 + {b:.1f} = 0")
            return True
            
    print(f"  -> FRACASO. Límite de {max_epocas} épocas alcanzado sin convergencia.")
    return False

# ==============================================================
# 3. EJECUCIÓN DEL EXPERIMENTO
# ==============================================================
entrenar_perceptron(datos_OR, "Compuerta OR")
entrenar_perceptron(datos_XOR, "Compuerta XOR")
