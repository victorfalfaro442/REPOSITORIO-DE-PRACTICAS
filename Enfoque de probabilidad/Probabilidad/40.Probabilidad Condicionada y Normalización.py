import random

print("--- ALGORITMO: CADENAS DE MARKOV (CONDICIÓN Y NORMALIZACIÓN) ---")

# ==============================================================
# 1. LOS DATOS CRUDOS (Conteos Históricos sin normalizar)
# ==============================================================
# La IA leyó un diario de muchos años y anotó las transiciones.
# Ejemplo: Si hoy estuvo 'Soleado', al día siguiente hubo Sol 80 veces y Lluvia 20 veces.
registro_transiciones = {
    'Soleado': {'Soleado': 80, 'Lluvioso': 20, 'Nublado': 50},
    'Lluvioso': {'Soleado': 30, 'Lluvioso': 60, 'Nublado': 10},
    'Nublado': {'Soleado': 40, 'Lluvioso': 40, 'Nublado': 20}
}

# ==============================================================
# 2. FASE A: NORMALIZACIÓN (Creando la Matriz de Probabilidades)
# ==============================================================
# Aquí convertimos los números crudos en probabilidades válidas (que sumen 1.0)
matriz_markov = {}

print("[*] Normalizando los datos históricos...\n")

for clima_hoy, transiciones in registro_transiciones.items():
    # 1. Calculamos el total de eventos para el clima de hoy (El divisor)
    total_eventos = sum(transiciones.values())
    
    # 2. Normalizamos dividiendo cada conteo entre el total
    matriz_markov[clima_hoy] = {}
    for clima_manana, conteo in transiciones.items():
        probabilidad_normalizada = conteo / total_eventos
        matriz_markov[clima_hoy][clima_manana] = probabilidad_normalizada

# Imprimimos la matriz resultante para ver cómo aprendió la IA
for clima, probabilidades in matriz_markov.items():
    print(f"Si hoy está {clima.upper()}:")
    for prox_clima, prob in probabilidades.items():
        print(f"  -> Prob. de que mañana esté {prox_clima}: {prob * 100:.1f}%")
    # Comprobación de que la Normalización funcionó (la suma debe ser 100%)
    suma_total = sum(probabilidades.values())
    print(f"  (Suma total normalizada: {suma_total * 100:.0f}%)\n")

# ==============================================================
# 3. FASE B: INFERENCIA (Usando la Probabilidad Condicionada)
# ==============================================================
def predecir_siguiente_estado(estado_actual):
    """Elige el siguiente estado basándose en las probabilidades condicionadas."""
    # Extraemos las opciones y sus probabilidades DADO EL estado actual
    probabilidades_condicionadas = matriz_markov[estado_actual]
    
    opciones = list(probabilidades_condicionadas.keys())
    pesos = list(probabilidades_condicionadas.values())
    
    # random.choices lanza un dado usando las probabilidades exactas que le pasamos
    siguiente_estado = random.choices(opciones, weights=pesos, k=1)[0]
    return siguiente_estado

# ==============================================================
# 4. SIMULACIÓN DE LA PREDICCIÓN
# ==============================================================
clima_inicial = 'Lluvioso'
dias_a_predecir = 7

print("="*50)
print(f" SIMULANDO EL CLIMA A 7 DÍAS (Iniciando en: {clima_inicial})")
print("="*50)

clima_actual = clima_inicial

for dia in range(1, dias_a_predecir + 1):
    # La IA predice el futuro CONDICIONADO al presente
    clima_futuro = predecir_siguiente_estado(clima_actual)
    
    print(f"Día {dia}: {clima_futuro}")
    
    # Avanzamos en el tiempo: El mañana se convierte en el hoy
    clima_actual = clima_futuro
