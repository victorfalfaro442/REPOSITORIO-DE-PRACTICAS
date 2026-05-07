from collections import defaultdict

print("--- TRADUCCIÓN AUTOMÁTICA ESTADÍSTICA (MODELO DE ALINEACIÓN) ---")

# ==============================================================
# 1. EL CORPUS PARALELO (Textos alineados a nivel de oración)
# ==============================================================
# Formato: (Oración en Español, Oración en Inglés)
corpus_paralelo = [
    ("la casa verde", "the green house"),
    ("el perro ladra", "the dog barks"),
    ("el perro verde", "the green dog"),
    ("la casa grande", "the big house")
]

# ==============================================================
# 2. ENTRENAMIENTO (Cálculo de Probabilidades de Traducción)
# ==============================================================
# Diccionarios para contar co-ocurrencias
conteo_coocurrencia = defaultdict(lambda: defaultdict(int))
conteo_total_ingles = defaultdict(int)

print("[*] Procesando el Corpus Paralelo...")

# Paso 1: Contar cuántas veces aparece una palabra en español junto a una en inglés
for oracion_es, oracion_en in corpus_paralelo:
    palabras_es = oracion_es.split()
    palabras_en = oracion_en.split()
    
    for palabra_en in palabras_en:
        conteo_total_ingles[palabra_en] += 1
        for palabra_es in palabras_es:
            conteo_coocurrencia[palabra_en][palabra_es] += 1

# Paso 2: Convertir los conteos en probabilidades P(Español | Inglés)
# P(es|en) = Co-ocurrencias(es, en) / Total_apariciones(en)
probabilidades_traduccion = defaultdict(dict)

for palabra_en, traducciones_es in conteo_coocurrencia.items():
    for palabra_es, conteo in traducciones_es.items():
        prob = conteo / conteo_total_ingles[palabra_en]
        probabilidades_traduccion[palabra_en][palabra_es] = prob

# Mostrar las probabilidades aprendidas
print("\n[*] DICCIONARIO PROBABILÍSTICO APRENDIDO:")
for palabra_en, traducciones_es in probabilidades_traduccion.items():
    print(f"\nInglés: '{palabra_en}' se alinea con:")
    # Ordenar por mayor probabilidad
    trad_ordenadas = sorted(traducciones_es.items(), key=lambda x: x[1], reverse=True)
    for palabra_es, prob in trad_ordenadas:
        if prob > 0.2: # Mostrar solo asociaciones fuertes para limpiar la consola
            print(f"  -> Español: '{palabra_es}' (Probabilidad: {prob:.2f})")

# ==============================================================
# 3. DECODIFICADOR (Traducción Greedy - Solo Modelo de Traducción)
# ==============================================================
def traducir_palabra(palabra_es):
    """Encuentra la palabra en inglés que tiene más probabilidad de generar esta palabra en español."""
    mejor_traduccion = "?"
    max_prob = 0.0
    
    for palabra_en, traducciones_es in probabilidades_traduccion.items():
        if palabra_es in traducciones_es:
            prob = traducciones_es[palabra_es]
            if prob > max_prob:
                max_prob = prob
                mejor_traduccion = palabra_en
                
    return mejor_traduccion

print("\n" + "-" * 50)
print("[*] PRUEBA DE TRADUCCIÓN INVERSA (Español -> Inglés)")
print("-" * 50)

oracion_prueba = "el perro verde"
print(f"Oración original : {oracion_prueba}")

# Traducimos palabra por palabra buscando la máxima probabilidad
traduccion = [traducir_palabra(p) for p in oracion_prueba.split()]
print(f"Traducción SMT   : {' '.join(traduccion)}")
