import math

print("--- FUNCIONES DE ACTIVACIÓN: TRANSFORMANDO SEÑALES ---")

# ==============================================================
# 1. DEFINICIÓN MATEMÁTICA DE LAS FUNCIONES
# ==============================================================
def sigmoide(x):
    # Limitamos x para evitar errores de desbordamiento en math.exp
    x = max(-700, min(700, x))
    return 1 / (1 + math.exp(-x))

def tanh_activacion(x):
    return math.tanh(x)

def relu(x):
    # Literalmente: el máximo entre 0 y el número
    return max(0.0, float(x))

def softmax(lista_x):
    # 1. Encontrar el valor máximo para estabilidad numérica
    max_x = max(lista_x)
    # 2. Calcular los exponenciales (restando el max para evitar números gigantes)
    exponenciales = [math.exp(x - max_x) for x in lista_x]
    # 3. Suma total de los exponenciales
    suma_exp = sum(exponenciales)
    # 4. Dividir cada uno entre el total para obtener la probabilidad
    return [e / suma_exp for e in exponenciales]

# ==============================================================
# 2. SEÑALES DE ENTRADA (Valores crudos 'Z' de una neurona)
# ==============================================================
# Imaginemos que una neurona recibe estas 5 señales en distintos momentos
senales_z = [-5.0, -1.0, 0.0, 2.0, 10.0]

print("\n[*] SEÑALES ORIGINALES (Z):")
print([f"{z:>6.1f}" for z in senales_z])
print("-" * 65)

# ==============================================================
# 3. PROCESANDO LAS SEÑALES INDIVIDUALES
# ==============================================================
# SIGMOIDE
salidas_sig = [sigmoide(z) for z in senales_z]
print("SIGMOIDE (0 a 1)      ->", [f"{s:>6.4f}" for s in salidas_sig])

# TANH
salidas_tanh = [tanh_activacion(z) for z in senales_z]
print("TANH     (-1 a 1)     ->", [f"{s:>6.4f}" for s in salidas_tanh])

# RELU
salidas_relu = [relu(z) for z in senales_z]
print("RELU     (0 a inf)    ->", [f"{s:>6.1f}" for s in salidas_relu])
print("-" * 65)

# ==============================================================
# 4. EL CASO ESPECIAL: SOFTMAX (Evaluación grupal)
# ==============================================================
# Softmax no evalúa números aislados, evalúa a todos juntos para repartir el 100%
puntajes_clases = [1.5, 3.8, 0.2]

probabilidades = softmax(puntajes_clases)

print("\n[*] APLICANDO SOFTMAX A PUNTAJES DE CLASIFICACIÓN:")
print(f"Puntajes crudos: {puntajes_clases}")
print("Probabilidades resultantes:")
clases = ["Gato", "Perro", "Pájaro"]

for i in range(len(clases)):
    porcentaje = probabilidades[i] * 100
    print(f"  -> {clases[i]:<6}: {porcentaje:5.2f}%")

print(f"  -> SUMA TOTAL : {sum(probabilidades)*100:.0f}%")
