import math
import random

print("--- RED NEURONAL PROFUNDA (MLP) RESOLVIENDO XOR ---")

# ==============================================================
# 1. FUNCIONES MATEMÁTICAS
# ==============================================================
def sigmoide(x):
    # Limitamos x para evitar desbordamientos matemáticos
    x = max(-700, min(700, x))
    return 1 / (1 + math.exp(-x))

def derivada_sigmoide(x):
    # La derivada de la sigmoide es curiosamente ella misma por (1 - ella misma)
    return x * (1 - x)

# ==============================================================
# 2. DATOS DE ENTRENAMIENTO (Lógica XOR)
# ==============================================================
# [Entrada 1, Entrada 2], Salida Esperada
datos = [
    ([0, 0], 0),
    ([0, 1], 1), # 1 porque solo hay un '1'
    ([1, 0], 1),
    ([1, 1], 0)  # 0 porque ambos son '1' (Exclusivo)
]

# ==============================================================
# 3. INICIALIZACIÓN DE LA RED
# ==============================================================
# PESOS: Capa Entrada -> Capa Oculta (2 entradas x 2 neuronas ocultas = 4 pesos)
w_i_h = [[random.uniform(-1, 1), random.uniform(-1, 1)], 
         [random.uniform(-1, 1), random.uniform(-1, 1)]]
b_h = [random.uniform(-1, 1), random.uniform(-1, 1)] # Sesgos capa oculta

# PESOS: Capa Oculta -> Capa Salida (2 neuronas ocultas x 1 salida = 2 pesos)
w_h_o = [random.uniform(-1, 1), random.uniform(-1, 1)]
b_o = random.uniform(-1, 1) # Sesgo capa salida

tasa_aprendizaje = 0.5
epocas = 15000

print("[*] Entrenando la red... Esto requerirá miles de ajustes microscópicos.")

# ==============================================================
# 4. EL BUCLE DE APRENDIZAJE PROFUNDO
# ==============================================================
for epoca in range(epocas):
    for (x1, x2), y_real in datos:
        
        # --- PASO A: FORWARD PASS (Hacia adelante) ---
        # 1. Activación de la capa oculta
        h1_z = (x1 * w_i_h[0][0]) + (x2 * w_i_h[1][0]) + b_h[0]
        h1_a = sigmoide(h1_z)
        
        h2_z = (x1 * w_i_h[0][1]) + (x2 * w_i_h[1][1]) + b_h[1]
        h2_a = sigmoide(h2_z)
        
        # 2. Activación de la capa de salida
        out_z = (h1_a * w_h_o[0]) + (h2_a * w_h_o[1]) + b_o
        prediccion = sigmoide(out_z)
        
        # --- PASO B: BACKPROPAGATION (Hacia atrás) ---
        # 1. Error en la salida
        error_salida = y_real - prediccion
        delta_salida = error_salida * derivada_sigmoide(prediccion)
        
        # 2. Error en la capa oculta (¿De quién fue la culpa?)
        error_h1 = delta_salida * w_h_o[0]
        delta_h1 = error_h1 * derivada_sigmoide(h1_a)
        
        error_h2 = delta_salida * w_h_o[1]
        delta_h2 = error_h2 * derivada_sigmoide(h2_a)
        
        # --- PASO C: ACTUALIZACIÓN DE PESOS (Gradiente Descendente) ---
        # Ajuste Capa Oculta -> Salida
        w_h_o[0] += h1_a * delta_salida * tasa_aprendizaje
        w_h_o[1] += h2_a * delta_salida * tasa_aprendizaje
        b_o += delta_salida * tasa_aprendizaje
        
        # Ajuste Capa Entrada -> Oculta
        w_i_h[0][0] += x1 * delta_h1 * tasa_aprendizaje
        w_i_h[1][0] += x2 * delta_h1 * tasa_aprendizaje
        b_h[0] += delta_h1 * tasa_aprendizaje
        
        w_i_h[0][1] += x1 * delta_h2 * tasa_aprendizaje
        w_i_h[1][1] += x2 * delta_h2 * tasa_aprendizaje
        b_h[1] += delta_h2 * tasa_aprendizaje

print("[*] ¡Entrenamiento completado!")
print("-" * 50)

# ==============================================================
# 5. PRUEBA FINAL
# ==============================================================
print("RESULTADOS DEL PROBLEMA XOR:")
for (x1, x2), _ in datos:
    # Pasamos los datos por la red ya entrenada
    h1_a = sigmoide((x1 * w_i_h[0][0]) + (x2 * w_i_h[1][0]) + b_h[0])
    h2_a = sigmoide((x1 * w_i_h[0][1]) + (x2 * w_i_h[1][1]) + b_h[1])
    prediccion = sigmoide((h1_a * w_h_o[0]) + (h2_a * w_h_o[1]) + b_o)
    
    # Redondeamos para ver la decisión final de la IA
    decision = 1 if prediccion >= 0.5 else 0
    print(f"Entradas [{x1}, {x2}] -> Probabilidad: {prediccion:.4f} | Decisión: {decision}")
