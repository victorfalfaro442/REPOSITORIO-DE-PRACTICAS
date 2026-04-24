"""
=================================================================
PSEUDOCÓDIGO: VALOR DE LA INFORMACIÓN PERFECTA (VPI)
=================================================================
FUNCIÓN calcular_vpi():
    # FASE 1: Calcular Utilidad Esperada a ciegas (Conocimiento actual)
    eu_actual = MAX_a( SUM_s( P(s) * U(a, s) ) )

    # FASE 2: Calcular Utilidad Esperada si fuéramos clarividentes
    eu_con_info_perfecta = 0
    PARA CADA estado EN estados_del_entorno:
        prob_de_que_ocurra_este_estado = OBTENER_PROBABILIDAD(estado)
        
        # Si supiéramos que este estado va a ocurrir al 100%, elegiríamos la mejor acción
        mejor_recompensa = MAX_a( U(a, estado) )
        
        # Ponderamos esa ganancia perfecta por la probabilidad de que ocurra
        eu_con_info_perfecta += (prob_de_que_ocurra_este_estado * mejor_recompensa)

    # FASE 3: La diferencia matemática
    vpi = eu_con_info_perfecta - eu_actual
    RETORNAR vpi
=================================================================
"""

# Entorno Original
decisiones = ['Llevar Paraguas', 'Dejar Paraguas']
estados_clima = ['Lluvia', 'Sol']
probabilidad_clima = {'Lluvia': 0.70, 'Sol': 0.30}

utilidades = {
    ('Llevar Paraguas', 'Lluvia'): 5,
    ('Llevar Paraguas', 'Sol'):   -2,
    ('Dejar Paraguas', 'Lluvia'): -10,
    ('Dejar Paraguas', 'Sol'):    10
}

def calcular_valor_informacion():
    print("--- 1. CALCULANDO EL MUNDO ACTUAL (Sin Información) ---")
    utilidad_maxima_actual = float('-inf')
    
    for decision in decisiones:
        eu_actual = sum(probabilidad_clima[clima] * utilidades[(decision, clima)] for clima in estados_clima)
        if eu_actual > utilidad_maxima_actual:
            utilidad_maxima_actual = eu_actual
            
    print(f"Utilidad Esperada actual: {utilidad_maxima_actual:.2f}")

    print("\n--- 2. CALCULANDO EL MUNDO CON INFORMACIÓN PERFECTA ---")
    utilidad_esperada_con_info = 0
    
    for clima in estados_clima:
        utilidad_maxima_sabiendo_clima = float('-inf')
        
        for decision in decisiones:
            recompensa = utilidades[(decision, clima)]
            if recompensa > utilidad_maxima_sabiendo_clima:
                utilidad_maxima_sabiendo_clima = recompensa
                
        aporte_al_total = probabilidad_clima[clima] * utilidad_maxima_sabiendo_clima
        utilidad_esperada_con_info += aporte_al_total
        print(f"Si el reporte dice '{clima}', la mejor decisión da {utilidad_maxima_sabiendo_clima}. Aporta: {aporte_al_total:.2f}")

    print(f"\nUtilidad Esperada CON Info Perfecta: {utilidad_esperada_con_info:.2f}")

    print("\n--- 3. EL VALOR DE LA INFORMACIÓN (VPI) ---")
    vpi = utilidad_esperada_con_info - utilidad_maxima_actual
    print(f"VPI = {utilidad_esperada_con_info:.2f} - {utilidad_maxima_actual:.2f} = {vpi:.2f} puntos.")
    
    return vpi

# Ejecución
valor_reporte = calcular_valor_informacion()