print("--- MOTOR DE RECONOCIMIENTO DEL HABLA ---")

# ==============================================================
# 1. EL MODELO DE LENGUAJE (Probabilidad a Priori)
# ==============================================================
# Refleja qué tan común es que el usuario diga estas palabras.
# P(W)
modelo_lenguaje = {
    "LUCES": 0.60, # Es una casa inteligente, es muy probable que pidan las luces
    "NUBES": 0.30, # Quizás preguntan por el clima
    "VOCES": 0.10  # Rara vez hablan de voces
}

# ==============================================================
# 2. EL DICCIONARIO FONÉTICO (Lo ideal)
# ==============================================================
# Cómo DEBERÍA sonar cada palabra en un mundo perfecto.
diccionario = {
    "LUCES": ["L", "U", "S", "E", "S"],
    "NUBES": ["N", "U", "B", "E", "S"],
    "VOCES": ["B", "O", "S", "E", "S"]  # Fonéticamente, V suena como B, C suena como S
}

# ==============================================================
# 3. EL MODELO ACÚSTICO (El ruido del mundo real)
# ==============================================================
def probabilidad_acustica(fonema_capturado, fonema_real):
    """
    P(A|W): Probabilidad de que el micrófono capte 'A' cuando el humano dijo 'W'.
    Simula las confusiones típicas de un micrófono o de la dicción.
    """
    if fonema_capturado == fonema_real:
        return 0.90 # 90% de las veces el micrófono acierta perfectamente
        
    # Confusiones comunes de pronunciación o ruido
    confusiones = {
        ("N", "L"): 0.30, # Escuchar N cuando era L
        ("B", "S"): 0.20,
        ("U", "O"): 0.40  # Vocales cerradas confundidas
    }
    
    # Buscamos si existe esa confusión específica
    if (fonema_capturado, fonema_real) in confusiones:
        return confusiones[(fonema_capturado, fonema_real)]
        
    # Si es un sonido completamente loco y diferente (ej. escuchar "Z" cuando era "A")
    return 0.01 

# ==============================================================
# 4. EL DECODIFICADOR (El algoritmo de búsqueda)
# ==============================================================
def reconocer_audio(audio_microfono):
    print(f"[*] El micrófono captó los sonidos: {audio_microfono}")
    
    resultados = {}
    
    for palabra_candidata, prob_priori in modelo_lenguaje.items():
        fonemas_ideales = diccionario[palabra_candidata]
        
        # Asumimos (para este ejemplo simple) que el usuario pronunció la misma cantidad de letras
        if len(audio_microfono) != len(fonemas_ideales):
            continue
            
        # Calculamos el Modelo Acústico: Multiplicamos la prob de cada sonido
        prob_acustica_total = 1.0
        for i in range(len(audio_microfono)):
            sonido_capturado = audio_microfono[i]
            sonido_ideal = fonemas_ideales[i]
            prob_acustica_total *= probabilidad_acustica(sonido_capturado, sonido_ideal)
            
        # LA ECUACIÓN MAESTRA: Modelo Acústico * Modelo de Lenguaje
        # P(A|W) * P(W)
        puntaje_final = prob_acustica_total * prob_priori
        resultados[palabra_candidata] = puntaje_final
        
    # Encontrar la palabra con el puntaje más alto
    palabra_ganadora = max(resultados, key=resultados.get)
    
    # Normalizar para mostrar porcentajes amigables
    suma_total = sum(resultados.values())
    print("-" * 50)
    for palabra, puntaje in resultados.items():
        porcentaje = (puntaje / suma_total) * 100
        print(f"Probabilidad de '{palabra}': {porcentaje:6.2f}%")
        
    return palabra_ganadora

# ==============================================================
# 5. PRUEBA DE CAMPO
# ==============================================================
# Imagina que el usuario dijo "LUCES" pero estaba resfriado y el micrófono era malo.
audio_ruidoso = ["B", "U", "S", "E", "S"] 

ganador = reconocer_audio(audio_ruidoso)
print("-" * 50)
print(f"🤖 IA: 'Entendido. Ejecutando acción para: {ganador}'")