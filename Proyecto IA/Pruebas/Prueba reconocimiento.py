from PIL import Image
import matplotlib.pyplot as plt

# 1. Definimos la ruta de una de tus imágenes de muestra (ejemplo: el número 0)
# Si tus imágenes tienen nombres diferentes, cambia '0.1.png' por uno real
ruta_imagen = 'imagenes/sentdex.png'

try:
    # 2. Abrimos la imagen con Pillow
    img = Image.open(ruta_imagen)
    
    # 3. Le pedimos a Python que nos muestre las dimensiones de la imagen
    print(f"¡Imagen cargada con éxito!")
    print(f"Tamaño de la imagen: {img.size} píxeles (Ancho x Alto)")
    
    # 4. Mostramos la imagen en una gráfica para ver sus coordenadas
    plt.imshow(img)
    plt.title("Nuestra imagen de prueba")
    plt.show()

except FileNotFoundError:
    print(f"ERROR: No se pudo encontrar la imagen en la ruta: '{ruta_imagen}'")
    print("Revisa que el nombre del archivo y las carpetas coincidan exactamente.")
