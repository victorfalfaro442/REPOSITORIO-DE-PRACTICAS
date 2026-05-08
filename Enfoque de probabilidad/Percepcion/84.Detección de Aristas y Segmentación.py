import math
from PIL import Image

print("--- DETECCIÓN DE ARISTAS Y SEGMENTACIÓN (CON VISUALIZACIÓN AUTOMÁTICA) ---")

# ==============================================================
# 1. CREAR IMAGEN DE PRUEBA (Círculo con borde difuminado)
# ==============================================================
tamaño = 150
imagen_original = Image.new("L", (tamaño, tamaño), color=0)
pixeles = imagen_original.load()

centro = tamaño // 2
radio = 40

# Dibujamos un círculo suave
for x in range(tamaño):
    for y in range(tamaño):
        distancia = math.sqrt((x - centro)**2 + (y - centro)**2)
        if distancia <= radio:
            pixeles[x, y] = 255
        elif distancia <= radio + 10:
            # Creamos un gradiente/difuminado en el borde
            brillo = int(255 - ((distancia - radio) / 10) * 255)
            pixeles[x, y] = brillo

imagen_original.save("1_forma_original.png")
print("[*] Imagen original creada ('1_forma_original.png').")

# ==============================================================
# 2. OPERADOR DE SOBEL (Matemáticas del Gradiente)
# ==============================================================
sobel_x = [
    [-1,  0,  1],
    [-2,  0,  2],
    [-1,  0,  1]
]

sobel_y = [
    [-1, -2, -1],
    [ 0,  0,  0],
    [ 1,  2,  1]
]

imagen_aristas = Image.new("L", (tamaño, tamaño), color=0)
pixeles_aristas = imagen_aristas.load()

# ==============================================================
# 3. SEGMENTACIÓN POR UMBRAL (Thresholding)
# ==============================================================
UMBRAL = 100 
imagen_segmentada = Image.new("L", (tamaño, tamaño), color=0)
pixeles_segmentados = imagen_segmentada.load()

print("[*] Aplicando Operador de Sobel y Segmentación...")

for x in range(1, tamaño - 1):
    for y in range(1, tamaño - 1):
        
        gx = 0
        gy = 0
        
        # Aplicamos ambos Kernels simultáneamente
        for i in range(3):
            for j in range(3):
                color_pixel = pixeles[x + i - 1, y + j - 1]
                gx += color_pixel * sobel_x[i][j]
                gy += color_pixel * sobel_y[i][j]
                
        # Calculamos la magnitud del vector gradiente (Pitágoras)
        magnitud = math.sqrt(gx**2 + gy**2)
        
        # Guardamos la versión cruda de las aristas (suave)
        brillo_arista = int(max(0, min(magnitud, 255)))
        pixeles_aristas[x, y] = brillo_arista
        
        # APLICAMOS LA SEGMENTACIÓN BINARIA
        if magnitud >= UMBRAL:
            pixeles_segmentados[x, y] = 255 # Objeto válido (Blanco)
        else:
            pixeles_segmentados[x, y] = 0   # Fondo / Ruido (Negro)

# ==============================================================
# 4. GUARDAR Y MOSTRAR LOS RESULTADOS AUTOMÁTICAMENTE
# ==============================================================
imagen_aristas.save("2_aristas_sobel.png")
imagen_segmentada.save("3_segmentacion_limpia.png")
print("[*] ¡Proceso terminado! Imágenes guardadas.")

# ¡LA MAGIA OCURRE AQUÍ! 
print("[*] Abriendo visor de imágenes de tu sistema operativo...")
imagen_original.show(title="Imagen Original")
imagen_aristas.show(title="Bordes Detectados (Sobel)")
imagen_segmentada.show(title="Segmentación Limpia")
