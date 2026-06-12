import numpy as np                  # Para hacer cálculos matemáticos rápidos con matrices (arrays)
import matplotlib.pyplot as plt     # Para dibujar las gráficas y mostrar las imágenes
from PIL import Image               # Pillow: Para abrir y manipular los archivos de imagen (.png, .jpg)
from collections import Counter     # Para contar los "votos" (cuántas veces se repite un número en una lista)
import os                           # Para interactuar con el sistema operativo (ej. verificar si un archivo existe)

# =============================================================================
# 1. FUNCIÓN DE UMBRALIZACIÓN (Thresholding)
# =============================================================================
def threshold(imageArray):
    """
    Esta función toma la matriz de colores de una imagen y la simplifica al máximo:
    Convierte todo lo que sea claro en blanco puro, y lo oscuro en negro puro.
    Esto elimina sombras, difuminados y colores que puedan confundir a la computadora.
    """
    balanceAr = []
    # Hacemos una copia de la imagen original para no modificar la fuente directamente
    newAr = imageArray.copy()

    # --- FASE 1: Descubrir el punto medio (promedio de brillo) de toda la imagen ---
    for eachRow in imageArray:           # Recorremos cada fila de píxeles
        for eachPix in eachRow:          # Recorremos cada píxel dentro de esa fila
            # eachPix[:3] toma solo los valores Rojo, Verde y Azul (ignora la transparencia)
            avgNum = np.mean(eachPix[:3]) 
            balanceAr.append(avgNum)     # Guardamos el promedio de brillo de este píxel en la lista

    # Calculamos el promedio global de todos los píxeles. Este será nuestro "umbral".
    balance = np.mean(balanceAr)

    # --- FASE 2: Pintar la imagen de blanco y negro puro ---
    for eachRow in newAr:
        for eachPix in eachRow:
            # Si el píxel actual es MÁS CLARO que el promedio global de la imagen:
            if np.mean(eachPix[:3]) > balance:
                eachPix[0] = 255  # Rojo al máximo
                eachPix[1] = 255  # Verde al máximo
                eachPix[2] = 255  # Azul al máximo
                eachPix[3] = 255  # Canal Alpha (Opacidad) al máximo. Resultado = BLANCO PURO.
            
            # Si el píxel actual es MÁS OSCURO que el promedio (es parte del número dibujado):
            else:
                eachPix[0] = 0    # Sin Rojo
                eachPix[1] = 0    # Sin Verde
                eachPix[2] = 0    # Sin Azul
                eachPix[3] = 255  # Opacidad al máximo. Resultado = NEGRO PURO.

    # Devolvemos la nueva matriz de la imagen, ahora totalmente en blanco y negro
    return newAr

# =============================================================================
# 2. CREACIÓN DE LA BASE DE DATOS (.txt) - "El Cerebro"
# =============================================================================
def createExamples():
    """
    Esta función lee todas las imágenes de entrenamiento, las convierte a matrices de 
    blanco y negro, las transforma en texto, y las guarda en 'numArEx.txt'.
    """
    # Abrimos (o creamos) un archivo de texto en modo escritura ('w' = write)
    archivo_datos = open('numArEx.txt', 'w')
    
    # Definimos qué números tenemos (0 al 9) y cuántas versiones de cada uno (1 al 9)
    numbersWeHave = range(0, 10)
    versionsWeHave = range(1, 10)

    print("Generando archivo de conocimiento (numArEx.txt)...")
    
    # Anidamos bucles para construir los nombres de los archivos: 0.1.png, 0.2.png, etc.
    for eachNum in numbersWeHave:
        for eachVer in versionsWeHave:
            # Construimos la ruta exacta donde Python debe buscar la imagen
            imgFilePath = 'imagenes/numbers/' + str(eachNum) + '.' + str(eachVer) + '.png'
            
            # Si el archivo realmente existe en la carpeta, procedemos:
            if os.path.exists(imgFilePath):
                # 1. Abrimos la imagen y FORZAMOS que tenga 4 canales (RGBA) para evitar errores
                ei = Image.open(imgFilePath).convert('RGBA')
                # 2. Convertimos la imagen en una matriz matemática de Numpy
                eiar = np.array(ei)
                # 3. La pasamos por nuestra función para dejarla en blanco y negro puro
                eiar = threshold(eiar)
                
                # 4. TRUCO CLAVE: Convertimos esa enorme matriz matemática en una simple cadena de texto
                eiar1 = str(eiar.tolist())
                
                # 5. Formateamos la línea. Ejemplo: "3::[[255,255...],[0,0...]]"
                lineToWrite = str(eachNum) + '::' + eiar1 + '\n'
                
                # 6. Escribimos esta línea en nuestro archivo de texto
                archivo_datos.write(lineToWrite)
                
    archivo_datos.close() # Siempre debemos cerrar el archivo al terminar de escribir
    print("¡Archivo generado con éxito!\n")

# =============================================================================
# 3. RECONOCIMIENTO Y VISUALIZACIÓN
# =============================================================================
def whatNumIsThis(filePath):
    """
    Toma una imagen nueva, la convierte a texto, y la compara "píxel por píxel"
    (texto contra texto) contra la base de datos para adivinar qué número es.
    """
    print(f"Analizando la imagen: {filePath}...")
    
    # Aquí guardaremos un "voto" cada vez que un píxel coincida con uno de la base de datos
    matchedAr = []
    
    # Verificamos que el archivo de base de datos exista antes de intentar leerlo
    if not os.path.exists('numArEx.txt'):
        print("Error: No existe 'numArEx.txt'. Primero debes generar la base de datos.")
        return

    # Abrimos la base de datos en modo lectura ('r' = read) y leemos todo su contenido
    with open('numArEx.txt', 'r') as loadExamps_file:
        loadExamps = loadExamps_file.read()
    
    # Separamos el contenido por saltos de línea para tener cada ejemplo como un elemento de una lista
    loadExamps = loadExamps.split('\n')

    # Preparamos la imagen de prueba que queremos reconocer (mismo proceso que en el entrenamiento)
    i = Image.open(filePath).convert('RGBA')
    iar = np.array(i)
    iar = threshold(iar) 
    iarl = iar.tolist()

    # Convertimos la imagen de prueba a texto
    inQuestion = str(iarl)

    # --- LÓGICA DE COMPARACIÓN ---
    # Revisamos cada línea de nuestra base de datos
    for eachExample in loadExamps:
        if len(eachExample) > 3: # Ignoramos líneas vacías o corruptas
            # Separamos el número real de su matriz usando nuestro separador '::'
            splitEx = eachExample.split('::')
            currentNum = splitEx[0] # El número que es (ej. '5')
            currentAr = splitEx[1]  # La matriz en texto de ese número

            # Dividimos las matrices de texto usando '],' para aislar cada píxel individual
            eachPixEx = currentAr.split('],')
            eachPixInQ = inQuestion.split('],')

            x = 0
            # Comparamos píxel por píxel
            while x < len(eachPixEx):
                # Si el texto del píxel de muestra es idéntico al píxel de la imagen nueva:
                if eachPixEx[x] == eachPixInQ[x]:
                    # ¡Añadimos un voto para este número!
                    matchedAr.append(int(currentNum))
                x += 1 # Avanzamos al siguiente píxel

    # Counter cuenta los votos. Ej: {5: 350, 3: 120} (El 5 tuvo 350 píxeles iguales)
    x_counter = Counter(matchedAr)
    print("Predicción de coincidencias (Número : Votos de píxeles):")
    print(x_counter)

    # --- VISUALIZACIÓN DE LOS RESULTADOS CON MATPLOTLIB ---
    graphX = [] # Aquí irán los números (0 al 9)
    graphY = [] # Aquí irán los votos de cada número

    for eachThing in x_counter:
        graphX.append(eachThing)
        graphY.append(x_counter[eachThing])

    # Creamos la ventana principal de la gráfica
    fig = plt.figure()
    
    # Dividimos la ventana en una cuadrícula. 
    # ax1 será la parte de arriba (para la imagen) y ax2 la de abajo (para la gráfica de barras)
    ax1 = plt.subplot2grid((4,4), (0,0), rowspan=1, colspan=4)
    ax2 = plt.subplot2grid((4,4), (1,0), rowspan=3, colspan=4)

    # Mostramos la imagen procesada arriba
    ax1.imshow(iar)
    # Dibujamos las barras de predicción abajo
    ax2.bar(graphX, graphY, align='center')
    
    # Configuramos el diseño de la gráfica de barras
    plt.ylim(400) # Límite de altura para la gráfica (útil si todas las barras se ven muy planas)
    xloc = plt.MaxNLocator(12)
    ax2.xaxis.set_major_locator(xloc)
    
    plt.title("Resultados del Reconocimiento de Patrones")
    plt.show() # Muestra la ventana. El programa se pausará aquí hasta que cierres la gráfica.

# =============================================================================
# EJECUCIÓN PRINCIPAL DEL PROGRAMA
# =============================================================================
# Esto asegura que el código principal solo se ejecute si corremos este archivo directamente
if __name__ == '__main__':
    
    # 1. ENTRENAMIENTO
    # Llama a esta función para leer las imágenes y crear/actualizar 'numArEx.txt'.
    # Si ya tienes el archivo generado y no has agregado imágenes nuevas, puedes comentarla (ponerle un # al inicio).
    createExamples()
    
    # 2. PRUEBA Y RECONOCIMIENTO
    # Ruta de la imagen que queremos que la computadora intente adivinar
    ruta_prueba = 'imagenes/numbers/5.5.png'
    
    # Verificamos que no te hayas equivocado al escribir la ruta antes de intentar predecir
    if os.path.exists(ruta_prueba):
        whatNumIsThis(ruta_prueba) # ¡Magia en acción!
    else:
        print(f"Error: No se encontró la imagen de prueba en '{ruta_prueba}'.")
