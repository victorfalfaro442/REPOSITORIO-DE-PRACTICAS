import math
import random

print("--- ALGORITMO DE RETROPROPAGACIÓN (BACKPROPAGATION) ---")

# ==============================================================
# 1. FUNCIONES MATEMÁTICAS Y SUS DERIVADAS
# ==============================================================
def sigmoide(x):
    x = max(-700, min(700, x))
    return 1 / (1 + math.exp(-x))

def derivada_sigmoide(a):
    # Recibe la salida de la sigmoide ('a'), no el valor crudo ('z')
    return a * (1 - a)

# ==============================================================
# 2. DEFINICIÓN DE LA RED NEURONAL (1 Capa Oculta)
# ==============================================================
class RedNeuronalSimple:
    def __init__(self, entradas, ocultas, salidas):
        # Inicialización de pesos al azar entre -1 y 1
        self.W_oculta = [[random.uniform(-1, 1) for _ in range(entradas)] for _ in range(ocultas)]
        self.B_oculta = [random.uniform(-1, 1) for _ in range(ocultas)]
        
        self.W_salida = [[random.uniform(-1, 1) for _ in range(ocultas)] for _ in range(salidas)]
        self.B_salida = [random.uniform(-1, 1) for _ in range(salidas)]

    def forward(self, X):
        # --- CAPA OCULTA ---
        self.A_oculta = []
        for i in range(len(self.W_oculta)):
            z = sum(X[j] * self.W_oculta[i][j] for j in range(len(X))) + self.B_oculta[i]
            self.A_oculta.append(sigmoide(z))
            
        # --- CAPA DE SALIDA ---
        self.A_salida = []
        for i in range(len(self.W_salida)):
            z = sum(self.A_oculta[j] * self.W_salida[i][j] for j in range(len(self.A_oculta))) + self.B_salida[i]
            self.A_salida.append(sigmoide(z))
            
        return self.A_salida

    def backward(self, X, Y_real, tasa_aprendizaje):
        # 1. Calcular Error en la Salida
        errores_salida = [Y_real[i] - self.A_salida[i] for i in range(len(Y_real))]
        
        # 2. Calcular los Gradientes (Deltas) de la capa de salida
        deltas_salida = [errores_salida[i] * derivada_sigmoide(self.A_salida[i]) for i in range(len(self.A_salida))]
        
        # 3. Propagar el error hacia atrás 
        errores_oculta = [0] * len(self.A_oculta)
        for j in range(len(self.A_oculta)):
            errores_oculta[j] = sum(deltas_salida[i] * self.W_salida[i][j] for i in range(len(self.A_salida)))
            
        # 4. Calcular los Gradientes (Deltas) de la capa oculta
        deltas_oculta = [errores_oculta[j] * derivada_sigmoide(self.A_oculta[j]) for j in range(len(self.A_oculta))]
        
        # --- ACTUALIZACIÓN DE PESOS ---
        
        # Ajustar pesos de la Capa de Salida
        for i in range(len(self.W_salida)):
            for j in range(len(self.W_salida[i])):
                self.W_salida[i][j] += tasa_aprendizaje * deltas_salida[i] * self.A_oculta[j]
            self.B_salida[i] += tasa_aprendizaje * deltas_salida[i]
            
        # Ajustar pesos de la Capa Oculta
        for i in range(len(self.W_oculta)):
            for j in range(len(self.W_oculta[i])):
                self.W_oculta[i][j] += tasa_aprendizaje * deltas_oculta[i] * X[j]
            self.B_oculta[i] += tasa_aprendizaje * deltas_oculta[i]

# ==============================================================
# 3. ENTRENAMIENTO (Problema XOR)
# ==============================================================
datos_XOR = [
    ([0, 0], [0]),
    ([0, 1], [1]),
    ([1, 0], [1]),
    ([1, 1], [0])
]

# Red con 2 entradas, 4 neuronas ocultas y 1 salida
red = RedNeuronalSimple(entradas=2, ocultas=4, salidas=1)
epocas = 10000
tasa_ap = 0.5

print("[*] Iniciando entrenamiento de Retropropagación...")
for epoca in range(epocas):
    error_total = 0
    for X, Y in datos_XOR:
        prediccion = red.forward(X)
        red.backward(X, Y, tasa_ap)
        error_total += 0.5 * sum((Y[i] - prediccion[i])**2 for i in range(len(Y)))
        
    if (epoca + 1) % 2500 == 0:
        print(f"  -> Época {epoca + 1} | Error Cuadrático: {error_total:.6f}")

print("-" * 50)
print("[*] ENTRENAMIENTO COMPLETADO. PROBANDO RED:")

for X, Y in datos_XOR:
    resultado = red.forward(X)[0]
    decision = 1 if resultado >= 0.5 else 0
    print(f"Entrada {X} -> Esperado: {Y[0]} | Predicción IA: {resultado:.4f} -> {decision}")
