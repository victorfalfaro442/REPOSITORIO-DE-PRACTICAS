import os

def distribucion_inicial(archivo_principal, f_a1, f_a2):
    """
    Toma el archivo original y distribuye los elementos uno por uno (bloques de tamaño 1)
    alternando entre los primeros dos archivos auxiliares (A1 y A2).
    """
    with open(archivo_principal, 'r') as f_orig, \
         open(f_a1, 'w') as a1, \
         open(f_a2, 'w') as a2:
        
        es_a1 = True
        linea = f_orig.readline()
        
        while linea:
            if es_a1:
                a1.write(linea)
            else:
                a2.write(linea)
            es_a1 = not es_a1
            linea = f_orig.readline()


def mezclar_pasada(f_in1, f_in2, f_out1, f_out2, longitud):
    """
    Lee bloques de tamaño 'longitud' de f_in1 y f_in2, los fusiona en un bloque ordenado
    de tamaño (2 * longitud) y los escribe alternadamente en f_out1 y f_out2.
    
    Retorna la cantidad de elementos escritos en f_out2 para saber si la mezcla terminó.
    """
    with open(f_in1, 'r') as in1, open(f_in2, 'r') as in2, \
         open(f_out1, 'w') as out1, open(f_out2, 'w') as out2:
        
        linea1 = in1.readline()
        linea2 = in2.readline()
        
        es_out1 = True
        elementos_en_out2 = 0
        
        # Mientras queden registros en cualquiera de los archivos de entrada
        while linea1 or linea2:
            # Seleccionamos el archivo de salida actual (redirección balanceada)
            f_destino = out1 if es_out1 else out2
            
            c1, c2 = 0, 0
            # Fusionamos un bloque de tamaño 'longitud' de cada archivo
            while c1 < longitud and linea1 and c2 < longitud and linea2:
                v1 = int(linea1.strip())
                v2 = int(linea2.strip())
                
                if v1 <= v2:
                    f_destino.write(linea1)
                    linea1 = in1.readline()
                    c1 += 1
                else:
                    f_destino.write(linea2)
                    linea2 = in2.readline()
                    c2 += 1
                if not es_out1:
                    elementos_en_out2 += 1
                    
            # Vaciamos los elementos restantes del bloque de in1 (si quedan)
            while c1 < longitud and linea1:
                f_destino.write(linea1)
                linea1 = in1.readline()
                c1 += 1
                if not es_out1:
                    elementos_en_out2 += 1
                    
            # Vaciamos los elementos restantes del bloque de in2 (si quedan)
            while c2 < longitud and linea2:
                f_destino.write(linea2)
                linea2 = in2.readline()
                c2 += 1
                if not es_out1:
                    elementos_en_out2 += 1
            
            # Cambiamos de archivo de salida para el siguiente bloque fusionado
            es_out1 = not es_out1
            
    return elementos_en_out2


def copiar_archivo(origen, destino):
    """Función auxiliar para volcar el resultado final al archivo principal."""
    with open(origen, 'r') as f_orig, open(destino, 'w') as f_dest:
        f_dest.write(f_orig.read())


def ordenamiento_mezcla_balanceada(archivo_principal):
    """
    Función de control de la Mezcla Balanceada.
    Administra los dos conjuntos de archivos (A y B) alternando sus roles de entrada/salida.
    """
    # Definimos los dos pares de archivos auxiliares en el disco
    f_a1, f_a2 = "aux_A1.txt", "aux_A2.txt"
    f_b1, f_b2 = "aux_B1.txt", "aux_B2.txt"
    
    # Paso 1: Distribución inicial en el conjunto A
    distribucion_inicial(archivo_principal, f_a1, f_a2)
    
    longitud = 1
    en_conjunto_A = True # Bandera para saber qué conjunto es la entrada actual
    
    while True:
        if en_conjunto_A:
            # Leemos de A y escribimos ordenadamente en B
            elementos_aux2 = mezclar_pasada(f_a1, f_a2, f_b1, f_b2, longitud)
            # Si el segundo archivo del destino quedó vacío, ¡ya terminamos! Todo está unificado en B1.
            if elementos_aux2 == 0:
                copiar_archivo(f_b1, archivo_principal)
                break
        else:
            # Leemos de B y escribimos ordenadamente en A
            elementos_aux2 = mezclar_pasada(f_b1, f_b2, f_a1, f_a2, longitud)
            # Si el segundo archivo del destino quedó vacío, ¡ya terminamos! Todo está unificado en A1.
            if elementos_aux2 == 0:
                copiar_archivo(f_a1, archivo_principal)
                break
                
        # Duplicamos el tamaño del bloque para la siguiente pasada y alternamos los conjuntos
        longitud *= 2
        en_conjunto_A = not en_conjunto_A
        
    # Limpieza absoluta de archivos temporales en el disco duro
    for archivo in [f_a1, f_a2, f_b1, f_b2]:
        if os.path.exists(archivo):
            os.remove(archivo)


# ==========================================
# Ejemplo de uso y prueba del algoritmo
# ==========================================

if __name__ == "__main__":
    nombre_archivo = "datos_balanceados.txt"
    
    lista_desordenada = [71, 14, 36, 9, 85, 23, 4, 60, 52, 11]
    with open(nombre_archivo, 'w') as f:
        for numero in lista_desordenada:
            f.write(f"{numero}\n")
            
    print("Archivo en disco listo para Mezcla Balanceada.")
    
    # Ejecutamos el ordenamiento externo multidireccional
    ordenamiento_mezcla_balanceada(nombre_archivo)
    
    # Comprobamos los resultados leyendo el archivo final
    lista_ordenada = []
    with open(nombre_archivo, 'r') as f:
        for linea in f:
            lista_ordenada.append(int(linea.strip()))
            
    print("Archivo ordenado mediante Mezcla Balanceada:", lista_ordenada)
    
    if os.path.exists(nombre_archivo):
        os.remove(nombre_archivo)
