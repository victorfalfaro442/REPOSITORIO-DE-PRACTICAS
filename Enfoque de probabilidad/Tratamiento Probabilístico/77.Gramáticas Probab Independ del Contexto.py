import random

print("--- GRAMÁTICAS PROBABILÍSTICAS (PCFG) ---")

# ==============================================================
# 1. DEFINICIÓN DE LA GRAMÁTICA Y PROBABILIDADES
# ==============================================================
# Formato: NoTerminal : [(Probabilidad, [Expansión]), ...]
# IMPORTANTE: Las probabilidades de cada bloque deben sumar 1.0

pcfg = {
    # Reglas Estructurales
    "O":  [ (1.0, ["SN", "SV"]) ],                 # Oración -> Sintagma Nominal + Sintagma Verbal
    
    "SN": [ (0.6, ["Det", "N"]),                   # Sintagma Nominal simple (ej. "el gato")
            (0.4, ["Det", "N", "SPrep"]) ],        # Sintagma Nominal con preposición (ej. "el gato con collar")
            
    "SV": [ (0.5, ["V", "SN"]),                    # Sintagma Verbal transitivo (ej. "ve al perro")
            (0.3, ["V"]),                          # Sintagma Verbal intransitivo (ej. "duerme")
            (0.2, ["V", "SN", "SPrep"]) ],         # Verbo + Objeto + Preposición
            
    "SPrep": [(1.0, ["Prep", "SN"]) ],             # Sintagma Preposicional -> Preposición + Sintagma Nominal
    
    # Reglas Léxicas (El vocabulario)
    "Det":  [ (0.5, ["el"]), (0.3, ["un"]), (0.2, ["aquel"]) ],
    "N":    [ (0.4, ["astrónomo"]), (0.4, ["perro"]), (0.2, ["telescopio"]) ],
    "V":    [ (0.5, ["observa"]), (0.3, ["persigue"]), (0.2, ["duerme"]) ],
    "Prep": [ (0.7, ["con"]), (0.3, ["en"]) ]
}

# ==============================================================
# 2. MOTOR DE EXPANSIÓN RECURSIVA
# ==============================================================
def expandir_nodo(simbolo):
    """Expande un símbolo recursivamente bajando por el árbol sintáctico."""
    
    # Condición de parada: si es una palabra final (terminal), la devolvemos
    if simbolo not in pcfg:
        return simbolo

    # Extraemos las opciones y sus probabilidades para este símbolo no terminal
    opciones = pcfg[simbolo]
    probabilidades = [opcion[0] for opcion in opciones]
    expansiones = [opcion[1] for opcion in opciones]
    
    # Elegimos una regla basándonos en la probabilidad estadística
    regla_elegida = random.choices(expansiones, weights=probabilidades)[0]
    
    # Expandimos recursivamente cada parte de la regla elegida
    resultado = []
    for sub_simbolo in regla_elegida:
        resultado.append(expandir_nodo(sub_simbolo))
        
    # Unimos las palabras resultantes
    return " ".join(resultado)

# ==============================================================
# 3. GENERACIÓN DE ORACIONES
# ==============================================================
print("\n[*] GENERANDO ORACIONES SINTÁCTICAMENTE CORRECTAS:")
print("-" * 55)

for i in range(5):
    # Siempre empezamos por la raíz del árbol: la Oración ("O")
    oracion_generada = expandir_nodo("O")
    print(f"Árbol {i+1} -> {oracion_generada}")
