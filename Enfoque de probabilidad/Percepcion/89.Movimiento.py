from PIL import Image, ImageDraw

print("--- PERCEPCIÓN DINÁMICA: DETECCIÓN DE MOVIMIENTO ---")

# ==============================================================
# 1. SIMULACIÓN DE VIDEO (Crear dos fotogramas consecutivos)
# ==============================================================
ancho = 200
alto = 100

# Fotograma 1 (Tiempo: T-1) -> El objeto está a la izquierda
fotograma_1 = Image.new("L", (ancho, alto), "black")
dibujo_1 = ImageDraw.Draw(fotograma_1)
dibujo_1.rectangle([20, 40, 60, 60], fill="white") # Objeto inicial

# Fotograma 2 (Tiempo: T) -> El objeto se movió a la derecha
fotograma_2 = Image.new("L", (ancho, alto), "black")
dibujo_2 = ImageDraw.Draw(fotograma_2)
dibujo_2.rectangle([50, 40, 90, 60], fill="white") # Nueva posición

fotograma_1.save("1_fotograma_anterior.png")
fotograma_2.save("2_fotograma_actual.png")
print("[*] Fotogramas generados simulando el paso del tiempo.")

# ==============================================================
# 2. ALGORITMO DE DIFERENCIA DE FOTOGRAMAS
# ==============================================================
pix_1 = fotograma_1.load()
pix_2 = fotograma_2.load()

imagen_movimiento = Image.new("L", (ancho, alto), "black")
pix_mov = imagen_movimiento.load()

UMBRAL = 50 # Ignoramos pequeños cambios de luz
print("[*] Calculando la diferencia absoluta entre fotogramas...")

for x in range(ancho):
    for y in range(alto):
        # 1. Extraemos el valor del píxel en ambos momentos
        val_anterior = pix_1[x, y]
        val_actual = pix_2[x, y]
        
        # 2. Matemática del movimiento: Diferencia Absoluta
        diferencia = abs(val_actual - val_anterior)
        
        # 3. Segmentación (Limpiar el ruido)
        if diferencia > UMBRAL:
            pix_mov[x, y] = 255 # ¡ALERTA! Hubo movimiento aquí
        else:
            pix_mov[x, y] = 0   # Todo está tranquilo

# ==============================================================
# 3. GUARDAR Y MOSTRAR
# ==============================================================
imagen_movimiento.save("3_mapa_de_movimiento.png")
print("[*] ¡Movimiento detectado con éxito!")

# Mostramos el "antes", el "después" y la "huella" del movimiento
fotograma_1.show(title="Tiempo 1")
fotograma_2.show(title="Tiempo 2")
imagen_movimiento.show(title="Huella de Movimiento")
