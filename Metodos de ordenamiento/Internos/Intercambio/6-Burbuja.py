def ordenamiento_burbuja(arreglo):
    """
    Ordena una lista utilizando el algoritmo de Burbuja (Bubble Sort).
    
    Explicación del proceso:
    1. Compara pares de elementos adyacentes de izquierda a derecha.
    2. Si el elemento de la izquierda es mayor que el de la derecha, los intercambia.
    3. Al final de la primera pasada, el elemento más grande quedará en la última posición.
    4. El proceso se repite ignorando los últimos elementos que ya fueron ordenados.
    """
    
    # Obtenemos la longitud total del arreglo.
    n = len(arreglo)
    
    # El bucle externo controla el número de pasadas que haremos sobre la lista.
    # En el peor de los casos, necesitaremos 'n' pasadas.
    for i in range(n):
        
        # Bandera de optimización: la usamos para saber si hubo algún intercambio en la pasada actual.
        # Si terminamos una pasada completa sin hacer intercambios, significa que la lista ya está ordenada.
        hubo_intercambio = False
        
        # El bucle interno hace las comparaciones de elementos adyacentes.
        # Restamos 'i' porque los últimos 'i' elementos ya están en su lugar correcto (burbujearon al final).
        # Restamos '1' extra para evitar un error de índice fuera de rango al comparar con j + 1.
        for j in range(0, n - i - 1):
            
            # Comparamos el elemento actual con el siguiente.
            if arreglo[j] > arreglo[j + 1]:
                
                # Si están en el orden incorrecto, los intercambiamos.
                # Python permite hacer esto en una sola línea mediante asignación múltiple.
                arreglo[j], arreglo[j + 1] = arreglo[j + 1], arreglo[j]
                
                # Como hicimos un intercambio, cambiamos nuestra bandera a True.
                hubo_intercambio = True
                
        # Si al finalizar el bucle interno la bandera sigue siendo False, 
        # interrumpimos el bucle externo porque ya no hay nada que ordenar.
        if not hubo_intercambio:
            break

    # Retornamos el arreglo ya ordenado.
    return arreglo


# ==========================================
# Ejemplo de uso y prueba del algoritmo
# ==========================================

if __name__ == "__main__":
    # Definimos una lista desordenada de ejemplo
    lista_desordenada = [64, 34, 25, 12, 22, 11, 90]
    
    # Imprimimos la lista original
    print("Lista original:", lista_desordenada)
    
    # Llamamos a nuestra función de Burbuja
    lista_ordenada = ordenamiento_burbuja(lista_desordenada)
    
    # Imprimimos la lista después de ordenar
    print("Lista ordenada:", lista_ordenada)
