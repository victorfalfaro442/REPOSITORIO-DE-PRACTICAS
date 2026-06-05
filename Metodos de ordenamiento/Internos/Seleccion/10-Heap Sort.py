def hacer_monticulo(arreglo, tamaño_monticulo, indice_raiz):
    """
    Función auxiliar que reorganiza un sub-árbol para que cumpla con la propiedad 
    de un Max-Heap (el padre siempre es mayor que sus hijos).
    """
    
    # Asumimos que la raíz es el elemento más grande
    indice_mayor = indice_raiz
    
    # Calculamos los índices de los hijos izquierdo y derecho en la lista
    hijo_izquierdo = 2 * indice_raiz + 1
    hijo_derecho = 2 * indice_raiz + 2
    
    # Si el hijo izquierdo existe y es mayor que la raíz actual, lo marcamos como el mayor
    if hijo_izquierdo < tamaño_monticulo and arreglo[hijo_izquierdo] > arreglo[indice_mayor]:
        indice_mayor = hijo_izquierdo
        
    # Si el hijo derecho existe y es mayor que el elemento más grande registrado hasta ahora
    if hijo_derecho < tamaño_monticulo and arreglo[hijo_derecho] > arreglo[indice_mayor]:
        indice_mayor = hijo_derecho
        
    # Si el mayor ya no es la raíz original, necesitamos intercambiarlos
    if indice_mayor != indice_raiz:
        arreglo[indice_raiz], arreglo[indice_mayor] = arreglo[indice_mayor], arreglo[indice_raiz]
        
        # Como alteramos el árbol hacia abajo, llamamos recursivamente a la función
        # para asegurarnos de que el sub-árbol afectado siga siendo un Max-Heap
        hacer_monticulo(arreglo, tamaño_monticulo, indice_mayor)


def heap_sort(arreglo):
    """
    Ordena una lista utilizando el algoritmo Heap Sort.
    
    Explicación del proceso:
    1. Transforma todo el arreglo en un Max-Heap (estructura donde el mayor está al inicio).
    2. "Selecciona" la raíz (el mayor), la saca del árbol intercambiándola con el último elemento.
    3. Reconstruye el Max-Heap con los elementos restantes.
    4. Repite el proceso hasta que el árbol se vacíe.
    """
    
    n = len(arreglo)
    
    # FASE 1: Construir el Max-Heap inicial.
    # Empezamos desde el último nodo que tiene hijos (n // 2 - 1) hacia atrás hasta la raíz (0).
    for i in range(n // 2 - 1, -1, -1):
        hacer_monticulo(arreglo, n, i)
        
    # FASE 2: Extracción (Selección) de elementos uno por uno.
    # Vamos desde el último elemento de la lista hasta el segundo (índice 1).
    for i in range(n - 1, 0, -1):
        
        # Movemos la raíz actual (el valor más grande del montículo) al final del arreglo.
        arreglo[i], arreglo[0] = arreglo[0], arreglo[i]
        
        # Ahora que quitamos el mayor, el arreglo[0] es un elemento pequeño.
        # Llamamos a nuestra función para que ese elemento se "hunda" y el nuevo
        # mayor suba a la raíz. Pasamos 'i' como tamaño para ignorar los que ya ordenamos al final.
        hacer_monticulo(arreglo, i, 0)

    # Retornamos el arreglo ordenado
    return arreglo


# ==========================================
# Ejemplo de uso
# ==========================================
if __name__ == "__main__":
    lista_3 = [12, 11, 13, 5, 6, 7]
    print("\nHeap Sort Original:", lista_3)
    print("Heap Sort Ordenada:", heap_sort(lista_3))
