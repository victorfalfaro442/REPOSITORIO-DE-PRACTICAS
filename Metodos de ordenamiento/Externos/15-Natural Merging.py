import os

def particion_natural(archivo_principal, archivo_aux1, archivo_aux2):
    """
    FASE 1: PARTICIÓN NATURAL.
    Identifica los tramos ordenados de forma nativa en el archivo principal
    y los distribuye alternadamente entre ambos archivos auxiliares.
    """
    with open(archivo_principal, 'r') as f_orig, \
         open(archivo_aux1, 'w') as f_a1, \
         open(archivo_aux2, 'w') as f_a2:
        
        linea = f_orig.readline()
        if not linea:
            return 0 # Archivo vacío, 0 tramos creados
            
        # Empezamos escribiendo en el primer archivo auxiliar
        f_actual = f_a1
        f_actual.write(linea)
        previo = int(linea.strip())
        
        # Contadores para saber cuántos tramos totales distribuimos
        tramos_aux1 = 1
        tramos_aux2 = 0
        
        linea = f_orig.readline()
        while linea:
            actual = int(linea.strip())
            
            # Si el número actual es menor que el anterior, el tramo natural se rompió.
            # Cambiamos de archivo auxiliar para empezar el siguiente tramo.
            if actual < previo:
                if f_actual == f_a1:
                    f_actual = f_a2
                    tramos_aux2 += 1
                else:
                    f_actual = f_a1
                    tramos_aux1 += 1
                    
            f_actual.write(linea)
            previo = actual
            linea = f_orig.readline()
            
    # Retornamos el total de tramos creados en el segundo archivo.
    # Si es 0, significa que todo el archivo original era un único gran tramo ordenado.
    return tramos_aux2


def fusion_natural(archivo_principal, archivo_aux1, archivo_aux2):
    """
    FASE 2: FUSIÓN NATURAL.
    Toma un tramo de cada archivo auxiliar, los mezcla ordenadamente 
    y los escribe de vuelta en el archivo principal. Repite hasta vaciar los auxiliares.
    """
    with open(archivo_principal, 'w') as f_orig, \
         open(archivo_aux1, 'r') as f_a1, \
         open(archivo_aux2, 'r') as f_a2:
        
        # Inicializamos las lecturas de flujo
        linea1 = f_a1.readline()
        linea2 = f_a2.readline()
        
        # Mientras queden datos en cualquiera de los dos archivos temporales
        while linea1 or linea2:
            
            # Si ambos archivos tienen datos, mezclamos sus respectivos tramos naturales
            if linea1 and linea2:
                val1 = int(linea1.strip())
                val2 = int(linea2.strip())
                
                # Bucle para procesar un tramo de cada archivo simultáneamente
                while True:
                    if val1 <= val2:
                        f_orig.write(f"{val1}\n")
                        next_l1 = f_a1.readline()
                        if not next_l1: # Fin de archivo aux1
                            linea1 = None
                            break
                        next_v1 = int(next_l1.strip())
                        if next_v1 < val1: # Fin del tramo natural de aux1
                            linea1 = next_l1
                            break
                        val1 = next_v1
                    else:
                        f_orig.write(f"{val2}\n")
                        next_l2 = f_a2.readline()
                        if not next_l2: # Fin de archivo aux2
                            linea2 = None
                            break
                        next_v2 = int(next_l2.strip())
                        if next_v2 < val2: # Fin del tramo natural de aux2
                            linea2 = next_l2
                            break
                        val2 = next_v2
                        
                # Al salir del bucle interno, uno de los dos tramos terminó.
                # Vaciamos el tramo restante del otro archivo.
                if linea1 and (not linea2 or val1 >= int(linea1.strip())): # Quedó activo el tramo 1
                    while True:
                        f_orig.write(f"{val1}\n")
                        next_l1 = f_a1.readline()
                        if not next_l1:
                            linea1 = None
                            break
                        next_v1 = int(next_l1.strip())
                        if next_v1 < val1:
                            linea1 = next_l1
                            break
                        val1 = next_v1
                        
                elif linea2: # Quedó activo el tramo 2
                    while True:
                        f_orig.write(f"{val2}\n")
                        next_l2 = f_a2.readline()
                        if not next_l2:
                            linea2 = None
                            break
                        next_v2 = int(next_l2.strip())
                        if next_v2 < val2:
                            linea2 = next_l2
                            break
                        val2 = next_v2
                        
            # Si solo el archivo auxiliar 1 tiene datos restantes, los vaciamos directo
            elif linea1:
                f_orig.write(linea1)
                linea1 = f_a1.readline()
                
            # Si solo el archivo auxiliar 2 tiene datos restantes, los vaciamos directo
            elif linea2:
                f_orig.write(linea2)
                linea2 = f_a2.readline()


def ordenamiento_mezcla_natural(archivo_principal):
    """
    Función de control del algoritmo de Mezcla Natural.
    Se repite la partición y fusión hasta que ya no existan tramos que separar.
    """
    archivo_aux1 = "aux1_natural.txt"
    archivo_aux2 = "aux2_natural.txt"
    
    while True:
        # Hacemos la partición. Nos devuelve cuántos tramos se enviaron al segundo archivo.
        tramos_en_aux2 = particion_natural(archivo_principal, archivo_aux1, archivo_aux2)
        
        # Si no se envió ningún tramo al archivo 2, significa que el archivo principal
        # se procesó en un solo tramo continuo. ¡Ya está ordenado!
        if tramos_en_aux2 == 0:
            break
            
        # Si hay tramos distribuidos en ambos archivos, los fusionamos de vuelta
        fusion_natural(archivo_principal, archivo_aux1, archivo_aux2)
        
    # Limpieza de archivos basura en disco
    if os.path.exists(archivo_aux1):
        os.remove(archivo_aux1)
    if os.path.exists(archivo_aux2):
        os.remove(archivo_aux2)


# ==========================================
# Ejemplo de uso y prueba del algoritmo
# ==========================================

if __name__ == "__main__":
    nombre_archivo = "datos_naturales.txt"
    
    # Creamos un archivo con algunas secuencias ya ordenadas nativamente (ej: 5, 10, 15)
    lista_desordenada = [5, 10, 15, 2, 8, 20, 1, 4, 3, 9]
    with open(nombre_archivo, 'w') as f:
        for numero in lista_desordenada:
            f.write(f"{numero}\n")
            
    print("Archivo en disco con tramos naturales creado.")
    
    # Ejecutamos el ordenamiento externo
    ordenamiento_mezcla_natural(nombre_archivo)
    
    # Comprobamos el resultado leyendo desde el disco
    lista_ordenada = []
    with open(nombre_archivo, 'r') as f:
        for linea in f:
            lista_ordenada.append(int(linea.strip()))
            
    print("Archivo ordenado mediante Mezcla Natural:", lista_ordenada)
    
    # Limpieza final del archivo de prueba
    if os.path.exists(nombre_archivo):
        os.remove(nombre_archivo)
