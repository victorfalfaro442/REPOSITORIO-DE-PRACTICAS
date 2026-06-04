def particion(arreglo, bajo, alto):
    """
    Función auxiliar que maneja la lógica de intercambio y posicionamiento del pivote.
    
    Explicación del proceso:
    1. Elegimos el último elemento como nuestro 'pivote'.
    2. Usamos un índice 'i' para rastrear la posición de los elementos menores al pivote.
    3. Recorremos el subarreglo; si encontramos un elemento menor o igual al pivote, 
       lo intercambiamos para pasarlo al lado izquierdo.
    4. Al final, colocamos el pivote en su posición final correcta.
    """
    
    # Elegimos el elemento en la posición 'alto' como nuestro pivote.
    pivote = arreglo[alto]
    
    # 'i' será el índice del último elemento menor al pivote encontrado.
    # Inicialmente, lo colocamos justo antes del inicio de nuestro segmento.
    i = bajo - 1
    
    # Recorremos los elementos desde 'bajo' hasta 'alto - 1'
    for j in range(bajo, alto):
        
        # Si el elemento actual es menor o igual al pivote...
        if arreglo[j] <= pivote:
            
            # ...avanzamos el índice de los elementos menores.
            i += 1
            
            # Intercambiamos el elemento actual para mandarlo a la sección de "menores" (izquierda).
            arreglo[i], arreglo[j] = arreglo[j], arreglo[i]
            
    # Una vez que terminamos de revisar, sabemos que la posición 'i + 1' es el 
    # lugar exacto donde debe ir el pivote para separar a los menores de los mayores.
    # Así que lo intercambiamos.
    arreglo[i + 1], arreglo[alto] = arreglo[alto], arreglo[i + 1]
    
    # Retornamos la posición final (índice) donde quedó el pivote.
    return i + 1


def _quicksort_recursivo(arreglo, bajo, alto):
    """
    Función auxiliar recursiva que aplica el algoritmo QuickSort.
    El guion bajo al inicio del nombre indica que es de uso interno.
    """
    
    # Condición base de la recursividad: el subarreglo debe tener al menos 2 elementos.
    # Si 'bajo' es mayor o igual a 'alto', el subarreglo ya está ordenado.
    if bajo < alto:
        
        # Obtenemos el índice del pivote ya posicionado en su lugar correcto.
        indice_pivote = particion(arreglo, bajo, alto)
        
        # Llamamos recursivamente a QuickSort para la mitad izquierda (menores al pivote).
        _quicksort_recursivo(arreglo, bajo, indice_pivote - 1)
        
        # Llamamos recursivamente a QuickSort para la mitad derecha (mayores al pivote).
        _quicksort_recursivo(arreglo, indice_pivote + 1, alto)


def ordenamiento_quicksort(arreglo):
    """
    Función principal envolvente para ordenar una lista utilizando QuickSort.
    Mantiene la misma interfaz simple (un solo argumento) que los métodos anteriores.
    """
    
    # Obtenemos la longitud del arreglo.
    n = len(arreglo)
    
    # Si la lista tiene 1 o 0 elementos, ya está ordenada por definición.
    if n <= 1:
        return arreglo
        
    # Iniciamos la llamada recursiva pasándole el índice inicial y el final.
    _quicksort_recursivo(arreglo, 0, n - 1)
    
    # Retornamos el arreglo ya ordenado in-place.
    return arreglo


# ==========================================
# Ejemplo de uso y prueba del algoritmo
# ==========================================

if __name__ == "__main__":
    # Definimos una lista desordenada
    lista_desordenada = [10, 7, 8, 9, 1, 5]
    
    # Imprimimos la lista original
    print("Lista original:", lista_desordenada)
    
    # Llamamos a nuestra función principal de QuickSort
    lista_ordenada = ordenamiento_quicksort(lista_desordenada)
    
    # Imprimimos la lista después de ordenar
    print("Lista ordenada:", lista_ordenada)
