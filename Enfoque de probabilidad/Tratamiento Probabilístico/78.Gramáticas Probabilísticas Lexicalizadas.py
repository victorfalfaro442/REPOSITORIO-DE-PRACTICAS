import random

print("--- GRAMÁTICAS PROBABILÍSTICAS LEXICALIZADAS ---")

# ==============================================================
# 1. GRAMÁTICA LEXICALIZADA (Reglas condicionadas por el núcleo)
# ==============================================================
# Formato: Categoria_Sintactica : { Palabra_Nucleo : [(Prob, [ (Cat_Hijo, Nucleo_Hijo), ... ])] }

gramatica_lexicalizada = {
    "O": {
        # La oración hereda el verbo como su núcleo principal
        "come":   [(1.0, [("SN", "gato"), ("SV", "come")])],
        "duerme": [(1.0, [("SN", "perro"), ("SV", "duerme")])]
    },
    
    "SV": {
        # Si el núcleo es "come", es 90% probable que pida un objeto (SN)
        "come": [
            (0.9, [("V", "come"), ("SN", "pescado")]),
            (0.1, [("V", "come")]) # "el gato come" (sin objeto, menos probable)
        ],
        # Si el núcleo es "duerme", es 95% probable que NO lleve objeto
        "duerme": [
            (0.95, [("V", "duerme")]),
            (0.05, [("V", "duerme"), ("SN", "cama")]) # "duerme la cama" (raro gramaticalmente)
        ]
    },
    
    "SN": {
        "gato":    [(1.0, [("Det", "el"), ("N", "gato")])],
        "perro":   [(1.0, [("Det", "un"), ("N", "perro")])],
        "pescado": [(1.0, [("N", "pescado")])],
        "cama":    [(1.0, [("Det", "la"), ("N", "cama")])]
    },
    
    # Reglas terminales (Léxico final)
    "Det": { "el": [(1.0, ["el"])], "un": [(1.0, ["un"])], "la": [(1.0, ["la"])] },
    "N":   { "gato": [(1.0, ["gato"])], "perro": [(1.0, ["perro"])], "pescado": [(1.0, ["pescado"])], "cama": [(1.0, ["cama"])] },
    "V":   { "come": [(1.0, ["come"])], "duerme": [(1.0, ["duerme"])] }
}

# ==============================================================
# 2. MOTOR DE EXPANSIÓN LEXICALIZADA
# ==============================================================
def expandir_nodo_lexicalizado(categoria, nucleo):
    """Expande el árbol considerando no solo la sintaxis, sino la palabra núcleo."""
    
    # Si llegamos a una palabra terminal (string plano), la retornamos
    if categoria not in gramatica_lexicalizada:
        return nucleo
        
    # Buscamos las reglas específicas para ESTA categoría y ESTE núcleo
    opciones = gramatica_lexicalizada[categoria][nucleo]
    probabilidades = [op[0] for op in opciones]
    expansiones = [op[1] for op in opciones]
    
    # Elegimos basados en la probabilidad estadística
    regla_elegida = random.choices(expansiones, weights=probabilidades)[0]
    
    # Si la regla elegida es una palabra final (ej. ["el"])
    if isinstance(regla_elegida[0], str):
        return regla_elegida[0]
        
    # Expandimos los nodos hijos
    resultado = []
    for sub_categoria, sub_nucleo in regla_elegida:
        resultado.append(expandir_nodo_lexicalizado(sub_categoria, sub_nucleo))
        
    return " ".join(resultado)

# ==============================================================
# 3. PRUEBA DE GENERACIÓN INTELIGENTE
# ==============================================================
print("\n[*] GENERANDO ORACIONES BASADAS EN EL NÚCLEO VERBAL:")
print("-" * 60)

# Forzamos la generación con el verbo "come"
print("Generando con núcleo transitivo ('come'):")
for _ in range(3):
    print("  ->", expandir_nodo_lexicalizado("O", "come"))

print("\nGenerando con núcleo intransitivo ('duerme'):")
for _ in range(3):
    print("  ->", expandir_nodo_lexicalizado("O", "duerme"))
