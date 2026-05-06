import re

print("--- EXTRACCIÓN DE INFORMACIÓN (NER Y RELACIONES) ---")

# ==============================================================
# 1. BASES DE CONOCIMIENTO (Gacetas o Gazetteers)
# ==============================================================
# En la vida real, estas son listas gigantescas de bases de datos
entidades_conocidas = {
    "PER": ["Elon Musk", "Ada Lovelace", "Alan Turing", "Bill Gates"],
    "ORG": ["SpaceX", "Microsoft", "Universidad de Cambridge", "Tesla"],
    "LOC": ["California", "Londres", "Texas", "Reino Unido"]
}

# Verbos o frases que indican una relación entre entidades
patrones_relacion = {
    "FUNDO_A": ["fundó", "creó", "es fundador de", "inició"],
    "UBICADO_EN": ["ubicado en", "con sede en", "situada en", "en"]
}

# ==============================================================
# 2. MOTOR DE RECONOCIMIENTO DE ENTIDADES (NER)
# ==============================================================
def extraer_entidades(texto):
    entidades_encontradas = []
    
    # Buscamos coincidencias de nuestras entidades en el texto
    for tipo, lista_nombres in entidades_conocidas.items():
        for nombre in lista_nombres:
            # Usamos regex para encontrar la palabra exacta en el texto
            if re.search(rf'\b{nombre}\b', texto):
                entidades_encontradas.append({
                    "entidad": nombre,
                    "tipo": tipo
                })
                
    # Ordenamos por aparición en el texto para mantener la secuencia
    entidades_encontradas.sort(key=lambda x: texto.find(x["entidad"]))
    return entidades_encontradas

# ==============================================================
# 3. MOTOR DE EXTRACCIÓN DE RELACIONES (RE)
# ==============================================================
def extraer_relaciones(texto, entidades):
    relaciones_encontradas = []
    
    # Si no hay al menos 2 entidades, no puede haber relaciones
    if len(entidades) < 2:
        return relaciones_encontradas

    # Buscamos relaciones tipo: [PER] fundó [ORG]
    for i in range(len(entidades) - 1):
        ent_origen = entidades[i]
        ent_destino = entidades[i+1]
        
        # Extraemos el fragmento de texto que hay ENTRE las dos entidades
        inicio_texto = texto.find(ent_origen["entidad"]) + len(ent_origen["entidad"])
        fin_texto = texto.find(ent_destino["entidad"])
        contexto_intermedio = texto[inicio_texto:fin_texto].strip().lower()
        
        # Evaluamos el contexto contra nuestros patrones
        for tipo_relacion, frases in patrones_relacion.items():
            for frase in frases:
                if frase in contexto_intermedio:
                    # Validamos la lógica (Persona funda Organización)
                    if tipo_relacion == "FUNDO_A" and ent_origen["tipo"] == "PER" and ent_destino["tipo"] == "ORG":
                        relaciones_encontradas.append((ent_origen["entidad"], "FUNDADOR_DE", ent_destino["entidad"]))
                        
                    # Validamos la lógica (Organización ubicada en Ubicación)
                    elif tipo_relacion == "UBICADO_EN" and ent_origen["tipo"] == "ORG" and ent_destino["tipo"] == "LOC":
                        relaciones_encontradas.append((ent_origen["entidad"], "UBICADO_EN", ent_destino["entidad"]))

    return relaciones_encontradas

# ==============================================================
# 4. PRUEBA DEL SISTEMA
# ==============================================================
texto_prueba = "El empresario Elon Musk fundó SpaceX en California durante el año 2002. " \
               "Años antes, el famoso Alan Turing estudió en la Universidad de Cambridge, " \
               "ubicada en el Reino Unido."

print("\n[*] PROCESANDO TEXTO NO ESTRUCTURADO:")
print(f"'{texto_prueba}'\n")

# Paso 1: Extraer Entidades (NER)
entidades = extraer_entidades(texto_prueba)
print("[*] 1. ENTIDADES RECONOCIDAS (NER):")
for e in entidades:
    print(f"  -> [{e['tipo']}] {e['entidad']}")

# Paso 2: Extraer Relaciones (RE)
relaciones = extraer_relaciones(texto_prueba, entidades)
print("\n[*] 2. RELACIONES EXTRAÍDAS (Tripletas de Conocimiento):")
if relaciones:
    for r in relaciones:
        print(f"  -> HECHO: ( {r[0]} ) ---> [ {r[1]} ] ---> ( {r[2]} )")
else:
    print("  -> No se encontraron relaciones lógicas.")
