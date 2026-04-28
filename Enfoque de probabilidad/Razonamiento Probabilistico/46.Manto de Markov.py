# =====================================================================
# ALGORITMO PARA EXTRAER EL MANTO DE MARKOV EN UNA RED BAYESIANA
# =====================================================================

def obtener_manto_de_markov(estructura_red, nodo_objetivo):
    """
    Escanea la estructura de una red bayesiana y devuelve el Manto de Markov
    del nodo objetivo (Padres + Hijos + Co-padres).
    """
    
    # Verificamos que el nodo exista en la red
    if nodo_objetivo not in estructura_red:
        return None
        
    # Usamos un 'set' (conjunto) de Python para evitar nodos duplicados
    manto_markov = set()
    
    # Listas auxiliares para mostrar el desglose educativo
    padres_encontrados = []
    hijos_encontrados = []
    copadres_encontrados = []

    # 1. ENCONTRAR LOS PADRES
    # Los padres están definidos directamente en el diccionario del nodo
    padres = estructura_red[nodo_objetivo]['padres']
    padres_encontrados.extend(padres)
    manto_markov.update(padres) # Añadimos al manto final
    
    # 2. ENCONTRAR LOS HIJOS Y CO-PADRES
    # Para encontrar los hijos, tenemos que revisar todos los nodos de la red
    # y ver si tienen a nuestro 'nodo_objetivo' como padre.
    for posible_hijo, datos_hijo in estructura_red.items():
        if nodo_objetivo in datos_hijo['padres']:
            
            # ¡Encontramos un hijo!
            hijos_encontrados.append(posible_hijo)
            manto_markov.add(posible_hijo) # Añadimos el hijo al manto
            
            # 3. ENCONTRAR LOS CO-PADRES
            # Ahora revisamos quiénes más son padres de este hijo que encontramos
            for co_padre in datos_hijo['padres']:
                # Si el co-padre no es nuestro nodo objetivo, es un "pareja"
                if co_padre != nodo_objetivo:
                    copadres_encontrados.append(co_padre)
                    manto_markov.add(co_padre) # Añadimos el co-padre al manto

    # Retornamos el conjunto final (convertido a lista) y los desgloses
    return {
        'manto_completo': list(manto_markov),
        'padres': padres_encontrados,
        'hijos': hijos_encontrados,
        'co_padres': list(set(copadres_encontrados)) # quitamos duplicados visuales
    }

# =====================================================================
# EJEMPLO DE USO (Sistema de Diagnóstico Médico)
# =====================================================================
if __name__ == "__main__":
    # Definimos la estructura de la red mediante dependencias (Padres -> Hijos)
    # Ejemplo clásico de una red médica simplificada
    red_medica = {
        'Contaminacion': {'padres': []},
        'Fumar': {'padres': []},
        'Cancer_Pulmon': {'padres': ['Contaminacion', 'Fumar']},
        'Rayos_X_Positivo': {'padres': ['Cancer_Pulmon']},
        'Fatiga': {'padres': ['Cancer_Pulmon']},
        'Tos': {'padres': ['Cancer_Pulmon', 'Infeccion_Viral']},
        'Infeccion_Viral': {'padres': []}
    }

    # ¿Cuál es el manto de Markov para 'Cancer_Pulmon'?
    objetivo = 'Cancer_Pulmon'
    
    print(f"--- ANALIZANDO EL MANTO DE MARKOV PARA: '{objetivo}' ---\n")
    
    resultados = obtener_manto_de_markov(red_medica, objetivo)
    
    if resultados:
        print("DESGLOSE DE COMPONENTES:")
        print(f"1. Padres (Causas): {resultados['padres']}")
        print(f"2. Hijos (Efectos): {resultados['hijos']}")
        print(f"3. Co-padres (Otras causas de los mismos efectos): {resultados['co_padres']}")
        
        print("\n==================================================")
        print(f"MANTO DE MARKOV COMPLETO: {resultados['manto_completo']}")
        print("==================================================")
        
        print(f"\nExplicación IA:")
        print(f"Si la IA conoce el estado exacto de {resultados['manto_completo']},")
        print(f"aislará por completo a '{objetivo}'. El resto de variables del universo")
        print("ya no aportarán información adicional para predecir el cáncer.")
    else:
        print("El nodo no existe en la red.")
