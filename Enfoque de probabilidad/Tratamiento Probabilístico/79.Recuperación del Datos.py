import math
from collections import Counter

print("--- MOTOR DE BÚSQUEDA: RECUPERACIÓN DE DATOS (TF-IDF) ---")

# ==============================================================
# 1. LA BASE DE DATOS (Corpus) Y LA CONSULTA
# ==============================================================
documentos = {
    "Doc1": "el gato come pescado y el perro come carne",
    "Doc2": "la inteligencia artificial ayuda a analizar datos",
    "Doc3": "el analisis de datos es el futuro de la inteligencia"
}

consulta = "inteligencia y datos"

# ==============================================================
# 2. PROCESAMIENTO Y VOCABULARIO
# ==============================================================
# Tokenización simple (convertir a minúsculas y separar palabras)
def tokenizar(texto):
    return texto.lower().split()

docs_tokenizados = {nombre: tokenizar(texto) for nombre, texto in documentos.items()}
consulta_tokenizada = tokenizar(consulta)

# Crear el vocabulario global (todas las palabras únicas)
vocabulario = set()
for tokens in docs_tokenizados.values():
    vocabulario.update(tokens)
vocabulario.update(consulta_tokenizada)
vocabulario = sorted(list(vocabulario))

print(f"[*] Tamaño del vocabulario global: {len(vocabulario)} palabras")

# ==============================================================
# 3. CÁLCULO DE IDF (Frecuencia Inversa de Documento)
# ==============================================================
N = len(documentos)
idf = {}
for palabra in vocabulario:
    # Contamos en cuántos documentos aparece la palabra
    doc_count = sum(1 for tokens in docs_tokenizados.values() if palabra in tokens)
    # Si la palabra solo está en la consulta, evitamos división por cero asumiendo doc_count = 1
    doc_count = max(1, doc_count) 
    # Fórmula IDF
    idf[palabra] = math.log(N / doc_count)

# ==============================================================
# 4. CÁLCULO DE VECTORES TF-IDF
# ==============================================================
def calcular_vector_tfidf(tokens):
    vector = []
    total_palabras = len(tokens)
    conteos = Counter(tokens)
    
    for palabra in vocabulario:
        # TF: Frecuencia del término
        tf = conteos[palabra] / total_palabras if total_palabras > 0 else 0
        # TF-IDF = TF * IDF
        vector.append(tf * idf[palabra])
    return vector

vectores_docs = {nombre: calcular_vector_tfidf(tokens) for nombre, tokens in docs_tokenizados.items()}
vector_consulta = calcular_vector_tfidf(consulta_tokenizada)

# ==============================================================
# 5. SIMILITUD DEL COSENO (Búsqueda o Matching)
# ==============================================================
def similitud_coseno(v1, v2):
    producto_punto = sum(a * b for a, b in zip(v1, v2))
    magnitud_v1 = math.sqrt(sum(a**2 for a in v1))
    magnitud_v2 = math.sqrt(sum(b**2 for b in v2))
    
    if magnitud_v1 == 0 or magnitud_v2 == 0:
        return 0.0
    return producto_punto / (magnitud_v1 * magnitud_v2)

print(f"\n[*] Ejecutando búsqueda para: '{consulta}'")
print("-" * 50)

# Calculamos la similitud de la consulta contra cada documento
resultados = {}
for nombre, vector_doc in vectores_docs.items():
    similitud = similitud_coseno(vector_consulta, vector_doc)
    resultados[nombre] = similitud

# Ordenamos los resultados de mayor a menor relevancia
resultados_ordenados = sorted(resultados.items(), key=lambda item: item[1], reverse=True)

# Mostrar resultados
for nombre, score in resultados_ordenados:
    print(f"Relevancia: {score:.4f} | {nombre}: '{documentos[nombre]}'")
