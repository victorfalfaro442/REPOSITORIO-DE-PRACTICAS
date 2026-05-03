print("--- ALGORITMO NAÏVE BAYES (FILTRO DE SPAM) ---")

# ==============================================================
# 1. EL CONJUNTO DE DATOS (Entrenamiento)
# ==============================================================
datos_entrenamiento = [
    ("gana dinero rápido gratis", "Spam"),
    ("oferta dinero gratis", "Spam"),
    ("gana un premio ahora", "Spam"),
    ("hola amigo", "Normal"),
    ("necesito dinero amigo", "Normal"),
    ("reunión de trabajo mañana", "Normal"),
    ("hola mañana hay reunión", "Normal")
]

# ==============================================================
# 2. FASE DE ENTRENAMIENTO (Extrayendo el conocimiento)
# ==============================================================
# Contadores
total_correos = len(datos_entrenamiento)
conteo_clases = {"Spam": 0, "Normal": 0}
vocabulario = set()
palabras_por_clase = {"Spam": [], "Normal": []}

# Llenando los contadores
for texto, clase in datos_entrenamiento:
    conteo_clases[clase] += 1
    palabras = texto.split()
    palabras_por_clase[clase].extend(palabras)
    for palabra in palabras:
        vocabulario.add(palabra)

# P(C) - Probabilidad a Priori de cada clase
prob_priori = {
    "Spam": conteo_clases["Spam"] / total_correos,
    "Normal": conteo_clases["Normal"] / total_correos
}

tamano_vocabulario = len(vocabulario)

# ==============================================================
# 3. FASE DE PREDICCIÓN (El clasificador Naïve Bayes)
# ==============================================================
def calcular_probabilidad_palabra(palabra, clase):
    """
    P(Atributo | Clase) con Suavizado de Laplace (+1)
    """
    lista_palabras_clase = palabras_por_clase[clase]
    # ¿Cuántas veces aparece esta palabra en esta clase?
    conteo_palabra = lista_palabras_clase.count(palabra)
    
    # Ecuación de Laplace: (Apariciones + 1) / (Total palabras en clase + Tamaño vocabulario total)
    numerador = conteo_palabra + 1
    denominador = len(lista_palabras_clase) + tamano_vocabulario
    
    return numerador / denominador

def clasificar_correo(nuevo_texto):
    print(f"[*] Analizando nuevo correo: '{nuevo_texto}'")
    palabras_nuevo = nuevo_texto.split()
    
    puntajes = {"Spam": 0.0, "Normal": 0.0}
    
    for clase in ["Spam", "Normal"]:
        # Empezamos con la probabilidad a Priori
        prob_acumulada = prob_priori[clase]
        
        # Multiplicamos por la probabilidad de cada palabra individual (La "Ingenuidad")
        for palabra in palabras_nuevo:
            prob_palabra = calcular_probabilidad_palabra(palabra, clase)
            prob_acumulada *= prob_palabra
            
        puntajes[clase] = prob_acumulada
        
    return puntajes

# ==============================================================
# 4. PRUEBA DEL ALGORITMO
# ==============================================================
correo_sospechoso = "¡Llegaron Nuevos Lentes Imperdibles!"

resultados = clasificar_correo(correo_sospechoso)

# Normalizamos para mostrar porcentajes bonitos
suma_total = sum(resultados.values())

print("-" * 50)
for clase, puntaje in resultados.items():
    porcentaje = (puntaje / suma_total) * 100
    print(f"Probabilidad de ser {clase:<6}: {porcentaje:6.2f}%")

clase_ganadora = max(resultados, key=resultados.get)
print("-" * 50)
print(f"🤖 DECISIÓN: El correo ha sido clasificado como -> {clase_ganadora.upper()}")