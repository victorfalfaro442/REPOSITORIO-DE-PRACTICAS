def ordenamiento_shell(arreglo):
    """
    Ordena una lista de elementos utilizando el algoritmo Shell Sort.
    
    Explicación del proceso:
    1. Se define una "brecha" (gap) inicial, generalmente la mitad de la longitud del arreglo.
    2. Se agrupan y ordenan los elementos que están separados por esa brecha usando inserción.
    3. Se reduce la brecha a la mitad y se repite el proceso.
    4. El algoritmo termina cuando la brecha es 1 y se hace una última pasada de Inserción Directa.
    """
    
    # Obtenemos la longitud total del arreglo.
    n = len(arreglo)
    
    # Inicializamos el tamaño de la brecha. 
    # Usaremos la secuencia original propuesta por Donald Shell: n // 2.
    # El operador '//' hace una división entera.
    brecha = n // 2
    
    # El bucle principal se ejecuta mientras la brecha sea mayor que 0.
    while brecha > 0:
        
        # Iteramos desde el índice igual a la 'brecha' hasta el final del arreglo.
        # Esto equivale a hacer un Ordenamiento por Inserción, pero en lugar de comparar 
        # con el elemento inmediatamente anterior (salto de 1), comparamos con saltos de 'brecha'.
        for i in range(brecha, n):
            
            # Guardamos el elemento actual en una variable temporal. 
            # Este es el elemento que vamos a intentar insertar en su posición correcta.
            temp = arreglo[i]
            
            # 'j' nos ayudará a recorrer hacia atrás los elementos de este "subgrupo" separado por la brecha.
            j = i
            
            # Este bucle desplaza los elementos mayores hacia la derecha.
            # Condiciones:
            # 1. j >= brecha: Evita que busquemos índices negativos fuera del arreglo.
            # 2. arreglo[j - brecha] > temp: Comprueba si el elemento anterior del subgrupo es mayor que 'temp'.
            while j >= brecha and arreglo[j - brecha] > temp:
                
                # Movemos el elemento mayor hacia la derecha dentro de su subgrupo.
                arreglo[j] = arreglo[j - brecha]
                
                # Retrocedemos 'j' la distancia de la brecha para seguir comparando.
                j -= brecha
                
            # Una vez que encontramos su lugar, insertamos 'temp' en la posición correcta.
            arreglo[j] = temp
            
        # Reducimos la brecha a la mitad para la siguiente iteración del bucle 'while'.
        brecha //= 2

    # Retornamos el arreglo ya ordenado.
    return arreglo


# ==========================================
# Ejemplo de uso y prueba del algoritmo
# ==========================================

if __name__ == "__main__":
    # Definimos una lista desordenada, idealmente un poco más larga para notar el efecto de los saltos
    lista_desordenada = [45, 12, 85, 32, 89, 39, 69, 44, 42, 1, 14]
    
    # Imprimimos la lista original
    print("Lista original:", lista_desordenada)
    
    # Llamamos a nuestra función Shell Sort
    lista_ordenada = ordenamiento_shell(lista_desordenada)
    
    # Imprimimos la lista después de aplicar el algoritmo
    print("Lista ordenada:", lista_ordenada)
