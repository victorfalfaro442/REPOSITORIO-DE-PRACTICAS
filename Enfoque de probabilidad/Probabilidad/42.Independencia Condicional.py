# =====================================================================
# ALGORITMO BASADO EN INDEPENDENCIA CONDICIONAL (NAIVE BAYES)
# =====================================================================

def entrenar_modelo_independiente(datos):
    """
    Fase de Aprendizaje: Calcula las probabilidades previas (prior) 
    y las probabilidades condicionales de cada característica dada la clase.
    """
    total_correos = len(datos)
    
    # Diccionarios para contar
    conteo_clases = {'Spam': 0, 'Ham': 0}
    # Estructura: {'Spam': {'palabra1': conteo, 'palabra2': conteo}, 'Ham': {...}}
    conteo_palabras_por_clase = {'Spam': {}, 'Ham': {}}
    
    # 1. Contar frecuencias
    for clase, palabras in datos:
        conteo_clases[clase] += 1
        
        for palabra in palabras:
            if palabra not in conteo_palabras_por_clase[clase]:
                conteo_palabras_por_clase[clase][palabra] = 0
            conteo_palabras_por_clase[clase][palabra] += 1

    # 2. Calcular probabilidades
    modelo = {
        'probabilidad_clase': {},
        'probabilidad_condicional': {'Spam': {}, 'Ham': {}}
    }
    
    # Probabilidad previa P(Clase)
    for clase, conteo in conteo_clases.items():
        modelo['probabilidad_clase'][clase] = conteo / total_correos
        
    # Probabilidad condicional P(Palabra | Clase)
    for clase in ['Spam', 'Ham']:
        total_palabras_clase = sum(conteo_palabras_por_clase[clase].values())
        
        for palabra, conteo in conteo_palabras_por_clase[clase].items():
            # ¿Qué probabilidad hay de ver esta palabra asumiendo esta clase?
            modelo['probabilidad_condicional'][clase][palabra] = conteo / total_palabras_clase
            
    return modelo


def predecir_con_independencia_condicional(modelo, nuevo_correo):
    """
    Fase de Inferencia: Utiliza la asunción de Independencia Condicional
    para multiplicar las probabilidades individuales y predecir la clase.
    """
    probabilidades_finales = {}
    
    for clase in ['Spam', 'Ham']:
        # Partimos de la probabilidad base de la clase P(Clase)
        prob_acumulada = modelo['probabilidad_clase'][clase]
        
        # APLICACIÓN DE LA INDEPENDENCIA CONDICIONAL:
        # Asumimos que las palabras son independientes entre sí dada la clase.
        # Por lo tanto, podemos simplemente multiplicar sus probabilidades.
        for palabra in nuevo_correo:
            # Si la palabra existe en nuestro modelo para esa clase
            if palabra in modelo['probabilidad_condicional'][clase]:
                prob_palabra_dada_clase = modelo['probabilidad_condicional'][clase][palabra]
            else:
                # Técnica simple de suavizado (si una palabra es nueva, le damos
                # una probabilidad mínima en lugar de 0 para no anular la multiplicación)
                prob_palabra_dada_clase = 0.001 
                
            # Multiplicamos: P(Clase) * P(Palabra1 | Clase) * P(Palabra2 | Clase)...
            prob_acumulada *= prob_palabra_dada_clase
            
        probabilidades_finales[clase] = prob_acumulada
        
    # Comparamos cuál clase obtuvo el puntaje más alto
    clase_ganadora = max(probabilidades_finales, key=probabilidades_finales.get)
    return clase_ganadora, probabilidades_finales


# =====================================================================
# EJEMPLO DE USO
# =====================================================================
if __name__ == "__main__":
    # Nuestro conjunto de datos histórico (Clase, [Lista de palabras en el correo])
    datos_entrenamiento = [
        ('Spam', ['oferta', 'dinero', 'gratis']),
        ('Spam', ['dinero', 'urgente']),
        ('Spam', ['oferta', 'exclusiva']),
        ('Ham', ['hola', 'amigo', 'reunion']),
        ('Ham', ['proyecto', 'reunion', 'urgente']), # 'urgente' puede aparecer en correos normales también
        ('Ham', ['hola', 'proyecto'])
    ]

    print("--- 1. ENTRENANDO EL MODELO ---")
    modelo_ia = entrenar_modelo_independiente(datos_entrenamiento)
    
    print("\nProbabilidades base P(Clase):")
    print(modelo_ia['probabilidad_clase'])
    
    print("\n--- 2. HACIENDO PREDICCIONES ---")
    
    # Caso A: Un correo que parece Spam
    correo_misterioso_1 = ['oferta', 'dinero']
    prediccion1, puntajes1 = predecir_con_independencia_condicional(modelo_ia, correo_misterioso_1)
    print(f"El correo {correo_misterioso_1} es clasificado como: {prediccion1}")
    print(f"Puntajes calculados: {puntajes1}\n")
    
    # Caso B: Un correo que parece Ham (Normal)
    correo_misterioso_2 = ['hola', 'reunion', 'proyecto']
    prediccion2, puntajes2 = predecir_con_independencia_condicional(modelo_ia, correo_misterioso_2)
    print(f"El correo {correo_misterioso_2} es clasificado como: {prediccion2}")
    print(f"Puntajes calculados: {puntajes2}")
