import itertools

# =====================================================================
# 1. DEFINICIÓN DEL MODELO (LA RED BAYESIANA)
# =====================================================================
# Estructura: { 'Variable': { 'padres': [...], 'cpt': { (estado_padres): prob_True } } }
# Nota: La CPT solo guarda la probabilidad de que el nodo sea True. 
# La probabilidad de False es simplemente (1 - prob_True).

red_bayesiana = {
    'Lluvia': {
        'padres': [],
        'cpt': {
            (): 0.20  # P(Lluvia=True) = 0.20 (No tiene padres)
        }
    },
    'Aspersor': {
        'padres': ['Lluvia'],
        'cpt': {
            (True,): 0.01,  # P(Aspersor=True | Lluvia=True)
            (False,): 0.40  # P(Aspersor=True | Lluvia=False)
        }
    },
    'Pasto_Mojado': {
        'padres': ['Lluvia', 'Aspersor'],
        'cpt': {
            (True, True): 0.99,   # P(Pasto=True | Lluvia=True, Aspersor=True)
            (True, False): 0.80,  # P(Pasto=True | Lluvia=True, Aspersor=False)
            (False, True): 0.90,  # P(Pasto=True | Lluvia=False, Aspersor=True)
            (False, False): 0.00  # P(Pasto=True | Lluvia=False, Aspersor=False)
        }
    }
}

# =====================================================================
# 2. ALGORITMO DE INFERENCIA: CÁLCULO DE PROBABILIDAD CONJUNTA
# =====================================================================
def calcular_probabilidad_conjunta(red, estado_mundo):
    """
    Calcula la probabilidad de un escenario específico exacto.
    Ejemplo de estado_mundo: {'Lluvia': True, 'Aspersor': False, 'Pasto_Mojado': True}
    Multiplica P(Nodo | Padres) para todos los nodos.
    """
    probabilidad_total = 1.0
    
    for nodo, datos in red.items():
        # Obtenemos el valor asignado a este nodo en el escenario actual
        valor_nodo = estado_mundo[nodo]
        
        # Buscamos los valores de los padres de este nodo en el escenario
        valores_padres = tuple(estado_mundo[padre] for padre in datos['padres'])
        
        # Buscamos la probabilidad en la tabla (CPT) de que sea True
        prob_true = datos['cpt'][valores_padres]
        
        # Si en nuestro escenario el nodo es True, multiplicamos por prob_true.
        # Si es False, multiplicamos por (1 - prob_true).
        if valor_nodo == True:
            probabilidad_total *= prob_true
        else:
            probabilidad_total *= (1.0 - prob_true)
            
    return probabilidad_total

# =====================================================================
# 3. ALGORITMO DE INFERENCIA EXACTA POR ENUMERACIÓN
# =====================================================================
def inferencia_por_enumeracion(red, consulta, evidencia):
    """
    Calcula P(Consulta | Evidencia) generando todos los mundos posibles.
    Por ejemplo: P(Lluvia=True | Pasto_Mojado=True)
    """
    todas_las_variables = list(red.keys())
    
    # Generamos todas las combinaciones posibles de True/False para nuestras variables
    # Como tenemos 3 variables, habrá 2^3 = 8 mundos posibles.
    combinaciones = list(itertools.product([True, False], repeat=len(todas_las_variables)))
    
    suma_prob_evidencia = 0.0
    suma_prob_consulta_y_evidencia = 0.0
    
    for combinacion in combinaciones:
        # Construimos un diccionario con el "estado del mundo" actual
        estado_mundo = dict(zip(todas_las_variables, combinacion))
        
        # Verificamos si este mundo cumple con la evidencia que ya conocemos
        cumple_evidencia = all(estado_mundo[var] == val for var, val in evidencia.items())
        
        if cumple_evidencia:
            # Calculamos la probabilidad de que este mundo exacto ocurra
            prob_mundo = calcular_probabilidad_conjunta(red, estado_mundo)
            
            # Sumamos a la probabilidad total de la evidencia
            suma_prob_evidencia += prob_mundo
            
            # Verificamos si, además, este mundo cumple con lo que estamos consultando
            cumple_consulta = all(estado_mundo[var] == val for var, val in consulta.items())
            if cumple_consulta:
                suma_prob_consulta_y_evidencia += prob_mundo
                
    # Retornamos P(Consulta y Evidencia) / P(Evidencia)
    if suma_prob_evidencia == 0:
        return 0.0
    return suma_prob_consulta_y_evidencia / suma_prob_evidencia

# =====================================================================
# EJEMPLO DE USO
# =====================================================================
if __name__ == "__main__":
    print("--- INFERENCIA EN RED BAYESIANA ---")
    
    # CASO 1: Diagnóstico (De efecto a causa)
    # Vemos el pasto mojado (Evidencia). ¿Cuál es la probabilidad de que haya llovido?
    evidencia_1 = {'Pasto_Mojado': True}
    consulta_1 = {'Lluvia': True}
    
    prob_1 = inferencia_por_enumeracion(red_bayesiana, consulta_1, evidencia_1)
    print(f"1. Si el pasto está mojado, la probabilidad de que haya llovido es: {prob_1 * 100:.2f}%")
    
    # CASO 2: Explicación alternativa (Efecto de "Descuento" o "Explaining away")
    # Vemos el pasto mojado, PERO también vemos que el aspersor está encendido.
    # ¿Cómo cambia la probabilidad de que haya llovido?
    evidencia_2 = {'Pasto_Mojado': True, 'Aspersor': True}
    consulta_2 = {'Lluvia': True}
    
    prob_2 = inferencia_por_enumeracion(red_bayesiana, consulta_2, evidencia_2)
    print(f"2. Si el pasto está mojado Y el aspersor está encendido, la probabilidad de que haya llovido cae a: {prob_2 * 100:.2f}%")
