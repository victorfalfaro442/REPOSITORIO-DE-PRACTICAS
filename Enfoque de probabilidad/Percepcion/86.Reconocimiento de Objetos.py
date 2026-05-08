from PIL import Image, ImageDraw

print("--- RECONOCIMIENTO DE OBJETOS: TEMPLATE MATCHING ---")

# ==============================================================
# 1. CREACIÓN DE LA ESCENA Y LA PLANTILLA
# ==============================================================
# Escena principal (100x100)
escena = Image.new("RGB", (100, 100), "black")
dibujo_escena = ImageDraw.Draw(escena)

# Dibujamos varios objetos ("ruido" y el objetivo)
dibujo_escena.ellipse([10, 10, 30, 30], fill="white")    # Círculo
dibujo_escena.polygon([80, 20, 90, 40, 70, 40], fill="white") # Triángulo
dibujo_escena.rectangle([50, 60, 70, 80], fill="white")  # Cuadrado (El objetivo)

# Plantilla objetivo (20x20) - Solo el cuadrado
plantilla = Image.new("RGB", (20, 20), "black")
dibujo_plantilla = ImageDraw.Draw(plantilla)
dibujo_plantilla.rectangle([0, 0, 20, 20], fill="white")

# Guardamos para visualizar
escena.save("1_escena.png")
plantilla.save("2_plantilla.png")
print("[*] Imágenes generadas: La Escena y La Plantilla.")

# ==============================================================
# 2. ALGORITMO DE VENTANA DESLIZANTE (Template Matching)
# ==============================================================
pix_escena = escena.load()
pix_plantilla = plantilla.load()

w_escena, h_escena = escena.size
w_plant, h_plant = plantilla.size

# Variables para rastrear el mejor resultado
mejor_ssd = float('inf')
mejor_x = 0
mejor_y = 0

print(f"[*] Buscando plantilla de {w_plant}x{h_plant} en escena de {w_escena}x{h_escena}...")
print("[*] Procesando matemáticas (esto tomará un par de segundos)...")

# Deslizamos la ventana por toda la escena
for y in range(h_escena - h_plant):
    for x in range(w_escena - w_plant):
        
        ssd_actual = 0
        
        # Comparamos la plantilla con el fragmento actual de la escena
        for j in range(h_plant):
            for i in range(w_plant):
                # Tomamos solo el canal Rojo [0] porque nuestra imagen es blanco y negro (RGB son iguales)
                val_escena = pix_escena[x + i, y + j][0]
                val_plantilla = pix_plantilla[i, j][0]
                
                # Fórmula SSD: (Imagen - Plantilla)^2
                diferencia = val_escena - val_plantilla
                ssd_actual += diferencia ** 2
                
        # Si este fragmento tiene menos error que el mejor que habíamos encontrado, lo actualizamos
        if ssd_actual < mejor_ssd:
            mejor_ssd = ssd_actual
            mejor_x = x
            mejor_y = y

print(f"[*] ¡Objeto detectado! Mejor coincidencia en coordenadas: X={mejor_x}, Y={mejor_y}")

# ==============================================================
# 3. DIBUJAR LA CAJA DELIMITADORA (Bounding Box)
# ==============================================================
# Hacemos una copia para no dañar la original y dibujamos un marco rojo
resultado = escena.copy()
dibujo_resultado = ImageDraw.Draw(resultado)

# Coordenadas de la caja: [x_izq, y_sup, x_der, y_inf]
caja = [mejor_x, mejor_y, mejor_x + w_plant, mejor_y + h_plant]
dibujo_resultado.rectangle(caja, outline="red", width=2)

resultado.save("3_deteccion_final.png")
print("[*] Caja delimitadora dibujada. ¡Proceso completado!")

# Mostrar imágenes automáticamente
escena.show(title="Escena Original")
plantilla.show(title="Plantilla a buscar")
resultado.show(title="Objeto Detectado")
