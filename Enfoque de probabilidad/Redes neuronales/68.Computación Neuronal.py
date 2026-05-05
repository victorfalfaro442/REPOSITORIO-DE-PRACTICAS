import math

print("--- COMPUTACIÓN NEURONAL: LA UNIDAD BÁSICA ---")

# ==============================================================
# 1. DEFINICIÓN DE LA NEURONA
# ==============================================================
class NeuronaArtificial:
    def __init__(self, pesos, sesgo):
        self.pesos = pesos
        self.sesgo = sesgo

    # --- Funciones de Activación ---
    def activacion_escalon(self, z):
        """Devuelve 1 si superamos el umbral, 0 si no (Clásica)."""
        return 1 if z >= 0 else 0

    def activacion_sigmoide(self, z):
        """Devuelve una probabilidad suave entre 0 y 1."""
        z = max(-700, min(700, z)) # Evitar desbordamiento
        return 1 / (1 + math.exp(-z))

    def activacion_relu(self, z):
        """Unidad Lineal Rectificada: Si es negativo, 0. Si es positivo, lo deja pasar."""
        return max(0, z)
        
    def activacion_tanh(self, z):
        """Tangente hiperbólica: Devuelve un valor entre -1 y 1."""
        return math.tanh(z)

    # --- El motor de computación ---
    def computar(self, entradas, funcion="relu"):
        # 1. Suma ponderada (Dot Product)
        suma_z = sum(x * w for x, w in zip(entradas, self.pesos)) + self.sesgo
        
        # 2. Paso por la función de activación
        if funcion == "escalon":
            salida = self.activacion_escalon(suma_z)
        elif funcion == "sigmoide":
            salida = self.activacion_sigmoide(suma_z)
        elif funcion == "relu":
            salida = self.activacion_relu(suma_z)
        elif funcion == "tanh":
            salida = self.activacion_tanh(suma_z)
        else:
            salida = suma_z # Lineal
            
        return suma_z, salida

# ==============================================================
# 2. SIMULACIÓN DE COMPUTACIÓN
# ==============================================================
# Imaginemos una neurona que decide si debes comprar un coche usado.
# Entradas: [Precio (normalizado), Kilometraje (normalizado), Estado estético (1-10)]
entradas_coche = [0.8, 0.9, 5] 

# Pesos: Le da importancia negativa al precio alto y kilometraje alto, y positiva al estado.
pesos_neurona = [-1.5, -2.0, 0.5] 
sesgo_neurona = 1.0 # Una predisposición inicial a comprar

mi_neurona = NeuronaArtificial(pesos_neurona, sesgo_neurona)

print(f"[*] Entradas recibidas: {entradas_coche}")
print(f"[*] Pesos sinápticos:   {pesos_neurona}")
print(f"[*] Sesgo (Bias):       {sesgo_neurona}\n")
print("-" * 55)

# Probamos la computación bajo diferentes "modos" matemáticos
funciones = ["escalon", "sigmoide", "relu", "tanh"]

for f in funciones:
    valor_z, resultado_final = mi_neurona.computar(entradas_coche, funcion=f)
    print(f"Computación con función '{f.upper()}':")
    print(f"  -> Valor crudo (Z) : {valor_z:.2f}")
    print(f"  -> Salida final (A): {resultado_final:.4f}\n")
