# =====================================================================
# 1. DEFINICIÓN DEL MODELO (LA RED DE LA ALARMA)
# =====================================================================
# Estructura: 'Nodo': {'padres': [...], 'cpt': {(estado_padres): prob_True}}
red_alarma = {
    'Robo': {'padres': [], 'cpt': {(): 0.001}},
    'Terremoto': {'padres': [], 'cpt': {(): 0.002}},
    'Alarma': {
        'padres': ['Robo', 'Terremoto'],
        'cpt': {
            (True, True): 0.95,
            (True, False): 0.94,
            (False, True): 0.29,
            (False, False): 0.001
        }
    },
    'JuanLlama': {
        'padres': ['Alarma'],
        'cpt': {(True,): 0.90, (False,): 0.05}
    },
    'MariaLlama': {
        'padres': ['Alarma'],
        'cpt': {(True,): 0.70, (False,): 0.01}
    }
}

# =====================================================================
# 2. FUNCIONES AUXILIARES
# =====================================================================
def obtener_probabilidad_nodo(nodo, valor_nodo, evidencia_actual, red):
    """Extrae P(Nodo=valor | Padres) de la tabla CPT basándose en el estado actual."""
    padres = red[nodo]['padres']
    # Buscamos qué valores tienen los padres en nuestra evidencia actual
    valores_padres = tuple(evidencia_actual[padre] for padre in padres)
    
    prob_true = red[nodo]['cpt'][valores_padres]
    
    # Si estamos evaluando el caso True, devolvemos prob_true. Si es False, su complemento.
    return prob_true if valor_nodo else (1.0 - prob_true)

def normalizar(distribucion):
    """Asegura que las probabilidades del diccionario sumen exactamente 1.0 (Constante Alfa)"""
    total = sum(distribucion.values())
    return {estado: prob / total for estado, prob in distribucion.items()}

# =====================================================================
# 3. ALGORITMO RECURSIVO: INFERENCIA POR ENUMERACIÓN
# =====================================================================
def enumerar_todas(variables, evidencia, red):
    """
    Función recursiva que recorre el árbol de variables.
    Si la variable es conocida (evidencia), multiplica su probabilidad y avanza.
    Si es oculta, calcula la probabilidad para True y False, y suma los resultados (Marginalización).
    """
    # CASO BASE: Si ya no quedan variables por procesar, retornamos 1.0 
    # (El fin de la cadena de multiplicaciones)
    if not variables:
        return 1.0
        
    # Tomamos la primera variable de la lista y separamos el resto
    Y = variables[0]
    resto_variables = variables[1:]
    
    if Y in evidencia:
        # CASO 1: La variable es parte de nuestra evidencia (ya sabemos su valor)
        valor_Y = evidencia[Y]
        prob_Y = obtener_probabilidad_nodo(Y, valor_Y, evidencia, red)
        
        # Multiplicamos su probabilidad y hacemos la llamada recursiva con el resto
        return prob_Y * enumerar_todas(resto_variables, evidencia, red)
        
    else:
        # CASO 2: La variable está oculta. Tenemos que MARGINALIZAR (Sumar sobre sus posibles valores)
        suma_probabilidades = 0.0
        
        # Evaluamos los dos mundos paralelos: ¿Qué pasa si Y es True? ¿Y si es False?
        for valor_posible in [True, False]:
            # Creamos un nuevo mundo (evidencia extendida) asumiendo este valor
            evidencia_extendida = evidencia.copy()
            evidencia_extendida[Y] = valor_posible
            
            prob_Y = obtener_probabilidad_nodo(Y, valor_posible, evidencia_extendida, red)
            
            # Multiplicamos y acumulamos la llamada recursiva
            suma_probabilidades += prob_Y * enumerar_todas(resto_variables, evidencia_extendida, red)
            
        return suma_probabilidades

def inferencia_por_enumeracion(consulta, evidencia, red):
    """
    Función principal. Calcula la distribución de probabilidad para la variable de consulta.
    Devuelve un diccionario con las probabilidades normalizadas de que sea True o False.
    """
    distribucion_final = {}
    todas_las_variables = list(red.keys())
    
    # Calculamos la probabilidad para cada estado posible de nuestra consulta (True y False)
    for valor_consulta in [True, False]:
        # Extendemos temporalmente la evidencia con el valor de la consulta
        evidencia_con_consulta = evidencia.copy()
        evidencia_con_consulta[consulta] = valor_consulta
        
        # Llamamos al motor recursivo para que haga todo el trabajo pesado
        probabilidad = enumerar_todas(todas_las_variables, evidencia_con_consulta, red)
        distribucion_final[valor_consulta] = probabilidad
        
    # El paso final es aplicar la constante alfa (normalizar)
    return normalizar(distribucion_final)

# =====================================================================
# EJEMPLO DE USO
# =====================================================================
if __name__ == "__main__":
    print("--- ALGORITMO DE INFERENCIA POR ENUMERACIÓN (RECURSIVO) ---")
    
    # EL MISTERIO: Juan y María me acaban de llamar para decirme que la alarma suena.
    evidencia_observada = {'JuanLlama': True, 'MariaLlama': True}
    
    # LA PREGUNTA: ¿Cuál es la probabilidad real de que estén robando mi casa?
    variable_objetivo = 'Robo'
    
    print(f"\nEvidencia recibida: {evidencia_observada}")
    print(f"Consultando probabilidad de: '{variable_objetivo}'...")
    
    # Ejecutamos el algoritmo
    resultado = inferencia_por_enumeracion(variable_objetivo, evidencia_observada, red_alarma)
    
    print("\n--- RESULTADO FINAL ---")
    print(f"Probabilidad de que haya un Robo (True): {resultado[True] * 100:.2f}%")
    print(f"Probabilidad de que sea una falsa alarma / otro motivo (False): {resultado[False] * 100:.2f}%")
    
    print("\nNota: La probabilidad no es del 100% porque la alarma tiene una pequeña")
    print("tasa de error, el terremoto podría haberla activado, o Juan/María podrían")
    print("haberse confundido. El algoritmo pondera matemáticamente todos esos factores.")
