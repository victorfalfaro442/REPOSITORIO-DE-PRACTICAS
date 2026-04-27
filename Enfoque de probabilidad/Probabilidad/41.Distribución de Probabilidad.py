import random

# =====================================================================
# FASE 1: APRENDIZAJE (CALCULAR LA DISTRIBUCIÓN DE PROBABILIDAD)
# =====================================================================
def aprender_distribucion(datos):
    """
    Toma una lista de datos (el historial) y calcula la probabilidad
    de que cada elemento aparezca, devolviendo un diccionario.
    """
    total_elementos = len(datos)
    frecuencias = {}
    
    # 1. Contar cuántas veces aparece cada elemento en nuestros datos
    for elemento in datos:
        if elemento in frecuencias:
            frecuencias[elemento] += 1  # Si ya existe, sumamos 1
        else:
            frecuencias[elemento] = 1   # Si es nuevo, empezamos en 1

    # 2. Convertir esas frecuencias en probabilidades (entre 0.0 y 1.0)
    distribucion = {}
    for elemento, conteo in frecuencias.items():
        # La probabilidad es la frecuencia dividida por el total de elementos
        probabilidad = conteo / total_elementos
        distribucion[elemento] = probabilidad
        
    return distribucion

# =====================================================================
# FASE 2: INFERENCIA (PREDECIR BASADO EN LA DISTRIBUCIÓN)
# =====================================================================
def generar_prediccion(distribucion):
    """
    Utiliza el algoritmo de 'Selección por Ruleta' para elegir un elemento.
    Elementos con mayor probabilidad tienen un 'trozo' más grande de la ruleta.
    """
    # Generamos un número aleatorio entre 0.0 y 1.0
    tiro_ruleta = random.random() 
    
    # Variable para ir sumando los "trozos" de la ruleta
    probabilidad_acumulada = 0.0
    
    # Recorremos cada elemento y su probabilidad
    for elemento, probabilidad in distribucion.items():
        # Añadimos la probabilidad actual al acumulador
        probabilidad_acumulada += probabilidad
        
        # Si nuestro tiro de ruleta cae dentro de esta área acumulada, 
        # hemos encontrado nuestro elemento ganador.
        if tiro_ruleta <= probabilidad_acumulada:
            return elemento
            
    # Retorno de seguridad (por si hay pequeñísimos errores de redondeo en Python)
    return list(distribucion.keys())[-1]

# =====================================================================
# EJEMPLO DE USO (PRUEBA DEL ALGORITMO)
# =====================================================================
if __name__ == "__main__":
    # 1. Definimos nuestros datos históricos (ej. acciones de un usuario, clima, etc.)
    # Aquí, 'manzana' aparece más veces, por lo que debería tener mayor probabilidad.
    historial_compras = [
        'manzana', 'manzana', 'manzana', 'manzana', 'manzana', # 5 manzanas
        'platano', 'platano', 'platano',                       # 3 plátanos
        'naranja', 'naranja'                                   # 2 naranjas
    ] # Total: 10 elementos

    # 2. Entrenamos el modelo
    print("--- FASE DE APRENDIZAJE ---")
    modelo_probabilidades = aprender_distribucion(historial_compras)
    
    # Mostramos lo que aprendió la IA
    for fruta, prob in modelo_probabilidades.items():
        print(f"Probabilidad de {fruta}: {prob * 100}%")

    # 3. Hacemos predicciones usando el modelo
    print("\n--- FASE DE PREDICCIÓN ---")
    print("Simulando 10 nuevas compras basadas en nuestro modelo...")
    
    resultados_simulacion = []
    for _ in range(10):
        # La IA predice la próxima compra basándose en la distribución aprendida
        prediccion = generar_prediccion(modelo_probabilidades)
        resultados_simulacion.append(prediccion)
        
    print(f"Resultados generados por la IA: {resultados_simulacion}")
