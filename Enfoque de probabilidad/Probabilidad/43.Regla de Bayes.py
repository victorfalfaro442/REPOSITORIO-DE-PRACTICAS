# =====================================================================
# ALGORITMO DE INFERENCIA USANDO LA REGLA DE BAYES
# =====================================================================

def aplicar_regla_de_bayes(prob_previa_A, prob_B_dado_A, prob_B_dado_no_A):
    """
    Calcula la probabilidad posterior P(A|B) usando el Teorema de Bayes.
    
    Parámetros:
    - prob_previa_A: P(A), nuestra creencia inicial (ej. prevalencia de la enfermedad).
    - prob_B_dado_A: P(B|A), la sensibilidad (ej. positivos correctos).
    - prob_B_dado_no_A: P(B|~A), la tasa de falsos positivos.
    """
    
    # 1. Calculamos P(~A), es decir, la probabilidad de NO tener 'A'
    # Si el 1% está enfermo, el 99% está sano.
    prob_previa_no_A = 1.0 - prob_previa_A
    
    # 2. Calculamos P(B), la Evidencia Total (Probabilidad de que la prueba dé positivo en general)
    # Esto ocurre en dos escenarios:
    #   Escenario 1: Estás enfermo y da positivo (Verdadero Positivo)
    verdadero_positivo = prob_B_dado_A * prob_previa_A
    
    #   Escenario 2: Estás sano pero da positivo (Falso Positivo)
    falso_positivo = prob_B_dado_no_A * prob_previa_no_A
    
    # Sumamos ambos para obtener la probabilidad total de ver un resultado positivo
    prob_total_B = verdadero_positivo + falso_positivo
    
    # 3. Aplicamos la fórmula final de Bayes: P(A|B) = P(B|A) * P(A) / P(B)
    prob_posterior_A_dado_B = verdadero_positivo / prob_total_B
    
    # Retornamos el resultado junto con algunos datos intermedios para visualización
    return {
        "prob_posterior": prob_posterior_A_dado_B,
        "prob_total_evidencia": prob_total_B,
        "falsos_positivos_totales": falso_positivo
    }

# =====================================================================
# EJEMPLO DE USO (Resolviendo el misterio médico)
# =====================================================================
if __name__ == "__main__":
    # Definimos nuestras probabilidades conocidas (Los datos del problema)
    prevalencia_enfermedad = 0.01      # P(A) = 1%
    sensibilidad_prueba = 0.99         # P(B|A) = 99%
    tasa_falso_positivo = 0.05         # P(B|~A) = 5%
    
    print("--- DATOS INICIALES ---")
    print(f"Prevalencia de la enfermedad: {prevalencia_enfermedad * 100}%")
    print(f"Efectividad de la prueba si estás enfermo: {sensibilidad_prueba * 100}%")
    print(f"Tasa de falsos positivos si estás sano: {tasa_falso_positivo * 100}%\n")
    
    # Ejecutamos nuestro "algoritmo" bayesiano
    resultados = aplicar_regla_de_bayes(
        prob_previa_A=prevalencia_enfermedad,
        prob_B_dado_A=sensibilidad_prueba,
        prob_B_dado_no_A=tasa_falso_positivo
    )
    
    # Extraemos el resultado final
    probabilidad_real = resultados["prob_posterior"] * 100
    
    print("--- RESULTADO DEL ANÁLISIS BAYESIANO ---")
    print("Un paciente acaba de dar POSITIVO en la prueba.")
    print(f"Probabilidad real de que el paciente tenga la enfermedad: {probabilidad_real:.2f}%\n")
    
    print("¿Por qué es tan baja?")
    print("Porque la enfermedad es muy rara (1%). En una población de 10,000 personas:")
    print("- 100 están enfermas. La prueba detectará correctamente a 99 de ellas.")
    print(f"- 9,900 están sanas. La prueba se equivocará en el 5%, dando {9900 * 0.05:.0f} falsos positivos.")
    print(f"Si das positivo, es más probable que seas uno de los {9900 * 0.05:.0f} sanos que uno de los 99 enfermos.")
