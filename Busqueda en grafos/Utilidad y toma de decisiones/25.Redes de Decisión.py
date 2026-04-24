# 1. Definimos las Opciones (Nodo de Decisión)
decisiones = ['Llevar Paraguas', 'Dejar Paraguas']

# 2. Definimos los Estados del Entorno (Nodo de Azar)
estados_clima = ['Lluvia', 'Sol']

# Hay un 70% de probabilidad de lluvia.
probabilidad_clima = {
    'Lluvia': 0.70,
    'Sol': 0.30
}

# 3. Definimos la Función de Utilidad (Nodo de Utilidad/Diamante)
# Mapea la combinación de (Decisión, Clima) -> Puntos de Felicidad
utilidades = {
    ('Llevar Paraguas', 'Lluvia'): 5,   # Te salvaste, pero cargas un paraguas mojado
    ('Llevar Paraguas', 'Sol'):   -2,   # Cargas un paraguas inútil todo el día
    ('Dejar Paraguas', 'Lluvia'): -10,  # ¡Desastre! Estás empapado
    ('Dejar Paraguas', 'Sol'):    10    # ¡Día perfecto y manos libres!
}

def evaluar_red_de_decision(evidencia_probabilidades):
    print("--- Analizando Red de Decisión ---")
    print(f"Evidencia del entorno: Lluvia al {evidencia_probabilidades['Lluvia']*100}%")
    print("-" * 34)
    
    utilidad_maxima = float('-inf')
    mejor_decision = None
    
    # 4. El algoritmo evalúa cada decisión posible
    for decision in decisiones:
        utilidad_esperada = 0
        print(f"\n[Evaluando nodo de decisión: '{decision}']")
        
        # 5. Calculamos la sumatoria de probabilidades x utilidades
        for clima in estados_clima:
            probabilidad = evidencia_probabilidades[clima]
            recompensa = utilidades[(decision, clima)]
            
            # EU = P(s) * U(s, a)
            valor_parcial = probabilidad * recompensa
            utilidad_esperada += valor_parcial
            
            print(f"  -> Si hace {clima} (Prob: {probabilidad}): Utilidad {recompensa} -> Aporta: {valor_parcial:.2f}")
            
        print(f"  [*] Utilidad Esperada Total para '{decision}': {utilidad_esperada:.2f}")
        
        # 6. Nos quedamos con la decisión que dé el mayor número
        if utilidad_esperada > utilidad_maxima:
            utilidad_maxima = utilidad_esperada
            mejor_decision = decision
            
    return mejor_decision, utilidad_maxima

# --- PRUEBA DEL CÓDIGO ---
decision_final, puntos_esperados = evaluar_red_de_decision(probabilidad_clima)

print("\n" + "=" * 40)
print(" 🤖 RESULTADO DE LA RED DE DECISIÓN ")
print("=" * 40)
print(f"La IA ha decidido: {decision_final.upper()}")
print(f"Con una utilidad matemática proyectada de: {puntos_esperados:.2f} puntos.")

# Ejecutamos la explicación
explicar_teoria_utilidad()