import random

print("--- APRENDIZAJE POR REFUERZO PASIVO (TD LEARNING) ---")

# 1. EL ENTORNO OCULTO (El Motor Físico)
estados = ['Inicio', 'Hielo', 'Tesoro', 'Trampa']
estados_terminales = ['Tesoro', 'Trampa']

def dar_un_paso(estado, accion):
    """El universo: La IA no conoce estas probabilidades ni recompensas."""
    if estado == 'Inicio':
        if accion == 'Avanzar':
            return ('Hielo', -1) if random.random() < 0.9 else ('Inicio', -1)
    elif estado == 'Hielo':
        if accion == 'Avanzar':
            return ('Tesoro', 100) if random.random() < 0.7 else ('Trampa', -100)
    return (estado, 0)

# 2. La IA está obligada a seguir este manual. No puede explorar otras acciones.
politica_fija = {
    'Inicio': 'Avanzar',
    'Hielo': 'Avanzar'
}

# 3. EL CEREBRO DE LA IA (Tabla de Utilidades)
# Empieza en cero. Aquí registrará qué tan bueno es cada estado.
U = {s: 0.0 for s in estados}

# Hiperparámetros
alfa = 0.1   # Tasa de aprendizaje
gamma = 0.9  # Factor de descuento
episodios = 1000

# 4. EL BUCLE DE APRENDIZAJE PASIVO
for episodio in range(1, episodios + 1):
    estado_actual = 'Inicio'
    
    while estado_actual not in estados_terminales:
        # A) La IA mira su manual y ejecuta la acción dictada
        accion = politica_fija[estado_actual]
        
        # B) El universo responde
        nuevo_estado, recompensa_inmediata = dar_un_paso(estado_actual, accion)
        
        # C) APRENDIZAJE TD (Diferencia Temporal)
        # Si llegamos a una meta, su valor futuro es 0 (porque ahí termina todo)
        utilidad_futura = U[nuevo_estado] if nuevo_estado not in estados_terminales else 0.0
        
        # La diferencia entre lo que experimentamos y lo que esperábamos
        diferencia_temporal = recompensa_inmediata + (gamma * utilidad_futura) - U[estado_actual]
        
        # Actualizamos la creencia del estado que acabamos de dejar
        U[estado_actual] = U[estado_actual] + (alfa * diferencia_temporal)
        
        # Si llegamos a un estado terminal, debemos registrar su valor puro
        if nuevo_estado in estados_terminales:
            U[nuevo_estado] = recompensa_inmediata
            
        # D) Avanzamos
        estado_actual = nuevo_estado

    if episodio % 200 == 0:
        print(f"[*] Completados {episodio} viajes en el tren automático...")

# 5. RESULTADOS
print("\n" + "="*50)
print(" UTILIDADES APRENDIDAS DE LA POLÍTICA FIJA ")
print("="*50)
for s in estados:
    print(f"Estado '{s}': {U[s]:.2f} puntos")
