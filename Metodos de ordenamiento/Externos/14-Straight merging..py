import os

def particion(archivo_principal, archivo_aux1, archivo_aux2, longitud):
    """
    FASE 1: PARTICIÓN.
    Lee el archivo principal y distribuye los datos en bloques de tamaño 'longitud'
    alternando entre el archivo auxiliar 1 y el archivo auxiliar 2.
    """
    # Abrimos el archivo de origen en modo lectura y los auxiliares en modo escritura
    with open(archivo_principal, 'r') as f_orig, \
         open(archivo_aux1, 'w') as f_a1, \
         open(archivo_aux2, 'w') as f_a2:
        
        # Variable booleana para alternar el destino (True = Aux1, False = Aux2)
        es_aux1 = True 
        # Leemos la primera línea (primer número) del archivo origen
        linea = f_orig.readline()
        # Contador para saber si el segundo archivo auxiliar llegó a recibir algún dato
        elementos_en_aux2 = 0 
        
        # Mientras sigan quedando registros por leer en el archivo original
        while linea:
            # Escribimos un bloque completo del tamaño indicado por la secuencia actual
            for _ in range(longitud):
                if not linea:
                    break # Si el archivo se queda sin datos antes de completar el bloque, salimos del for
                
                # Escribimos la línea en el archivo auxiliar correspondiente
                if es_aux1:
                    f_a1.write(linea)
                else:
                    f_a2.write(linea)
                    elementos_en_aux2 += 1 # Contabilizamos que aux2 está recibiendo datos
                    
                # Avanzamos a la siguiente línea del archivo de origen
                linea = f_orig.readline()
            
            # Una vez escrito el bloque del tamaño actual, alternamos el destino para el siguiente bloque
            es_aux1 = not es_aux1
            
    # Retornamos True si el archivo aux2 recibió datos. 
    # Si quedó vacío (False), significa que todos los datos cupieron en un solo bloque de aux1 y ya terminamos.
    return elementos_en_aux2 > 0


def fusion(archivo_principal, archivo_aux1, archivo_aux2, longitud):
    """
    FASE 2: FUSIÓN.
    Toma los bloques de tamaño 'longitud' de ambos archivos auxiliares, 
    los compara elemento por elemento y los escribe ordenados en el archivo principal.
    """
    # Abrimos el archivo principal para reescribirlo y los auxiliares para leerlos
    with open(archivo_principal, 'w') as f_orig, \
         open(archivo_aux1, 'r') as f_a1, \
         open(archivo_aux2, 'r') as f_a2:
        
        # Leemos el primer elemento de cada archivo auxiliar
        linea1 = f_a1.readline()
        linea2 = f_a2.readline()
        
        # Mientras quede contenido en cualquiera de los dos archivos auxiliares
        while linea1 or linea2:
            # Contadores para controlar cuántos elementos hemos leído del bloque actual de cada archivo
            c1, c2 = 0, 0
            
            # Mezclamos los dos bloques activos basándonos en la longitud actual de la secuencia
            while c1 < longitud and linea1 and c2 < longitud and linea2:
                # Convertimos las cadenas de texto a enteros para poder compararlas numéricamente
                val1 = int(linea1.strip())
                val2 = int(linea2.strip())
                
                # El menor de los dos se escribe en el archivo principal y avanzamos su puntero
                if val1 <= val2:
                    f_orig.write(linea1)
                    linea1 = f_a1.readline()
                    c1 += 1
                else:
                    f_orig.write(linea2)
                    linea2 = f_a2.readline()
                    c2 += 1
            
            # Si el bloque de aux2 se terminó (o el archivo se vació), vaciamos el resto del bloque de aux1
            while c1 < longitud and linea1:
                f_orig.write(linea1)
                linea1 = f_a1.readline()
                c1 += 1
                
            # Si el bloque de aux1 se terminó (o el archivo se vació), vaciamos el resto del bloque de aux2
            while c2 < longitud and linea2:
                f_orig.write(linea2)
                linea2 = f_a2.readline()
                c2 += 1


def ordenamiento_mezcla_directa(archivo_principal):
    """
    Función de control del algoritmo de Mezcla Directa.
    Incrementa de forma exponencial el tamaño de los bloques hasta completar el ordenamiento.
    """
    # Definimos los nombres de los archivos temporales que se crearán en el disco
    archivo_aux1 = "aux1.txt"
    archivo_aux2 = "aux2.txt"
    
    # La longitud inicial de las secuencias ordenadas de forma nativa es 1
    longitud = 1
    
    # El ciclo se repite de manera indefinida hasta que la condición de parada se cumpla
    while True:
        # Ejecutamos la partición. Si devuelve False, significa que el archivo ya está totalmente ordenado
        hay_mas_bloques = particion(archivo_principal, archivo_aux1, archivo_aux2, longitud)
        
        if not hay_mas_bloques:
            break
            
        # Si aún hay bloques dispersos, los fusionamos de vuelta al archivo original
        fusion(archivo_principal, archivo_aux1, archivo_aux2, longitud)
        
        # Multiplicamos la longitud por 2 para la siguiente pasada (1, 2, 4, 8, 16...)
        longitud *= 2
        
    # Eliminamos los archivos auxiliares del disco para no dejar basura informática
    if os.path.exists(archivo_aux1):
        os.remove(archivo_aux1)
    if os.path.exists(archivo_aux2):
        os.remove(archivo_aux2)


# ==========================================
# Ejemplo de uso y prueba del algoritmo
# ==========================================

if __name__ == "__main__":
    nombre_archivo = "datos_grandes.txt"
    
    # Creamos un archivo de texto simulando datos almacenados en disco
    lista_desordenada = [32, 7, 85, 24, 12, 90, 3, 66, 45, 11]
    with open(nombre_archivo, 'w') as f:
        for numero in lista_desordenada:
            f.write(f"{numero}\n")
            
    print("Archivo original en disco creado con éxito.")
    
    # Aplicamos el ordenamiento externo de Mezcla Directa
    ordenamiento_mezcla_directa(nombre_archivo)
    
    # Leemos el archivo resultante del disco para verificar que se haya ordenado
    lista_ordenada = []
    with open(nombre_archivo, 'r') as f:
        for linea in f:
            lista_ordenada.append(int(linea.strip()))
            
    print("Archivo ordenado en disco:", lista_ordenada)
    
    # Limpiamos el archivo principal de prueba
    if os.path.exists(nombre_archivo):
        os.remove(nombre_archivo)
