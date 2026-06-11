import os

def leer_tramo(archivo):
    """
    Esta función extrae un 'tramo' (run) ordenado desde un archivo abierto.
    Un tramo es una secuencia de números que ya están ordenados de menor a mayor.
    Ejemplo: Si el archivo tiene [3, 7, 9, 2, 5], el primer tramo es [3, 7, 9].
    """
    tramo = []
    
    # .tell() guarda la posición exacta (en bytes) donde se encuentra el puntero del archivo.
    # Nos sirve por si leemos un número que no pertenece a este tramo y debemos "regresar el cassette".
    posicion_inicial = archivo.tell()
    
    # Leemos la primera línea del archivo
    linea = archivo.readline()
    
    # Si la línea está vacía, significa que llegamos al final del archivo (EOF)
    if not linea:
        return tramo  # Retornamos la lista vacía
        
    # .strip() elimina espacios o saltos de línea (\n). Convertimos el texto a entero.
    actual = int(linea.strip())
    tramo.append(actual) # Añadimos el primer número al tramo actual
    
    # Iniciamos un bucle infinito para seguir leyendo los números que continúen el orden ascendente
    while True:
        # Guardamos la posición actual ANTES de leer la siguiente línea
        posicion_antes = archivo.tell()
        siguiente_linea = archivo.readline()
        
        # Si ya no hay más líneas en el archivo, rompemos el bucle
        if not siguiente_linea:
            break
            
        siguiente = int(siguiente_linea.strip())
        
        # COMPARACIÓN CRÍTICA: ¿El número que sigue mantiene el orden ascendente?
        if siguiente < actual:
            # ¡Atención! El número es menor, lo que significa que el tramo ordenado se rompió.
            # Como ya leímos este número pero pertenece al SIGUIENTE tramo, usamos .seek()
            # para regresar el puntero del archivo a la posición de 'posicion_antes'.
            archivo.seek(posicion_antes)
            break # Salimos del bucle porque este tramo ya terminó
        else:
            # Si el número es mayor o igual, se mantiene el orden. Lo agregamos al tramo.
            tramo.append(siguiente)
            # El número 'siguiente' pasa a ser nuestro nuevo número 'actual' para la próxima comparación
            actual = siguiente
            
    # Devolvemos la lista con todos los números que lograron formar el tramo ordenado
    return tramo


def escribir_tramo(archivo, tramo):
    """
    Función auxiliar muy sencilla. Toma una lista de números (un tramo)
    y los escribe línea por línea en el archivo de texto especificado.
    """
    for numero in tramo:
        archivo.write(f"{numero}\n")


def fusionar_dos_tramos(tramo1, tramo2):
    """
    Mezcla dos listas que YA están ordenadas por separado, y las une
    en una sola lista perfectamente ordenada. Es la lógica clásica de Merge Sort.
    """
    resultado = []
    i = 0  # Índice (puntero) para recorrer el tramo 1
    j = 0  # Índice (puntero) para recorrer el tramo 2
    
    # El ciclo continuará mientras AMBOS tramos tengan elementos por comparar
    while i < len(tramo1) and j < len(tramo2):
        # Comparamos cuál de los dos elementos activos es el menor
        if tramo1[i] <= tramo2[j]:
            resultado.append(tramo1[i]) # Agregamos el menor al resultado
            i += 1  # Avanzamos el puntero del tramo 1
        else:
            resultado.append(tramo2[j]) # Agregamos el menor al resultado
            j += 1  # Avanzamos el puntero del tramo 2
            
    # Al salir del bucle, uno de los dos tramos se quedó sin elementos.
    # Con .extend() simplemente vaciamos los elementos que hayan sobrado del otro tramo.
    resultado.extend(tramo1[i:])
    resultado.extend(tramo2[j:])
    
    # Retornamos la gran lista unificada y ordenada
    return resultado


def ordenamiento_polifasico(archivo_principal):
    """
    Algoritmo Principal del Ordenamiento Polifásico.
    Utiliza 3 archivos auxiliares. El secreto está en distribuir los tramos de forma
    asimétrica (siguiendo proporciones de Fibonacci) para usar un archivo menos que la mezcla balanceada.
    """
    # Definimos los nombres de nuestros 3 archivos de trabajo temporal en el disco duro
    f_a, f_b, f_c = "poly_A.txt", "poly_b.txt", "poly_C.txt"
    
    # -------------------------------------------------------------------------
    # FASE 1: LEER EL ARCHIVO ORIGINAL Y DIVIDIRLO EN TRAMOS NATURALES
    # -------------------------------------------------------------------------
    tramos_totales = []
    
    # Abrimos el archivo principal que nos dio el usuario en modo lectura ('r')
    with open(archivo_principal, 'r') as f:
        while True:
            # Extraemos los tramos uno por uno usando nuestra función protectora de flujo
            t = leer_tramo(f)
            if not t: # Si ya no hay más tramos (lista vacía), dejamos de leer
                break
            tramos_totales.append(t) # Guardamos el tramo en una lista temporal
            
    # Control de excepciones: Si el archivo tenía 1 o 0 tramos, significa que ya estaba ordenado
    if len(tramos_totales) <= 1:
        return 
        
    # DISTRIBUCIÓN ASIMÉTRICA (FIBONACCI):
    # Para 3 archivos, los tramos deben distribuirse de manera desigual.
    # Por ejemplo, si tenemos 5 tramos, pondremos 3 en el Archivo A y 2 en el Archivo B.
    # El Archivo C se quedará completamente vacío listo para recibir las fusiones.
    num_tramos_a = min(len(tramos_totales), 3) 
    
    # Abrimos el Archivo A y el Archivo B en modo escritura ('w') para depositar los tramos
    with open(f_a, 'w') as a, open(f_b, 'w') as b:
        for idx, tramo in enumerate(tramos_totales):
            if idx < num_tramos_a:
                escribir_tramo(a, tramo) # Va para el archivo A
            else:
                escribir_tramo(b, tramo) # Va para el archivo B
                
    # -------------------------------------------------------------------------
    # FASE 2: BUCLE DE MEZCLA POLIFÁSICA (PROCESAMIENTO)
    # -------------------------------------------------------------------------
    while True:
        # En cada iteración abrimos los dos archivos de entrada (Lectura: 'r')
        # y el archivo que está libre actúa como salida (Escritura: 'w')
        with open(f_a, 'r') as a, open(f_b, 'r') as b, open(f_c, 'w') as c:
            tramos_mezclados = 0 # Contador para saber cuántas fusiones logramos en esta pasada
            
            while True:
                # Leemos un tramo del Archivo A y un tramo del Archivo B
                t1 = leer_tramo(a)
                t2 = leer_tramo(b)
                
                # CASO A: Si ambos archivos aportaron un tramo, los fusionamos ordenadamente en C
                if t1 and t2:
                    tramo_fusionado = fusionar_dos_tramos(t1, t2)
                    escribir_tramo(c, tramo_fusionado)
                    tramos_mezclados += 1
                # CASO B: Si B se vació pero A aún tenía un tramo, este pasa directo a C
                elif t1:
                    escribir_tramo(c, t1)
                    tramos_mezclados += 1
                # CASO C: Si A se vació pero B aún tenía un tramo, este pasa directo a C
                elif t2:
                    escribir_tramo(c, t2)
                    tramos_mezclados += 1
                # CASO D: Si ambos archivos se quedaron sin tramos, terminamos esta pasada de fusión
                else:
                    break 
                    
        # CONDICIÓN DE PARADA DE TODO EL ALGORITMO:
        # Si logramos unificar todo en un solo tramo gigante (`tramos_mezclados == 1`)
        # y además los archivos de entrada quedaron completamente vacíos (tamaño en bytes == 0),
        # significa que el archivo C contiene el resultado final perfectamente ordenado.
        if tramos_mezclados == 1 and not os.path.getsize(f_a) and not os.path.getsize(f_b):
            # Abrimos el archivo final C para copiar su contenido al archivo original del usuario
            with open(f_c, 'r') as src, open(archivo_principal, 'w') as dest:
                dest.write(src.read()) # Reemplazamos el archivo desordenado por el ordenado
            break # Rompemos el 'while True' principal. ¡Éxito!
            
        # INTERCAMBIO DE ROLES POLIFÁSICO (ROTACIÓN DE ARCHIVOS):
        # Debido a la distribución asimétrica, uno de los dos archivos de entrada se vació antes.
        # El archivo que se quedó vacío cambia de rol con el archivo C (que era la salida).
        # Para no complicar la sintaxis, simplemente intercambiamos las variables de los nombres:
        if os.path.getsize(f_a) == 0:
            # Si el Archivo A se quedó vacío, en la siguiente pasada el Archivo C será la entrada
            # y el Archivo A se limpiará convirtiéndose en la nueva salida.
            f_a, f_c = f_c, f_a 
        elif os.path.getsize(f_b) == 0:
            # Si el Archivo B se quedó vacío, realiza el mismo intercambio estratégico con C
            f_b, f_c = f_c, f_b

    # -------------------------------------------------------------------------
    # FASE 3: LIMPIEZA DEL SISTEMA
    # -------------------------------------------------------------------------
    # Para mantener el disco duro limpio y no dejar archivos basura, eliminamos
    # los tres archivos de texto auxiliares que creamos durante el ordenamiento.
    for archivo in ["poly_A.txt", "poly_b.txt", "poly_C.txt"]:
        if os.path.exists(archivo):
            os.remove(archivo)


# =============================================================================
# BLOQUE DE EJECUCIÓN (PRUEBA DE ESCRITORIO DE EJEMPLO)
# =============================================================================
if __name__ == "__main__":
    # Definimos el nombre del archivo simulado en el disco
    nombre_archivo = "datos_polifasicos.txt"
    
    # Una lista desordenada común
    lista_desordenada = [45, 2, 89, 14, 67, 34, 12, 90, 5]
    
    # Escribimos los datos en el archivo simulando que es un archivo masivo en disco
    with open(nombre_archivo, 'w') as f:
        for numero in lista_desordenada:
            f.write(f"{numero}\n")
            
    print("-> Archivo original creado en el disco con éxito.")
    
    # Llamamos a nuestro potente algoritmo de ordenamiento externo polifásico
    ordenamiento_polifasico(nombre_archivo)
    
    # Comprobamos los resultados abriendo el archivo modificado
    lista_ordenada = []
    with open(nombre_archivo, 'r') as f:
        for linea in f:
            lista_ordenada.append(int(linea.strip()))
            
    print("-> Archivo ordenado mediante Algoritmo Polifásico:", lista_ordenada)
    
    # Eliminamos el archivo principal de prueba para dejar el entorno limpio
    if os.path.exists(nombre_archivo):
        os.remove(nombre_archivo)
