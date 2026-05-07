from PIL import Image

print("--- PREPROCESADO: FILTROS Y CONVOLUCIÓN ---")

# ==============================================================
# 1. CREAR UNA IMAGEN DE PRUEBA (Un cuadrado blanco sobre negro)
# ==============================================================
tamaño = 100
# "L" significa "Luminosidad" (Escala de grises: 0 es negro, 255 es blanco)
imagen_original = Image.new("L", (tamaño, tamaño), color=0)
pixeles = imagen_original.load()

# Dibujamos un cuadrado blanco en el centro
for x in range(30, 70):
    for y in range(30, 70):
        pixeles[x, y] = 255

# Guardamos la imagen original para comparar
imagen_original.save("1_original.png")
print("[*] Imagen original creada ('1_original.png').")

# ==============================================================
# 2. DEFINIR EL KERNEL (El Filtro Matemático)
# ==============================================================
# Este es un clásico Kernel de Detección de Bordes (Laplaciano).
# Suma los valores de alrededor y los resta al centro. Si todo es
# de un mismo color, el resultado da 0 (negro). Si hay un cambio
# brusco de color, el resultado se dispara (blanco).
kernel_bordes = [
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
]

# ==============================================================
# 3. EL ALGORITMO DE CONVOLUCIÓN
# ==============================================================
imagen_filtrada = Image.new("L", (tamaño, tamaño), color=0)
pixeles_filtrados = imagen_filtrada.load()

print("[*] Aplicando el Filtro de Convolución (Detección de Bordes)...")

# Recorremos la imagen (ignoramos los píxeles del borde exterior 
# para que el kernel de 3x3 no se salga de los límites)
for x in range(1, tamaño - 1):
    for y in range(1, tamaño - 1):
        
        suma_convolucion = 0
        
        # Deslizamos el Kernel de 3x3 sobre los vecinos del píxel actual
        for i in range(3):
            for j in range(3):
                # Extraemos el color del píxel de la imagen original
                # (Desplazamos -1 para centrar la cuadrícula de 3x3 en x,y)
                color_pixel = pixeles[x + i - 1, y + j - 1]
                
                # Multiplicamos por el valor correspondiente en el Kernel
                valor_kernel = kernel_bordes[i][j]
                
                suma_convolucion += color_pixel * valor_kernel
                
        # Aseguramos que el resultado no se salga del rango 0 a 255
        nuevo_color = int(max(0, min(suma_convolucion, 255)))
        
        # Guardamos el resultado en la nueva imagen
        pixeles_filtrados[x, y] = nuevo_color

# ==============================================================
# 4. GUARDAR EL RESULTADO
# ==============================================================
imagen_filtrada.save("2_filtrada.png")
print("[*] ¡Proceso terminado! Resultado guardado en '2_filtrada.png'.")
