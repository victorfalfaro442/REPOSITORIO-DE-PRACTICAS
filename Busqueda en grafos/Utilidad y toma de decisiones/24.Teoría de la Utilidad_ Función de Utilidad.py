def explicar_teoria_utilidad():
    print("=" * 65)
    print(" 🧠 TEORÍA DE LA UTILIDAD: TOMA DE DECISIONES EN IA ")
    print("=" * 65)
    
    print("\n1. ¿QUÉ ES LA FUNCIÓN DE UTILIDAD U(s)?")
    print("   Es el 'medidor de felicidad' de la IA.")
    print("   Si un estado 'A' es mejor que un estado 'B', entonces U(A) > U(B).")
    print("   Por ejemplo, para un robot de limpieza:")
    print("   - U(Batería al 100%) = 10")
    print("   - U(Batería al 0%) = -100 (Desastre)")

    print("\n2. EL PROBLEMA: LA INCERTIDUMBRE")
    print("   En el mundo real, las acciones no siempre salen como queremos.")
    print("   Si el robot cruza un charco para llegar más rápido a su cargador,")
    print("   hay un 80% de probabilidad de cruzar, pero un 20% de resbalar y caer.")

    print("\n3. LA SOLUCIÓN: LA UTILIDAD ESPERADA (Expected Utility)")
    print("   La IA multiplica la recompensa de cada resultado por su probabilidad,")
    print("   y suma todo para ver qué acción le conviene más a largo plazo.\n")
    
    print("-" * 65)
    print(" ⚙️  SIMULANDO EL CEREBRO DE LA IA (Cálculo de Utilidad) ")
    print("-" * 65)

    # Definimos dos acciones posibles:
    # Acción 1: Inversión Segura (100% de ganar $50)
    # Acción 2: Inversión Riesgosa (50% de ganar $200, 50% de perder $50)

    # Las Utilidades (U) son simplemente el dinero ganado/perdido
    u_ganar_seguro = 50
    u_ganar_riesgo = 200
    u_perder_riesgo = -50

    # Probabilidades (P)
    p_seguro = 1.0
    p_riesgo_exito = 0.5
    p_riesgo_falla = 0.5

    # Calculamos la Utilidad Esperada (EU)
    eu_accion_segura = (p_seguro * u_ganar_seguro)
    eu_accion_riesgosa = (p_riesgo_exito * u_ganar_riesgo) + (p_riesgo_falla * u_perder_riesgo)

    print("Situación: La IA tiene $100 y debe elegir una inversión.")
    
    print("\n[Evaluando Acción A: Inversión Segura]")
    print(f"  -> Probabilidad 100% de ganar $50")
    print(f"  -> Utilidad Esperada: {eu_accion_segura} puntos.")

    print("\n[Evaluando Acción B: Inversión Riesgosa]")
    print(f"  -> Probabilidad 50% de ganar $200")
    print(f"  -> Probabilidad 50% de perder $50")
    print(f"  -> Cálculo: (0.5 * 200) + (0.5 * -50)")
    print(f"  -> Utilidad Esperada: {eu_accion_riesgosa} puntos.")

    print("\n4. LA TOMA DE DECISIÓN RACIONAL")
    print("   El Principio de Utilidad Máxima Esperada dicta que la IA")
    print("   SIEMPRE debe elegir la acción con el número mayor.")
    
    if eu_accion_riesgosa > eu_accion_segura:
        print(f"\n   [Decisión Tomada] -> La IA elige la Acción B (Inversión Riesgosa).")
        print("   Aunque puede perder, matemáticamente el riesgo vale la pena.")
    else:
        print(f"\n   [Decisión Tomada] -> La IA elige la Acción A (Inversión Segura).")

    print("\n" + "=" * 65)
    print(" ¡Así es como una IA sopesa el riesgo contra la recompensa! ")
    print("=" * 65)

# Ejecutamos la explicación
explicar_teoria_utilidad()