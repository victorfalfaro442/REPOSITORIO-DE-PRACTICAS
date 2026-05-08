import math
from PIL import Image

print("--- GRÁFICOS AVANZADOS: TEXTURAS Y SOMBRAS ---")

# ==============================================================
# 1. HERRAMIENTAS VECTORIALES
# ==============================================================
def producto_punto(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))

def normalizar(v):
    magnitud = math.sqrt(max(producto_punto(v, v), 1e-10))
    return [a / magnitud for a in v]

def resta_vectores(v1, v2):
    return [a - b for a, b in zip(v1, v2)]

def suma_vectores(v1, v2):
    return [a + b for a, b in zip(v1, v2)]

# ==============================================================
# 2. DEFINICIÓN DE LA ESCENA
# ==============================================================
# Resolución (mantenemos un tamaño moderado para que procese rápido)
ancho = 600
alto = 400
imagen = Image.new("RGB", (ancho, alto), "black")
pixeles = imagen.load()

# Cámara y Luz
origen_camara = [0.0, 0.5, 0.0]  # Subimos un poco la cámara
direccion_luz = normalizar([1.0, 1.0, -1.0]) # Luz viene de arriba y derecha

# Esfera
centro_esfera = [0.0, 0.0, 5.0]
radio_esfera = 1.5
color_esfera = [255, 50, 50]

# Suelo (Plano horizontal)
altura_suelo = -1.5

# ==============================================================
# 3. FUNCIONES DE INTERSECCIÓN
# ==============================================================
def intersectar_esfera(origen, direccion):
    oc = resta_vectores(origen, centro_esfera)
    a = producto_punto(direccion, direccion)
    b = 2.0 * producto_punto(oc, direccion)
    c = producto_punto(oc, oc) - radio_esfera**2
    discriminante = b**2 - 4*a*c
    
    if discriminante >= 0:
        t = (-b - math.sqrt(discriminante)) / (2.0 * a)
        if t > 0: return t
    return float('inf')

def intersectar_suelo(origen, direccion):
    if abs(direccion[1]) > 1e-6: # Evitar división por cero
        t = (altura_suelo - origen[1]) / direccion[1]
        if t > 0: return t
    return float('inf')

# ==============================================================
# 4. MOTOR DE RENDERIZADO
# ==============================================================
print(f"[*] Renderizando escena (Resolución: {ancho}x{alto})...")

for y in range(alto):
    for x in range(ancho):
        nx = (x / ancho) * 2.0 - 1.0
        ny = -((y / alto) * 2.0 - 1.0) / (ancho / alto)
        direccion_rayo = normalizar([nx, ny, 1.0])
        
        # 4.1 Buscamos qué objeto choca primero (Esfera o Suelo)
        t_esfera = intersectar_esfera(origen_camara, direccion_rayo)
        t_suelo = intersectar_suelo(origen_camara, direccion_rayo)
        t_min = min(t_esfera, t_suelo)
        
        if t_min == float('inf'):
            # No chocó con nada -> Fondo azul oscuro
            pixeles[x, y] = (15, 20, 30)
            continue
            
        # 4.2 Calculamos el punto de impacto exacto en 3D
        punto_impacto = suma_vectores(origen_camara, [d * t_min for d in direccion_rayo])
        
        # 4.3 Propiedades del material y la normal según el objeto impactado
        if t_min == t_esfera:
            normal = normalizar(resta_vectores(punto_impacto, centro_esfera))
            color_base = color_esfera
        else:
            normal = [0.0, 1.0, 0.0] # El suelo siempre apunta hacia arriba
            # Textura Procedural: Tablero de ajedrez
            # Sumamos las coordenadas X y Z, las redondeamos y sacamos el módulo 2
            cuadro = (math.floor(punto_impacto[0]) + math.floor(punto_impacto[2])) % 2
            color_base = [220, 220, 220] if cuadro == 0 else [80, 80, 80] # Blanco o Gris Oscuro
            
        # 4.4 CÁLCULO DE SOMBRAS (Rayos Secundarios)
        # Levantamos ligeramente el punto de origen del rayo de sombra para evitar colisionar con la propia superficie
        origen_sombra = suma_vectores(punto_impacto, [n * 0.001 for n in normal])
        
        # Disparamos hacia la luz y vemos si la esfera nos tapa
        sombra_esfera = intersectar_esfera(origen_sombra, direccion_luz)
        en_sombra = sombra_esfera != float('inf')
        
        # 4.5 Cálculo de Iluminación Final
        luz_ambiental = 0.15
        
        if en_sombra:
            luz_final = luz_ambiental # Si hay sombra, solo recibe luz ambiental
        else:
            intensidad = max(0.0, producto_punto(normal, direccion_luz))
            luz_final = min(1.0, intensidad + luz_ambiental)
            
        # Pintamos el píxel
        r = int(color_base[0] * luz_final)
        g = int(color_base[1] * luz_final)
        b = int(color_base[2] * luz_final)
        pixeles[x, y] = (r, g, b)

# ==============================================================
# 5. GUARDAR Y MOSTRAR
# ==============================================================
nombre_archivo = "texturas_y_sombras.png"
imagen.save(nombre_archivo)
print("[*] ¡Magia completada! Abriendo imagen...")
imagen.show(title="Texturas y Sombras Arrojadas")
