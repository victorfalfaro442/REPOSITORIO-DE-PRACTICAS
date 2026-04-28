import itertools

# ========================
# 1. DEFINICIÓN DE LA RED 
# ========================
red_alarma = {
    'Robo': {'padres': [], 'cpt': {(): 0.001}},
    'Terremoto': {'padres': [], 'cpt': {(): 0.002}},
    'Alarma': {
        'padres': ['Robo', 'Terremoto'],
        'cpt': {
            (True, True): 0.95, (True, False): 0.94,
            (False, True): 0.29, (False, False): 0.001
        }
    },
    'JuanLlama': {'padres': ['Alarma'], 'cpt': {(True,): 0.90, (False,): 0.05}},
    'MariaLlama': {'padres': ['Alarma'], 'cpt': {(True,): 0.70, (False,): 0.01}}
}

# =====================================================================
# 2. EL MOTOR DE FACTORES (La base del algoritmo)
# =====================================================================
class Factor:
    def __init__(self, variables, tabla):
        """
        Un Factor tiene una lista de variables y una tabla (diccionario)
        que mapea combinaciones de esas variables a probabilidades.
        """
        self.variables = variables # ej. ['Robo', 'Alarma']
        self.tabla = tabla         # ej. {(True, True): 0.95, ...}

def crear_factor_inicial(nodo, red, evidencia):
    """Convierte la CPT de un nodo en un Factor, aplicando la evidencia si existe."""
    variables = red[nodo]['padres'] + [nodo]
    tabla = {}
    
    # Generamos todas las combinaciones posibles de True/False para estas variables
    combinaciones = list(itertools.product([True, False], repeat=len(variables)))
    
    for comb in combinaciones:
        estado = dict(zip(variables, comb))
        
        # Si la combinación choca con nuestra evidencia, la ignoramos (probabilidad 0)
        cumple_evidencia = True
        for var, val in evidencia.items():
            if var in estado and estado[var] != val:
                cumple_evidencia = False
                break
                
        if cumple_evidencia:
            # Extraemos la probabilidad de la CPT original
            valores_padres = tuple(estado[p] for p in red[nodo]['padres'])
            prob_true = red[nodo]['cpt'][valores_padres]
            prob = prob_true if estado[nodo] else (1.0 - prob_true)
            
            # Guardamos en la nueva tabla del factor
            tabla[comb] = prob
            
    return Factor(variables, tabla)

def multiplicar_factores(f1, f2):
    """Junta dos factores en uno solo multiplicando sus probabilidades."""
    # Obtenemos las variables combinadas sin duplicados
    nuevas_vars = list(set(f1.variables + f2.variables))
    nueva_tabla = {}
    
    # Generamos los nuevos mundos posibles
    combinaciones = list(itertools.product([True, False], repeat=len(nuevas_vars)))
    
    for comb in combinaciones:
        estado = dict(zip(nuevas_vars, comb))
        
        # Extraemos los valores correspondientes para f1 y f2
        tupla_f1 = tuple(estado[v] for v in f1.variables)
        tupla_f2 = tuple(estado[v] for v in f2.variables)
        
        # Si estas combinaciones existen en sus tablas, las multiplicamos
        if tupla_f1 in f1.tabla and tupla_f2 in f2.tabla:
            nueva_tabla[comb] = f1.tabla[tupla_f1] * f2.tabla[tupla_f2]
            
    return Factor(nuevas_vars, nueva_tabla)

def sumar_y_eliminar(factor, variable_a_eliminar):
    """Elimina una variable del factor sumando sus probabilidades (Marginalización)."""
    nuevas_vars = [v for v in factor.variables if v != variable_a_eliminar]
    nueva_tabla = {}
    
    for comb_original, prob in factor.tabla.items():
        estado = dict(zip(factor.variables, comb_original))
        
        # Creamos la tupla sin la variable que vamos a eliminar
        tupla_nueva = tuple(estado[v] for v in nuevas_vars)
        
        # Acumulamos la probabilidad (Sumatoria)
        if tupla_nueva not in nueva_tabla:
            nueva_tabla[tupla_nueva] = 0.0
        nueva_tabla[tupla_nueva] += prob
        
    return Factor(nuevas_vars, nueva_tabla)

# =====================================================================
# 3. ELIMINACIÓN DE VARIABLES
# =====================================================================
def eliminacion_de_variables(consulta, evidencia, red):
    # 1. Inicializar todos los factores
    factores = [crear_factor_inicial(nodo, red, evidencia) for nodo in red]
    
    # 2. Identificar variables ocultas a eliminar
    # Todas las de la red excepto la consulta y las que son evidencia
    variables_ocultas = [nodo for nodo in red if nodo != consulta and nodo not in evidencia]
    
    print("\n--- INICIANDO ELIMINACIÓN DE VARIABLES ---")
    
    # 3. Eliminar variables una por una
    for oculta in variables_ocultas:
        print(f"Eliminando variable oculta: '{oculta}'")
        
        # Separamos los factores que contienen la variable oculta
        factores_con_var = [f for f in factores if oculta in f.variables]
        factores = [f for f in factores if oculta not in f.variables] # Dejamos los demás
        
        # Multiplicamos todos los factores que tienen esta variable
        if factores_con_var:
            factor_multiplicado = factores_con_var[0]
            for f in factores_con_var[1:]:
                factor_multiplicado = multiplicar_factores(factor_multiplicado, f)
                
            # Eliminamos (sumamos) la variable y añadimos el factor destilado a nuestra lista
            factor_reducido = sumar_y_eliminar(factor_multiplicado, oculta)
            factores.append(factor_reducido)

    # 4. Fase Final: Solo queda la variable de consulta
    print("Multiplicando factores restantes para la consulta final...")
    factor_final = factores[0]
    for f in factores[1:]:
        factor_final = multiplicar_factores(factor_final, f)
        
    # 5. Normalizar el resultado (La constante Alfa)
    total = sum(factor_final.tabla.values())
    resultado_normalizado = {
        estado[0]: prob / total 
        for estado, prob in factor_final.tabla.items()
    }
    
    return resultado_normalizado

# =====================================================================
# EJEMPLO DE USO
# =====================================================================
if __name__ == "__main__":
    evidencia_observada = {'JuanLlama': True, 'MariaLlama': True}
    variable_objetivo = 'Robo'
    
    print(f"Evidencia: {evidencia_observada}")
    print(f"Consulta: '{variable_objetivo}'")
    
    resultado = eliminacion_de_variables(variable_objetivo, evidencia_observada, red_alarma)
    
    print("\n--- RESULTADO FINAL EXACTO ---")
    print(f"Probabilidad de que haya un Robo (True): {resultado[True] * 100:.2f}%")
    print(f"Probabilidad de que NO haya Robo (False): {resultado[False] * 100:.2f}%")
