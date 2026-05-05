import random
from collections import defaultdict, Counter

print("--- MODELO PROBABILÍSTICO DEL LENGUAJE (BIGRAMAS) ---")

# ==============================================================
# 1. EL CORPUS (Nuestra fuente de verdad)
# ==============================================================
# Un corpus extremadamente simple sobre animales para el ejemplo.
corpus = """
el gato come pescado . 
el gato duerme mucho . 
el perro come carne . 
el perro ladra fuerte . 
el pajaro canta . 
el gato juega . 
el perro duerme .
"""

# ==============================================================
# 2. PROCESAMIENTO (Tokenización)
# ==============================================================
# Limpiamos y dividimos el texto en palabras individuales (tokens)
tokens = corpus.replace('\n', ' ').split()
print(f"[*] Corpus procesado. Total de tokens (palabras): {len(tokens)}")

# ==============================================================
# 3. ENTRENAMIENTO (Conteo de Bigramas)
# ==============================================================
# Diccionario que guardará: {palabra_anterior: {palabra_siguiente: conteo}}
modelo_bigramas = defaultdict(Counter)

# Recorremos el corpus creando pares de palabras
for i in range(len(tokens) - 1):
    palabra_actual = tokens[i]
    palabra_siguiente = tokens[i + 1]
    modelo_bigramas[palabra_actual][palabra_siguiente] += 1

# Convertimos los conteos en probabilidades (Ecuación MLE)
probabilidades = {}
for palabra, siguientes in modelo_bigramas.items():
    total_apariciones = sum(siguientes.values())
    probabilidades[palabra] = {
        siguiente: conteo / total_apariciones 
        for siguiente, conteo in siguientes.items()
    }

print("\n[*] Entrañas del modelo (Probabilidades después de 'el'):")
for sig, prob in probabilidades['el'].items():
    print(f"  -> P({sig} | el) = {prob:.2f} ({prob*100:.0f}%)")

print("\n[*] Entrañas del modelo (Probabilidades después de 'gato'):")
for sig, prob in probabilidades['gato'].items():
    print(f"  -> P({sig} | gato) = {prob:.2f} ({prob*100:.0f}%)")

# ==============================================================
# 4. GENERACIÓN DE TEXTO (Inferencia)
# ==============================================================
def generar_oracion(modelo, semilla, longitud_maxima=10):
    oracion = [semilla]
    palabra_actual = semilla
    
    for _ in range(longitud_maxima - 1):
        # Si la palabra no está en el modelo o llegamos a un punto, terminamos
        if palabra_actual not in modelo or palabra_actual == '.':
            break
            
        # Obtenemos las posibles siguientes palabras y sus probabilidades
        opciones = list(modelo[palabra_actual].keys())
        pesos = list(modelo[palabra_actual].values())
        
        # Elegimos la siguiente palabra basándonos en la probabilidad estadística
        siguiente_palabra = random.choices(opciones, weights=pesos)[0]
        
        # Añadimos a la oración
        oracion.append(siguiente_palabra)
        palabra_actual = siguiente_palabra
        
    return " ".join(oracion)

print("\n" + "-" * 50)
print("[*] GENERANDO TEXTO NUEVO BASADO EN ESTADÍSTICA")
print("-" * 50)

# Generamos 5 oraciones empezando con la palabra "el"
for i in range(5):
    texto_generado = generar_oracion(probabilidades, "el")
    print(f"Generación {i+1}: {texto_generado}")
