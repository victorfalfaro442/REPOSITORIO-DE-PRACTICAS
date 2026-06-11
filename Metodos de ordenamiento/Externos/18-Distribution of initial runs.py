import heapq
import os

def distribucion_tramos_iniciales(archivo_origen, carpeta_destino, tamano_ram):
    """
    Toma un archivo gigante desordenado y lo divide en múltiples archivos pequeños
    llamados 'tramos' (runs), cada uno internamente ordenado de menor a mayor.
    
    Parámetros:
    - archivo_origen: El archivo de texto con los números desordenados.
    - carpeta_destino: Carpeta donde se guardarán los tramos generados (run_1.txt, run_2.txt, etc).
    - tamano_ram: Cuántos números podemos tener guardados simultáneamente en la memoria RAM.
    """
    # Si la carpeta de destino no existe, la creamos para no tener errores de guardado
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Abrimos el flujo de lectura del archivo desordenado
    with open(archivo_origen, 'r') as f_entrada:
        
        # ---------------------------------------------------------------------
        # FASE 1: LLENADO INICIAL DE LA "RAM"
        # ---------------------------------------------------------------------
        # Simulamos nuestra memoria RAM utilizando dos listas:
        heap_actual = []   # Guardará los números que compiten por entrar al tramo actual
        heap_siguiente = [] # Guardará los números que se retrasan para el próximo tramo
        
        # Leemos las primeras líneas del archivo hasta llenar la capacidad asignada a la RAM
        for _ in range(tamano_ram):
            linea = f_entrada.readline()
            if not linea:
                break # Si el archivo original se acaba antes de llenar la RAM, salimos
            # Convertimos a entero y lo metemos a la lista
            heap_actual.append(int(linea.strip()))
            
        # Transformamos la lista en un "Min-Heap" (Montículo Mínimo).
        # Esta estructura mágica hace que el elemento más pequeño siempre esté en la posición cero [0].
        # Cada vez que saquemos o metamos un número, Python lo reordenará automáticamente en O(log N).
        heapq.heapify(heap_actual)
        
        # ---------------------------------------------------------------------
        # FASE 2: PROCESAMIENTO Y GENERACIÓN DE TRAMOS
        # ---------------------------------------------------------------------
        numero_de_tramo = 1 # Contador para nombrar los archivos (run_1.txt, run_2.txt...)
        ultimo_escrito = None # Almacena el último número que grabamos en el disco
        
        # El ciclo principal continuará mientras tengamos datos en la RAM o sigan quedando en el archivo
        while heap_actual or heap_siguiente:
            
            # Construimos el nombre del archivo para el tramo actual
            nombre_run = os.path.join(carpeta_destino, f"run_{numero_de_tramo}.txt")
            
            # Abrimos el archivo del tramo en modo escritura ('w')
            with open(nombre_run, 'w') as f_tramo:
                
                # Este bucle se encarga de llenar el archivo actual hasta que el heap_actual se vacíe
                while heap_actual:
                    # Extraemos el número más pequeño de la RAM (siempre está en la raíz del Heap)
                    menor_en_ram = heapq.heappop(heap_actual)
                    
                    # Escribimos ese número en el archivo del tramo actual
                    f_tramo.write(f"{menor_en_ram}\n")
                    ultimo_escrito = menor_en_ram # Actualizamos el registro del último elemento escrito
                    
                    # Intentamos leer el SIGUIENTE número del archivo original para ocupar el espacio libre en RAM
                    linea_nueva = f_entrada.readline()
                    
                    if linea_nueva:
                        nuevo_numero = int(linea_nueva.strip())
                        
                        # REGLA DE ORO DE LA SELECCIÓN POR REEMPLAZO:
                        # ¿El nuevo número es mayor o igual que el que acabamos de escribir?
                        if nuevo_numero >= ultimo_escrito:
                            # ¡Perfecto! Puede unirse al tramo actual sin romper el orden ascendente.
                            heapq.heappush(heap_actual, nuevo_numero)
                        else:
                            # ¡Oh no! El número es más pequeño que el que acabamos de escribir.
                            # Si lo metemos ahora, rompería el orden del archivo actual. 
                            # Por lo tanto, lo "retrasamos" enviándolo al almacén del SIGUIENTE tramo.
                            heapq.heappush(heap_siguiente, nuevo_numero)
            
            print(f"-> ¡Tramo exitoso! Creado '{nombre_run}'")
            
            # ---------------------------------------------------------------------
            # FASE 3: CAMBIO DE TRAMO (RESET)
            # ---------------------------------------------------------------------
            # Si el heap_actual se quedó vacío, significa que ya no podemos meter más números en este archivo.
            # Cerramos este tramo, incrementamos el contador para el siguiente archivo...
            numero_de_tramo += 1
            
            # ... y todo lo que habíamos acumulado y retrasado en 'heap_siguiente' 
            # pasa a ser nuestro nuevo 'heap_actual' para reiniciar el proceso.
            heap_actual = heap_siguiente
            heap_siguiente = [] # Vaciamos el almacén de retrasos para la nueva ronda


# =============================================================================
# BLOQUE DE PRUEBA (SIMULACIÓN DE ESCRITORIO)
# =============================================================================
if __name__ == "__main__":
    archivo_caos = "archivo_gigante_desordenado.txt"
    carpeta_salida_tramos = "tramos_iniciales"
    
    # 1. Creamos un archivo con números muy desordenados para la prueba
    elementos_prueba = [25, 6, 21, 14, 35, 4, 12, 33, 2, 18, 10, 40]
    with open(archivo_caos, 'w') as f:
        for num in elementos_prueba:
            f.write(f"{num}\n")
            
    print(f"Archivo de prueba '{archivo_caos}' generado.")
    print(f"Lista original: {elementos_prueba}\n")
    
    # 2. Definimos una simulación de RAM muy pequeña (Capacidad: 3 números a la vez)
    # ¡Mira cómo el algoritmo crea tramos de tamaño mayor a 3 gracias al Min-Heap!
    capacidad_ram_simulada = 3
    
    print("--- Iniciando Distribución de Tramos Iniciales ---")
    distribucion_tramos_iniciales(archivo_caos, carpeta_salida_tramos, capacidad_ram_simulada)
    print("--------------------------------------------------\n")
    
    # 3. Mostramos en pantalla qué se guardó dentro de cada archivo tramo generado
    print("Verificación de los archivos creados en el disco:")
    for archivo in sorted(os.listdir(carpeta_salida_tramos)):
        ruta_completa = os.path.join(carpeta_salida_tramos, archivo)
        with open(ruta_completa, 'r') as f:
            contenido = [int(linea.strip()) for linea in f]
        print(f"  Archivo '{archivo}' contiene el tramo ordenado: {contenido}")
        
    # 4. Limpieza del entorno de pruebas
    if os.path.exists(archivo_caos):
        os.remove(archivo_caos)
    for archivo in os.listdir(carpeta_salida_tramos):
        os.remove(os.path.join(carpeta_salida_tramos, archivo))
    os.rmdir(carpeta_salida_tramos)
