def ordenamiento_casilleros(arreglo):
    """
    Ordena una lista utilizando el algoritmo Pigeonhole Sort.
    
    Explicación del proceso:
    1. Encuentra el rango de valores (máximo - mínimo + 1).
    2. Crea un "casillero" (sublista) para cada valor posible del rango.
    3. Mueve cada elemento de la lista original a su casillero correspondiente.
    4. Recorre los casilleros en orden y extrae los elementos de vuelta al arreglo.
    """
    if len(arreglo) <= 1:
        return arreglo
        
    min_val = min(arreglo)
    max_val = max(arreglo)
    rango = max_val - min_val + 1
    
    # Creamos un arreglo de casilleros. Cada casillero es una lista vacía.
    casilleros = [[] for _ in range(rango)]
    
    # Distribuimos los elementos en sus respectivos casilleros.
    # Usamos (numero - min_val) como el índice del casillero.
    for numero in arreglo:
        casilleros[numero - min_val].append(numero)
        
    # Reunimos los elementos de los casilleros de vuelta en el arreglo original.
    indice_original = 0
    for casillero in casilleros:
        for elemento in casillero:
            arreglo[indice_original] = elemento
            indice_original += 1
            
    return arreglo


# ==========================================
# Ejemplo de uso
# ==========================================
if __name__ == "__main__":
    lista_2 = [102, 107, 101, 102, 105]
    print("\nPigeonhole Sort Original:", lista_2)
    print("Pigeonhole Sort Ordenada:", ordenamiento_casilleros(lista_2))
