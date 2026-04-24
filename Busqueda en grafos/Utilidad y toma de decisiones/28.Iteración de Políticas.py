# 1. Componentes del Entorno (Idéntico al anterior)
estados = ['Inicio', 'Hielo', 'Tesoro', 'Trampa']
recompensas = {'Inicio': -1, 'Hielo': -1, 'Tesoro': 100, 'Trampa': -100}
estados_terminales = ['Tesoro', 'Trampa']
acciones = ['Avanzar', 'Retroceder']

transiciones = {
    'Inicio': {
        'Avanzar': [(0.9, 'Hielo'), (0.1, 'Inicio')],
        'Retroceder': [(1.0, 'Inicio')]
    },
    'Hielo': {
        'Avanzar': [(0.7, 'Tesoro'), (0.3, 'Trampa')],
        'Retroceder': [(1.0, 'Inicio')]
    }
}

gamma = 0.9

def evaluacion_de_politica(politica, U):
    """Calcula el valor de seguir estrictamente la política actual."""
    # Hacemos unas cuantas pasadas rápidas para estimar los valores (Evaluación iterativa)
    for _ in range(20):
        U_nueva = U.copy()
        for s in estados:
            if s in estados_terminales:
                U_nueva[s] = recompensas[s]
                continue
            
            # Simplemente tomamos la acción que dicta la política
            accion_dictada = politica[s]
            utilidad_esperada = sum(prob * U[s_destino] for prob, s_destino in transiciones[s][accion_dictada])
            
            U_nueva[s] = recompensas[s] + (gamma * utilidad_esperada)
        U = U_nueva
    return U

def iteracion_de_politicas():
    print("--- INICIANDO ITERACIÓN DE POLÍTICAS ---")
    
    # 1. Empezamos con un manual de instrucciones al azar (Política Inicial)
    politica = {'Inicio': 'Retroceder', 'Hielo': 'Retroceder', 'Tesoro': None, 'Trampa': None}
    U = {s: 0.0 for s in estados}
    
    iteracion = 1
    
    while True:
        print(f"\n[Iteración {iteracion}]")
        print(f"Manual actual: Inicio -> {politica['Inicio']}, Hielo -> {politica['Hielo']}")
        
        # FASE 1: EVALUACIÓN
        # ¿Qué tan bueno es este manual de instrucciones?
        U = evaluacion_de_politica(politica, U)
        print("  -> Valores evaluados: " + ", ".join([f"{k}: {v:.1f}" for k,v in U.items() if k not in estados_terminales]))
        
        # FASE 2: MEJORA
        politica_estable = True # Asumimos que el manual es perfecto hasta que se demuestre lo contrario
        
        for s in estados:
            if s in estados_terminales:
                continue
                
            accion_actual = politica[s]
            mejor_accion = None
            max_valor = float('-inf')
            
            # Miramos si hay una acción mejor que la que dicta el manual
            for a in acciones:
                valor_accion = sum(prob * U[s_destino] for prob, s_destino in transiciones[s][a])
                if valor_accion > max_valor:
                    max_valor = valor_accion
                    mejor_accion = a
                    
            # Si encontramos una acción mejor, corregimos el manual
            if mejor_accion != accion_actual:
                politica[s] = mejor_accion
                politica_estable = False
                print(f"  [*] ¡Mejora! En '{s}', cambiar '{accion_actual}' por '{mejor_accion}' es matemáticamente superior.")
                
        if politica_estable:
            print(f"\n[*] ÉXITO: El manual de instrucciones ya no puede mejorarse.")
            break
            
        iteracion += 1
        
    return politica, U

# --- PRUEBA DEL CÓDIGO ---
politica_final, utilidades_finales = iteracion_de_politicas()

print("\n" + "="*50)
print(" RESULTADO FINAL: LA POLÍTICA ÓPTIMA ")
print("="*50)
for estado in ['Inicio', 'Hielo']:
    print(f" Si estás en '{estado}' -> ¡Debes {politica_final[estado].upper()}!")