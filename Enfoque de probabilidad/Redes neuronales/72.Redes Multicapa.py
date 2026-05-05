import math
import random

print("--- ARQUITECTURA DE RED MULTICAPA (MLP) GENERALIZADA ---")

# ==============================================================
# 1. FUNCIONES MATEMÁTICAS BÁSICAS
# ==============================================================
def relu(x):
    return max(0.0, x)

def sigmoide(x):
    x = max(-700, min(700, x))
    return 1 / (1 + math.exp(-x))

# Simulación de producto punto (Dot Product) entre dos vectores
def producto_punto(vector1, vector2):
    return sum(v1 * v2 for v1, v2 in zip(vector1, vector2))

# ==============================================================
# 2. DEFINICIÓN DE LA CLASE "CAPA"
# ==============================================================
class CapaDensa:
    def __init__(self, n_entradas, n_neuronas, activacion="relu"):
        self.n_entradas = n_entradas
        self.n_neuronas = n_neuronas
        self.activacion = activacion
        
        # Matriz de pesos: una lista de pesos para cada neurona
        self.pesos = [[random.uniform(-1, 1) for _ in range(n_entradas)] for _ in range(n_neuronas)]
        # Vector de sesgos: un sesgo para cada neurona
        self.sesgos = [random.uniform(-1, 1) for _ in range(n_neuronas)]
        
    def propagar(self, entradas):
        salidas_capa = []
        for i in range(self.n_neuronas):
            # Z = W * A + b
            z = producto_punto(entradas, self.pesos[i]) + self.sesgos[i]
            
            # A = f(Z)
            if self.activacion == "relu":
                a = relu(z)
            elif self.activacion == "sigmoide":
                a = sigmoide(z)
            else:
                a = z # Lineal
                
            salidas_capa.append(a)
        return salidas_capa

# ==============================================================
# 3. DEFINICIÓN DE LA RED MULTICAPA
# ==============================================================
class RedMulticapa:
    def __init__(self, arquitectura):
        """
        arquitectura: lista con el número de neuronas por capa.
        Ej: [2, 3, 1] -> 2 entradas, 1 capa oculta de 3, 1 salida.
        """
        self.capas = []
        print(f"[*] Construyendo red con arquitectura: {arquitectura}")
        
        # Construimos las capas dinámicamente
        for i in range(1, len(arquitectura)):
            n_entradas = arquitectura[i-1]
            n_neuronas = arquitectura[i]
            
            # Usaremos ReLU para ocultas y Sigmoide para la salida final
            func_act = "relu" if i < len(arquitectura) - 1 else "sigmoide"
            
            nueva_capa = CapaDensa(n_entradas, n_neuronas, activacion=func_act)
            self.capas.append(nueva_capa)
            
            print(f"  -> Capa {i}: {n_entradas} entradas -> {n_neuronas} neuronas (Activación: {func_act.upper()})")
            
    def predecir(self, datos_entrada):
        activaciones_actuales = datos_entrada
        
        # La salida de una capa es la entrada de la siguiente
        for i, capa in enumerate(self.capas):
            activaciones_actuales = capa.propagar(activaciones_actuales)
            
        return activaciones_actuales

# ==============================================================
# 4. PRUEBA DE LA ARQUITECTURA
# ==============================================================
print("-" * 50)
# Creamos una red profunda: 3 entradas, dos capas ocultas (4 y 4), 1 salida
mi_red_profunda = RedMulticapa([3, 4, 4, 1])
print("-" * 50)

# Simulamos un dato de entrada cualquiera
entrada_ejemplo = [0.5, -1.2, 3.1]
print(f"[*] Procesando entrada: {entrada_ejemplo}")

# Hacemos la predicción (Forward Pass)
resultado_final = mi_red_profunda.predecir(entrada_ejemplo)

print(f"[*] Salida de la red: {resultado_final[0]:.6f}")
