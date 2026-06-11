def ordenamiento_enumeracion_pura(arreglo):
    """
    Ordena una lista utilizando el algoritmo de Enumeración Pura (Rank Sort).
    
    Explicación del proceso:
    1. Toma un elemento de la lista.
    2. Compara ese elemento contra todos los demás y cuenta cuántos son menores que él.
    3. Coloca el elemento directamente en la posición que indica ese conteo.
    4. Resuelve duplicados comparando los índices originales de los elementos.
    """
    n = len(arreglo)
    
    # Creamos un arreglo temporal vacío del mismo tamaño para ir armando el resultado.
    resultado = [0] * n
    
    # Recorremos cada elemento de la lista para calcular su "rango" o posición final.
    for i in range(n):
        elementos_menores = 0
        
        # Comparamos el elemento actual 'arreglo[i]' contra el resto de la lista.
        for j in range(n):
            
            # Condición 1: Si encontramos un elemento que es estrictamente menor, aumentamos el rango.
            if arreglo[j] < arreglo[i]:
                elementos_menores += 1
                
            # Condición 2 (Manejo de Duplicados): Si los elementos son iguales, 
            # para evitar que terminen en la misma posición, el que apareció primero 
            # en la lista original (j < i) se considera "menor".
            elif arreglo[j] == arreglo[i] and j < i:
                elementos_menores += 1
                
        # Una vez contado cuántos elementos son menores, sabemos su posición exacta.
        resultado[elementos_menores] = arreglo[i]
        
    # Copiamos los elementos ordenados del arreglo 'resultado' de vuelta al 'arreglo' original.
    for i in range(n):
        arreglo[i] = resultado[i]
        
    return arreglo


# ==========================================
# Ejemplo de uso
# ==========================================
if __name__ == "__main__":
    lista_3 = [45, 12, 45, 8, 23]
    print("\nEnumeración Pura Original:", lista_3)
    print("Enumeración Pura Ordenada:", ordenamiento_enumeracion_pura(lista_3))
