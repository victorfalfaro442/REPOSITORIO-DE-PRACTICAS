def ordenamiento_por_insercion(arreglo):
    """
    Ordena una lista de elementos utilizando el algoritmo de Inserción (Insertion Sort).
    
    Explicación del proceso:
    1. Se asume que el primer elemento (índice 0) ya está "ordenado".
    2. Se toma el siguiente elemento y se compara con los anteriores.
    3. Si el elemento anterior es mayor, se desplaza hacia la derecha.
    4. Se repite el paso 3 hasta encontrar la posición correcta para el elemento actual.
    """
    
    # Obtenemos la longitud total del arreglo para saber cuántos elementos recorrer.
    n = len(arreglo)
    
    # Iniciamos el bucle en el índice 1, ya que el índice 0 se considera inicialmente ordenado.
    for i in range(1, n):
        
        # 'clave' guarda el valor del elemento actual que queremos posicionar correctamente.
        clave = arreglo[i]
        
        # 'j' será el índice de los elementos que están a la izquierda del elemento actual.
        # Empezamos comparando con el elemento inmediatamente anterior (i - 1).
        j = i - 1
        
        # Este bucle 'while' desplaza los elementos mayores que la 'clave' hacia la derecha.
        # Condiciones para que el bucle se ejecute:
        # 1. j >= 0: Asegura que no nos salgamos del límite izquierdo del arreglo.
        # 2. arreglo[j] > clave: Comprueba si el elemento a la izquierda es mayor que nuestra clave.
        while j >= 0 and arreglo[j] > clave:
            
            # Si el elemento de la izquierda es mayor, lo movemos una posición a la derecha.
            arreglo[j + 1] = arreglo[j]
            
            # Disminuimos 'j' en 1 para comparar con el siguiente elemento hacia la izquierda.
            j -= 1
            
        # Una vez que encontramos un elemento menor que la clave (o llegamos al inicio del arreglo),
        # el bucle 'while' termina. Ahora insertamos nuestra 'clave' en su posición correcta.
        arreglo[j + 1] = clave

    # Retornamos el arreglo ya modificado y ordenado.
    return arreglo


# ==========================================
# Ejemplo de uso y prueba del algoritmo
# ==========================================

if __name__ == "__main__":
    # Definimos una lista desordenada de ejemplo
    lista_desordenada = [12, 11, 13, 5, 6, 106, 89, 8, 5, 4]
    
    # Imprimimos la lista original para ver el estado inicial
    print("Lista original:", lista_desordenada)
    
    # Llamamos a nuestra función y guardamos el resultado
    lista_ordenada = ordenamiento_por_insercion(lista_desordenada)
    
    # Imprimimos la lista después de aplicar el algoritmo
    print("Lista ordenada:", lista_ordenada)
