def busqueda_binaria(arreglo, valor, inicio, fin):
    """
    Función auxiliar que encuentra la posición correcta donde debe insertarse un valor 
    dentro de una sublista ya ordenada, utilizando el enfoque de divide y vencerás.
    """
    # Mientras el rango de búsqueda sea válido (inicio no sobrepase el fin)
    while inicio <= fin:
        
        # Calculamos el índice medio del rango actual. 
        # Usamos división entera '//' para evitar números decimales.
        medio = (inicio + fin) // 2
        
        # Si el valor que queremos insertar es igual al elemento en el medio...
        if arreglo[medio] == valor:
            # ...retornamos la posición siguiente para mantener la estabilidad del algoritmo
            # (insertar el nuevo elemento a la derecha de los ya existentes con el mismo valor).
            return medio + 1
            
        # Si el valor a insertar es mayor que el elemento del medio, 
        # significa que su posición correcta está en la mitad derecha.
        elif arreglo[medio] < valor:
            inicio = medio + 1
            
        # Si el valor es menor, su posición correcta está en la mitad izquierda.
        else:
            fin = medio - 1
            
    # Si no se encontró un valor exacto, 'inicio' nos dará el índice exacto 
    # donde el 'valor' debería insertarse para mantener el orden.
    return inicio


def ordenamiento_insercion_binaria(arreglo):
    """
    Ordena una lista utilizando el algoritmo de Inserción Binaria.
    
    Explicación del proceso:
    1. Asume que el primer elemento está ordenado.
    2. Toma el siguiente elemento y usa búsqueda binaria para encontrar su lugar exacto 
       en la porción izquierda (ya ordenada) del arreglo.
    3. Desplaza los elementos necesarios hacia la derecha de un solo golpe (o en bucle) 
       y coloca el elemento en su posición.
    """
    
    # Obtenemos la longitud total del arreglo.
    n = len(arreglo)
    
    # Iteramos desde el segundo elemento (índice 1) hasta el final.
    for i in range(1, n):
        
        # 'clave' es el valor actual que queremos acomodar.
        clave = arreglo[i]
        
        # Llamamos a nuestra función de búsqueda binaria para encontrar la posición de destino.
        # Buscamos solo en la parte de la lista que ya está ordenada: desde el índice 0 hasta i - 1.
        posicion_destino = busqueda_binaria(arreglo, clave, 0, i - 1)
        
        # Ahora debemos hacer espacio para insertar la 'clave'.
        # Empezamos desde el elemento inmediatamente anterior a la 'clave' (i - 1).
        j = i - 1
        
        # Mientras no lleguemos a la 'posicion_destino', desplazamos los elementos a la derecha.
        while j >= posicion_destino:
            arreglo[j + 1] = arreglo[j]
            j -= 1
            
        # Una vez hecho el espacio, insertamos nuestra 'clave' en la posición calculada.
        arreglo[posicion_destino] = clave

    # Retornamos el arreglo ya ordenado.
    return arreglo


# ==========================================
# Ejemplo de uso y prueba del algoritmo
# ==========================================

if __name__ == "__main__":
    # Definimos una lista desordenada de ejemplo
    lista_desordenada = [37, 23, 0, 17, 12, 72, 31, 46, 100, 88, 54]
    
    # Imprimimos la lista original
    print("Lista original:", lista_desordenada)
    
    # Llamamos a nuestra función de Inserción Binaria
    lista_ordenada = ordenamiento_insercion_binaria(lista_desordenada)
    
    # Imprimimos la lista después de ordenar
    print("Lista ordenada:", lista_ordenada)
