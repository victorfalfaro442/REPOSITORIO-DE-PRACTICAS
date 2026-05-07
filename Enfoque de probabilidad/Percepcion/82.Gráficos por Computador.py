import math
from PIL import Image

print("--- GRÁFICOS POR COMPUTADOR: RAY TRACING A IMAGEN REAL ---")

# ==============================================================
# 1. HERRAMIENTAS VECTORIALES MATEMÁTICAS
# ==============================================================
def producto_punto(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))

def normalizar(v):
    magnitud = math.sqrt(producto_punto(v, v))
    return [a / magnitud for a in v] if magnitud > 0 else v

def resta_vectores(v1, v2):
    return [a - b for a, b in zip(v1, v2)]

# ==============================================================
# 2. DEFINICIÓN DE LA ESCENA Y LA IMAGEN
# ==============================================================
# ¡Ahora podemos usar alta resolución!
ancho = 800
alto = 600

# Creamos una nueva imagen en blanco (formato RGB) y un objeto para acceder a los píxeles
imagen = Image.new("RGB", (ancho, alto), "black")
pixeles = imagen.load()

# Escena 3D
origen_camara = [0.0, 0.0, 0.0]
centro_esfera = [0.0, 0.0, 5.0]
radio_esfera = 2.0

# Luz direccional y colores
direccion_luz = normalizar([-1.0, -1.0, -1.0])
color_esfera = [255, 50, 50]  # Un rojo vibrante [R, G, B]
color_fondo = [20, 20, 30]    # Un azul muy oscuro para el espacio vacío

# ==============================================================
# 3. EL ALGORITMO DE TRAZADO (RENDERING)
# ==============================================================
print(f"[*] Renderizando imagen de {ancho}x{alto} píxeles...")

for y in range(alto):
    for x in range(ancho):
        # Mapeo de coordenadas de la pantalla (2D) al espacio (3D)
        aspect_ratio = ancho / alto
        nx = (x / ancho) * 2.0 - 1.0
        
        # En las imágenes, Y=0 está arriba, así que invertimos el eje Y para la física 3D
        ny = -((y / alto) * 2.0 - 1.0) / aspect_ratio 
        
        # Disparamos el rayo
        direccion_rayo = normalizar([nx, ny, 1.0])
        
        # Intersección (Ecuación Cuadrática)
        oc = resta_vectores(origen_camara, centro_esfera)
        a = producto_punto(direccion_rayo, direccion_rayo)
        b = 2.0 * producto_punto(oc, direccion_rayo)
        c = producto_punto(oc, oc) - radio_esfera**2
        
        discriminante = b**2 - 4*a*c
        
        if discriminante < 0:
            # Falló: Pintamos el píxel del color del fondo
            pixeles[x, y] = tuple(color_fondo)
        else:
            # ¡Impacto! Calculamos la iluminación
            t = (-b - math.sqrt(discriminante)) / (2.0 * a)
            punto_impacto = [origen_camara[i] + t * direccion_rayo[i] for i in range(3)]
            normal_superficie = normalizar(resta_vectores(punto_impacto, centro_esfera))
            
            # Luz Difusa (Lambertiana) + una pequeña luz ambiental base (0.1) para que no sea negro total
            luz_ambiental = 0.1
            intensidad_luz = max(0.0, producto_punto(normal_superficie, direccion_luz))
            luz_final = min(1.0, intensidad_luz + luz_ambiental)
            
            # Calculamos el color final del píxel multiplicando el color base por la luz
            r = int(color_esfera[0] * luz_final)
            g = int(color_esfera[1] * luz_final)
            b = int(color_esfera[2] * luz_final)
            
            # Pintamos el píxel
            pixeles[x, y] = (r, g, b)

# ==============================================================
# 4. GUARDAR EL RESULTADO
# ==============================================================
nombre_archivo = "esfera_renderizada.png"
imagen.save(nombre_archivo)
print(f"[*] ¡Éxito! Imagen guardada como '{nombre_archivo}'.")

# Si estás en un entorno local, esto abrirá la imagen automáticamente
imagen.show()
