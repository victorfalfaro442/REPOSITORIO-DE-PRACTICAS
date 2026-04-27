print("--- ALGORITMO NAÏVE BAYES (APRENDIZAJE A PRIORI) ---")

# ==============================================================
# 1. EL ENTORNO: DATOS HISTÓRICOS (Bandeja de entrada)
# ==============================================================
historial_correos = [
    ("gana dinero rapido", "Spam"),
    ("oferta exclusiva dinero", "Spam"),
    ("dinero gratis ahora", "Spam"),
    ("tu cuenta ha sido bloqueada", "Spam"),
    ("reunion de trabajo mañana", "Normal"),
    ("hola como estas", "Normal"),
    ("informe del proyecto", "Normal"),
    ("vamos a comer pizza", "Normal"),
    ("repaso del codigo fuente", "Normal"),
    ("felicidades por tu ascenso", "Normal")
]

# ==============================================================
# 2. FASE DE ENTRENAMIENTO (Calculando el "A Priori")
# ==============================================================
# Contadores
total_correos = len(historial_correos)
conteo_clases = {'Spam': 0, 'Normal': 0}
vocabulario_clases = {'Spam': [], 'Normal': []}

for texto, clase in historial_correos:
    conteo_clases[clase] += 1
    vocabulario_clases[clase].extend(texto.split())

# La IA deduce cómo es el mundo antes de analizar ninguna palabra.
prob_a_priori = {
    'Spam': conteo_clases['Spam'] / total_correos,
    'Normal': conteo_clases['Normal'] / total_correos
}

print("[*] Fase de entrenamiento completada.")
print(f"    Probabilidad a Priori de Spam:   {prob_a_priori['Spam'] * 100:.0f}%")
print(f"    Probabilidad a Priori de Normal: {prob_a_priori['Normal'] * 100:.0f}%\n")

# ==============================================================
# 3. EL MOTOR DE INFERENCIA (Clasificar un correo nuevo)
# ==============================================================
def calcular_probabilidad_palabra(palabra, clase):
    """Calcula P(Palabra|Clase). Usa 'Suavizado de Laplace' para evitar multiplicaciones por cero."""
    palabras_en_clase = vocabulario_clases[clase]
    # Contamos cuántas veces aparece la palabra, le sumamos 1 por seguridad (Laplace)
    conteo_palabra = palabras_en_clase.count(palabra) + 1 
    # Dividimos por el total de palabras en esa categoría + un margen
    total_palabras = len(palabras_en_clase) + 20 
    return conteo_palabra / total_palabras

def clasificar_correo(nuevo_texto):
    palabras = nuevo_texto.split()
    puntajes = {'Spam': 1.0, 'Normal': 1.0}
    
    for clase in ['Spam', 'Normal']:
        # 1. Todo comienza con la creencia A Priori
        puntaje_actual = prob_a_priori[clase]
        
        # 2. Multiplicamos la creencia por la evidencia de cada palabra
        for palabra in palabras:
            prob_palabra = calcular_probabilidad_palabra(palabra, clase)
            puntaje_actual *= prob_palabra
            
        puntajes[clase] = puntaje_actual
        
    return puntajes

# ==============================================================
# 4. PRUEBA EN TIEMPO REAL
# ==============================================================
correo_sospechoso = "Tu código de inicio de sesión de Spotify: 222968"
print(f"-> Analizando nuevo correo: '{correo_sospechoso}'")

resultados = clasificar_correo(correo_sospechoso)

# Normalizamos los puntajes para que sumen 100% (Probabilidad a Posteriori)
suma_total = sum(resultados.values())
prob_final_spam = (resultados['Spam'] / suma_total) * 100
prob_final_normal = (resultados['Normal'] / suma_total) * 100

print("\n" + "="*50)
print(" CONCLUSIÓN DEL FILTRO NAÏVE BAYES ")
print("="*50)
print(f"Probabilidad de que sea Normal: {prob_final_normal:.2f}%")
print(f"Probabilidad de que sea Spam:   {prob_final_spam:.2f}%")

if prob_final_spam > prob_final_normal:
    print("\n[Veredicto] -> 🚨 SPAM DETECTADO. Moviendo a la papelera.")
else:
    print("\n[Veredicto] -> ✅ CORREO LIMPIO. Moviendo a la bandeja de entrada.")
