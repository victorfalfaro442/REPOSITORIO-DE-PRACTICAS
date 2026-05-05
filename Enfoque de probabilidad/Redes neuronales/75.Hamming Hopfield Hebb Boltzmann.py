import random

print("--- RED DE HOPFIELD: MEMORIA ASOCIATIVA ---")

# ==============================================================
# 1. EL RECUERDO A MEMORIZAR (Una letra 'T' de 3x3)
# ==============================================================
# T: 1 1 1
#   -1 1 -1
#   -1 1 -1
patron_T = [
     1,  1,  1,
    -1,  1, -1,
    -1,  1, -1
]

n_neuronas = len(patron_T)

# ==============================================================
# 2. APRENDIZAJE HEBBIANO (Creando las conexiones)
# ==============================================================
# Matriz de pesos W de tamaño NxN (9x9)
W = [[0.0 for _ in range(n_neuronas)] for _ in range(n_neuronas)]

print("[*] Aplicando Regla de Hebb para memorizar la 'T'...")
for i in range(n_neuronas):
    for j in range(n_neuronas):
        if i == j:
            W[i][j] = 0.0 # Una neurona no se conecta consigo misma
        else:
            # Regla de Hebb: Multiplicamos los estados
            W[i][j] = patron_T[i] * patron_T[j] / n_neuronas

# ==============================================================
# 3. EL EXPERIMENTO: RECONSTRUCCIÓN DE MEMORIA
# ==============================================================
# Introducimos un recuerdo dañado (Volteamos 2 píxeles de la 'T')
# Dañado: 
#   -1  1  1  (Falta la esquina superior izquierda)
#   -1 -1 -1  (Centro borrado)
#   -1  1 -1
recuerdo_danado = [
    -1,  1,  1,
    -1, -1, -1,
    -1,  1, -1
]

def imprimir_patron(patron, titulo):
    print(f"\n{titulo}:")
    for i in range(0, 9, 3):
        fila = ["X" if p == 1 else "." for p in patron[i:i+3]]
        print("  " + " ".join(fila))

imprimir_patron(patron_T, "PATRÓN ORIGINAL (Lo que sabe la red)")
imprimir_patron(recuerdo_danado, "ENTRADA DAÑADA (Lo que ve la red hoy)")

print("\n[*] Iniciando dinámica de relajación (Recuperando recuerdo)...")
estado_actual = list(recuerdo_danado)
epocas = 5

for epoca in range(epocas):
    cambios = 0
    # En Hopfield, las neuronas se actualizan de forma asíncrona (una por una al azar)
    orden_actualizacion = list(range(n_neuronas))
    random.shuffle(orden_actualizacion)
    
    for i in orden_actualizacion:
        # Suma de la influencia de todas las vecinas
        suma_influencia = sum(W[i][j] * estado_actual[j] for j in range(n_neuronas))
        
        # Función de activación escalón (signo)
        nuevo_estado = 1 if suma_influencia >= 0 else -1
        
        if nuevo_estado != estado_actual[i]:
            estado_actual[i] = nuevo_estado
            cambios += 1
            
    print(f"  -> Iteración {epoca + 1}: {cambios} neuronas cambiaron de estado.")
    
    # Si ninguna neurona cambió, caímos en el mínimo de energía (recordamos)
    if cambios == 0:
        print("[*] ¡La red se estabilizó en un mínimo de energía!")
        break

imprimir_patron(estado_actual, "RECUERDO RECUPERADO (Salida final)")
