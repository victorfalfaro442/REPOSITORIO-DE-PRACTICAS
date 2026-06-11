def ordenamiento_conteo(arreglo):
    """
    Ordena una lista utilizando el algoritmo de Counting Sort.
    Soporta números negativos gracias al cálculo del desplazamiento (offset).
    
    Explicación del proceso:
    1. Encuentra los valores mínimo y máximo para determinar el rango de datos.
    2. Crea una lista auxiliar de "conteo" llena de ceros.
    3. Registra la frecuencia de cada número en la lista de conteo.
    4. Reconstruye el arreglo original vaciando las frecuencias en orden.
    """
    # Si el arreglo está vacío o tiene un solo elemento, ya está ordenado.
    if len(arreglo) <= 1:
        return arreglo
        
    # Encontramos los valores extremos para conocer el tamaño del rango.
    min_val = min(arreglo)
    max_val = max(arreglo)
    
    # El rango define cuántas posiciones necesitamos en nuestra lista auxiliar.
    rango = max_val - min_val + 1
    
    # Creamos la lista de conteo inicializada en cero para cada valor del rango.
    conteo = [0] * rango
    
    # Fase de Enumeración: Recorremos el arreglo original.
    # Restamos 'min_val' para que el número más pequeño se mapee correctamente al índice 0.
    for numero in arreglo:
        conteo[numero - min_val] += 1
        
    # Fase de Reconstrucción: Volvemos a llenar el arreglo original.
    indice_original = 0
    
    # Recorremos la lista de conteo
    for i in range(rango):
        # Mientras queden elementos por colocar de este valor específico...
        while conteo[i] > 0:
            # Recuperamos el valor original sumando de vuelta el 'min_val'
            arreglo[indice_original] = i + min_val
            # Avanzamos al siguiente espacio del arreglo original
            indice_original += 1
            # Decrementamos el contador de la frecuencia
            conteo[i] -= 1
            
    # Retornamos el arreglo completamente ordenado
    return arreglo


# ==========================================
# Ejemplo de uso
# ==========================================
if __name__ == "__main__":
    lista_1 = [4, -2, 2, 8, 3, 3, 1]
    print("Counting Sort Original:", lista_1)
    print("Counting Sort Ordenada:", ordenamiento_conteo(lista_1))
