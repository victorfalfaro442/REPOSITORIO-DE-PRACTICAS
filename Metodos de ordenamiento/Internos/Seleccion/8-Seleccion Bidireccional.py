def seleccion_bidireccional(arreglo):
    """
    Ordena una lista utilizando el algoritmo de Selección Bidireccional.
    
    Explicación del proceso:
    1. Recorre la lista buscando el valor mínimo y máximo al mismo tiempo.
    2. Coloca el mínimo en la primera posición disponible por la izquierda.
    3. Coloca el máximo en la última posición disponible por la derecha.
    4. Reduce la ventana de búsqueda por ambos extremos.
    """
    
    # Obtenemos la longitud del arreglo
    n = len(arreglo)
    
    # Solo necesitamos hacer n // 2 pasadas, ya que acomodamos 2 elementos por pasada
    for i in range(n // 2):
        
        # Suponemos inicialmente que el mínimo y el máximo están en el índice 'i'
        indice_min = i
        indice_max = i
        
        # Buscamos en el rango desordenado actual (entre 'i' y 'n - i - 1')
        for j in range(i + 1, n - i):
            
            # Si encontramos un elemento menor, actualizamos el índice del mínimo
            if arreglo[j] < arreglo[indice_min]:
                indice_min = j
                
            # Si encontramos un elemento mayor, actualizamos el índice del máximo
            elif arreglo[j] > arreglo[indice_max]:
                indice_max = j
                
        # Intercambiamos el elemento mínimo encontrado con el primer elemento de nuestro rango
        arreglo[i], arreglo[indice_min] = arreglo[indice_min], arreglo[i]
        
        # CASO ESPECIAL: Si resulta que el elemento máximo estaba justo en la posición 'i',
        # al hacer el intercambio anterior, el máximo se movió a 'indice_min'.
        # Debemos actualizar 'indice_max' para no perderlo.
        if indice_max == i:
            indice_max = indice_min
            
        # Intercambiamos el elemento máximo encontrado con el último elemento de nuestro rango
        arreglo[n - i - 1], arreglo[indice_max] = arreglo[indice_max], arreglo[n - i - 1]

    # Retornamos el arreglo ordenado
    return arreglo


# ==========================================
# Ejemplo de uso
# ==========================================
if __name__ == "__main__":
    lista_1 = [23, 78, 45, 8, 32, 56, 1]
    print("Selección Bidireccional Original:", lista_1)
    print("Selección Bidireccional Ordenada:", seleccion_bidireccional(lista_1))
