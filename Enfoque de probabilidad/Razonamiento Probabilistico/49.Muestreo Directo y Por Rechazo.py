import random
import math

print("--- ALGORITMO: MUESTREO DIRECTO Y POR RECHAZO ---")

# ==============================================================
# 1. LA DISTRIBUCIÓN COMPLEJA 
# ==============================================================
def prob_trafico_web(hora):
    """
    Una curva matemática compleja P(x). 
    Digamos que hay un pico de tráfico a las 10:00 y otro a las 20:00.
    Devuelve un valor de probabilidad entre 0.0 y 1.0
    """
    if 0 <= hora <= 24:
        # Una combinación loca de ondas senoidales simulando la vida real
        onda1 = math.sin(hora / 24 * math.pi * 2 - math.pi/2) * 0.4 + 0.4
        onda2 = math.exp(-0.2 * (hora - 20)**2) * 0.5 # Pico a las 20:00
        return min(onda1 + onda2, 1.0) # Aseguramos que el máximo sea 1.0
    return 0.0

# ==============================================================
# 2. MUESTREO DIRECTO (La caja de mármol - Q(x))
# ==============================================================
def muestreo_directo_uniforme():
    """
    Esto es fácil: Elegir una hora al azar entre 0 y 24.
    Representa nuestra distribución propuesta Q(x).
    """
    return random.uniform(0, 24)

# ==============================================================
# 3. MUESTREO POR RECHAZO (Esculpiendo la curva real)
# ==============================================================
def muestreo_por_rechazo():
    """
    Aplica la matemática del rechazo para obtener una hora válida
    que respete la compleja curva de tráfico.
    """
    # Constante M: La altura máxima de nuestra caja (En este caso, 1.0)
    M = 1.0 
    
    while True:
        # PASO A: Proponer un candidato usando el Muestreo Directo (La caja uniforme)
        hora_candidata = muestreo_directo_uniforme()
        
        # PASO B: Tirar un "dardo vertical" (u) entre 0 y la altura máxima de la caja (M)
        altura_aleatoria_u = random.uniform(0, M)
        
        # PASO C: Evaluar la Ecuación de Aceptación
        # ¿El dardo cayó por debajo de la altura real de la curva de tráfico?
        altura_curva_real = prob_trafico_web(hora_candidata)
        
        if altura_aleatoria_u <= altura_curva_real:
            # ¡ACEPTADO! El punto está dentro de la figura.
            return hora_candidata
        else:
            # ¡RECHAZADO! El punto cayó en el aire vacío. Repetir el bucle.
            pass

# ==============================================================
# 4. EJECUTANDO LA SIMULACIÓN
# ==============================================================
muestras_deseadas = 10000
horas_aceptadas = []
intentos_totales = 0

print(f"[*] La IA está generando {muestras_deseadas} perfiles de usuarios...")

while len(horas_aceptadas) < muestras_deseadas:
    intentos_totales += 1
    
    hora_valida = muestreo_por_rechazo()
    horas_aceptadas.append(hora_valida)

# ==============================================================
# 5. RESULTADOS DE LA SIMULACIÓN
# ==============================================================
print("\n" + "="*50)
print(" RESULTADOS DEL MUESTREO POR RECHAZO ")
print("="*50)

tasa_aceptacion = (muestras_deseadas / intentos_totales) * 100

print(f"Intentos (bloques de mármol usados): {intentos_totales}")
print(f"Muestras válidas (esculpidas):       {muestras_deseadas}")
print(f"Tasa de eficiencia del algoritmo:    {tasa_aceptacion:.1f}%")

print("\n[Muestra representativa de horas generadas]:")
# Imprimimos 5 resultados para ver cómo se ven
for i in range(5):
    hora_formateada = f"{int(horas_aceptadas[i]):02d}:{int((horas_aceptadas[i]%1)*60):02d}"
    print(f" -> Usuario simulado ingresó a las {hora_formateada}")
