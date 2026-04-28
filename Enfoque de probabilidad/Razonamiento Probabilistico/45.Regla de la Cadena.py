# =====================================================================
# ALGORITMO: REGLA DE LA CADENA PARA EVENTOS SECUENCIALES
# =====================================================================

def calcular_probabilidad_secuencia(urna_inicial, secuencia_deseada):
    """
    Calcula la probabilidad conjunta de una secuencia de eventos usando
    la Regla de la Cadena de probabilidad.
    
    Parámetros:
    - urna_inicial: Diccionario con el conteo de elementos (ej. {'Rojo': 5, 'Azul': 3})
    - secuencia_deseada: Lista con el orden exacto de los eventos a evaluar.
    """
    # Hacemos una copia de la urna para no modificar la original
    urna_actual = urna_inicial.copy()
    total_elementos = sum(urna_actual.values())
    
    # Aquí almacenaremos nuestra probabilidad final (empieza en 1.0 para poder multiplicar)
    probabilidad_conjunta = 1.0
    
    # Lista para guardar los pasos y mostrarlos después
    pasos_explicados = []

    # Aplicamos la Regla de la Cadena iterando por cada evento en la secuencia
    for paso, evento in enumerate(secuencia_deseada):
        
        # 1. Verificamos si es posible que ocurra el evento
        if urna_actual.get(evento, 0) == 0:
            pasos_explicados.append(f"Paso {paso + 1}: Imposible sacar '{evento}'. Probabilidad = 0")
            return 0.0, pasos_explicados
            
        # 2. Calculamos la probabilidad condicional del evento actual
        # P(Evento_actual | Eventos_anteriores)
        prob_actual = urna_actual[evento] / total_elementos
        
        # Guardamos la explicación del cálculo
        contexto = "Inicio" if paso == 0 else f"Dado lo anterior"
        pasos_explicados.append(
            f"Paso {paso + 1} ({contexto}): P({evento}) = {urna_actual[evento]}/{total_elementos} = {prob_actual:.4f}"
        )
        
        # 3. Multiplicamos la probabilidad al total acumulado (La esencia de la Regla de la Cadena)
        probabilidad_conjunta *= prob_actual
        
        # 4. Actualizamos "el mundo" basado en el evento que acaba de ocurrir
        # (Esto representa la condición para el siguiente evento)
        urna_actual[evento] -= 1
        total_elementos -= 1
        
    return probabilidad_conjunta, pasos_explicados

# =====================================================================
# EJEMPLO DE USO
# =====================================================================
if __name__ == "__main__":
    # Definimos nuestro estado inicial (El universo de posibilidades)
    # Total de canicas: 10
    urna_de_canicas = {
        'Rojo': 5,
        'Azul': 3,
        'Verde': 2
    }
    
    # La secuencia exacta que queremos predecir
    # ¿Qué probabilidad hay de sacar Rojo, luego Azul, y luego Rojo otra vez?
    secuencia_objetivo = ['Rojo', 'Azul', 'Rojo']
    
    print("--- ESTADO INICIAL ---")
    print(f"Urna: {urna_de_canicas}")
    print(f"Secuencia a evaluar: {secuencia_objetivo}\n")
    
    # Ejecutamos nuestro algoritmo
    print("--- APLICANDO LA REGLA DE LA CADENA ---")
    prob_final, detalles_pasos = calcular_probabilidad_secuencia(urna_de_canicas, secuencia_objetivo)
    
    # Mostramos el desglose matemático
    for detalle in detalles_pasos:
        print(detalle)
        
    print("\n--- RESULTADO FINAL ---")
    # P(R1, A2, R3) = P(R1) * P(A2|R1) * P(R3|R1,A2)
    print(f"La probabilidad conjunta exacta de la secuencia es: {prob_final:.6f} (o {prob_final * 100:.2f}%)")
