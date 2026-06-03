def ordenamiento_por_seleccion(arreglo):
    """
    Ordena una lista de elementos utilizando el algoritmo de Selección Directa (Selection Sort).
    
    Explicación del proceso:
    1. Divide lógicamente la lista en dos partes: una ordenada (izquierda) y otra desordenada (derecha).
    2. Busca el elemento más pequeño en la parte desordenada.
    3. Intercambia ese elemento más pequeño con el primer elemento de la parte desordenada.
    4. La frontera entre la parte ordenada y desordenada avanza una posición hacia la derecha.
    """
    
    # Obtenemos la longitud total del arreglo.
    n = len(arreglo)
    
    # El bucle externo recorre todo el arreglo. 
    # Solo necesitamos llegar hasta n - 1, porque cuando quede un solo elemento, 
    # ya estará en su lugar correcto por descarte.
    for i in range(n - 1):
        
        # Suponemos inicialmente que el primer elemento de la parte desordenada es el menor.
        # Guardamos su índice en 'indice_minimo'.
        indice_minimo = i
        
        # El bucle interno recorre el resto de los elementos a la derecha de 'i'
        # para verificar si nuestra suposición es correcta o si hay un elemento aún menor.
        for j in range(i + 1, n):
            
            # Si encontramos un elemento que es menor que nuestro 'minimo' actual...
            if arreglo[j] < arreglo[indice_minimo]:
                
                # ...actualizamos 'indice_minimo' con la nueva posición del elemento menor.
                indice_minimo = j
                
        # Una vez que el bucle interno termina, hemos encontrado el verdadero mínimo de la parte desordenada.
        # Si el elemento mínimo encontrado no es el mismo con el que empezamos (es decir, no está ya en la posición 'i')...
        if indice_minimo != i:
            
            # ...los intercambiamos. En Python, esto se puede hacer en una sola línea de manera nativa
            # usando asignación múltiple, sin necesidad de usar una variable temporal auxiliar.
            arreglo[i], arreglo[indice_minimo] = arreglo[indice_minimo], arreglo[i]

    # Retornamos el arreglo ya modificado y ordenado.
    return arreglo


# ==========================================
# Ejemplo de uso y prueba del algoritmo
# ==========================================

if __name__ == "__main__":
    # Definimos una nueva lista desordenada de ejemplo
    lista_desordenada = [64, 25, 12, 22, 11]
    
    # Imprimimos la lista original
    print("Lista original:", lista_desordenada)
    
    # Llamamos a nuestra función de Selección Directa
    lista_ordenada = ordenamiento_por_seleccion(lista_desordenada)
    
    # Imprimimos la lista después de ordenar
    print("Lista ordenada:", lista_ordenada)
