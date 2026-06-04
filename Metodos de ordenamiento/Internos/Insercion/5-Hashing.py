def funcion_hash(valor, max_valor, num_cubetas):
    """
    Función auxiliar para calcular la 'dirección' o índice de la cubeta.
    Mapea el 'valor' proporcionalmente al número de cubetas disponibles.
    """
    # Retorna 0 si el valor máximo es 0 para evitar errores de división por cero.
    if max_valor == 0:
        return 0
        
    # Se calcula la posición relativa del valor dentro del rango máximo
    # y se multiplica por el índice máximo posible (num_cubetas - 1).
    # Usamos '//' para asegurar un índice entero.
    return (valor * (num_cubetas - 1)) // max_valor


def ordenamiento_por_hashing(arreglo):
    """
    Ordena una lista utilizando Ordenamiento por Hashing (Address Calculation Sort).
    
    Explicación del proceso:
    1. Se crea una tabla hash (una lista de listas o "cubetas").
    2. A cada elemento se le aplica la función Hash para calcular su "dirección".
    3. Se inserta el elemento en su cubeta correspondiente.
    4. La inserción dentro de la cubeta se hace manteniendo el orden (Inserción Directa).
    5. Finalmente, se concatenan todas las cubetas para obtener la lista final.
    """
    
    # Obtenemos la longitud del arreglo. Si está vacío o tiene 1 elemento, ya está ordenado.
    n = len(arreglo)
    if n <= 1:
        return arreglo
        
    # Buscamos el valor máximo en el arreglo para que nuestra función hash sepa el límite.
    max_valor = max(arreglo)
    
    # Creamos nuestra "Tabla Hash". Será una lista que contiene 'n' listas vacías (cubetas).
    # Crear 'n' cubetas suele ofrecer la mejor distribución uniforme.
    cubetas = [[] for _ in range(n)]
    
    # Recorremos cada elemento del arreglo original para distribuirlo.
    for valor in arreglo:
        
        # Obtenemos la dirección (índice) aplicando nuestra función hash.
        indice = funcion_hash(valor, max_valor, n)
        
        # Seleccionamos la cubeta específica donde debe ir el valor.
        cubeta_actual = cubetas[indice]
        
        # =================================================================
        # FASE DE INSERCIÓN (El núcleo que lo vincula a esta familia)
        # =================================================================
        
        # Agregamos el valor al final de su cubeta correspondiente...
        cubeta_actual.append(valor)
        
        # ...y aplicamos Inserción Directa para acomodarlo en su lugar correcto.
        # Empezamos a comparar desde el penúltimo elemento de la cubeta.
        j = len(cubeta_actual) - 2
        
        # Desplazamos a la derecha los elementos de la cubeta que sean mayores al 'valor'.
        while j >= 0 and cubeta_actual[j] > valor:
            cubeta_actual[j + 1] = cubeta_actual[j]
            j -= 1
            
        # Colocamos el valor en su posición estrictamente ordenada dentro de la cubeta.
        cubeta_actual[j + 1] = valor

    # =================================================================
    # FASE DE RECOLECCIÓN
    # =================================================================
    
    # Vaciamos las cubetas (que ya están ordenadas internamente) de vuelta al arreglo original.
    indice_arreglo = 0
    for cubeta in cubetas:
        for elemento in cubeta:
            arreglo[indice_arreglo] = elemento
            indice_arreglo += 1
            
    # Retornamos el arreglo totalmente ordenado.
    return arreglo


# ==========================================
# Ejemplo de uso y prueba del algoritmo
# ==========================================

if __name__ == "__main__":
    # Definimos una lista desordenada con valores dispersos
    lista_desordenada = [89, 12, 65, 98, 23, 44, 76, 5, 33, 50]
    
    # Imprimimos la lista original
    print("Lista original:", lista_desordenada)
    
    # Llamamos a nuestra función de Ordenamiento por Hashing
    lista_ordenada = ordenamiento_por_hashing(lista_desordenada)
    
    # Imprimimos la lista después de ordenar
    print("Lista ordenada:", lista_ordenada)
