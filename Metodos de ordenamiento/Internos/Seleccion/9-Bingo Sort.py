def bingo_sort(arreglo):
    """
    Ordena una lista utilizando el algoritmo Bingo Sort.
    Ideal para listas con muchos elementos repetidos.
    
    Explicación del proceso:
    1. Encuentra el valor máximo de toda la lista y el valor mínimo actual ("bingo").
    2. Recorre la lista buscando todos los elementos iguales al "bingo" y los acomoda.
    3. Al mismo tiempo, descubre cuál es el siguiente elemento más pequeño para la siguiente ronda.
    4. Repite el proceso hasta que el "bingo" alcance al valor máximo.
    """
    
    n = len(arreglo)
    if n <= 1:
        return arreglo
        
    # Encontramos el valor más pequeño y el más grande de todo el arreglo
    bingo = min(arreglo)
    valor_maximo = max(arreglo)
    
    # Esta variable nos ayudará a encontrar el siguiente número a procesar
    siguiente_bingo = valor_maximo
    
    # 'posicion_actual' indica dónde debemos colocar el próximo elemento ordenado
    posicion_actual = 0
    
    # El bucle continúa hasta que hayamos procesado incluso el valor máximo
    while bingo < valor_maximo:
        
        # Reiniciamos la búsqueda del siguiente número menor
        siguiente_bingo = valor_maximo
        
        # Recorremos la porción de la lista que aún no está ordenada
        for i in range(posicion_actual, n):
            
            # ¡BINGO! Encontramos un número que coincide con nuestro objetivo actual
            if arreglo[i] == bingo:
                # Lo intercambiamos para ponerlo en su lugar definitivo
                arreglo[i], arreglo[posicion_actual] = arreglo[posicion_actual], arreglo[i]
                # Avanzamos la posición para el siguiente acierto
                posicion_actual += 1
                
            # Si no es un "bingo", pero es menor que nuestro 'siguiente_bingo' candidato,
            # lo guardamos porque será nuestro objetivo en la próxima ronda de todo el bucle 'while'
            elif arreglo[i] < siguiente_bingo:
                siguiente_bingo = arreglo[i]
                
        # Actualizamos el objetivo para la siguiente iteración
        bingo = siguiente_bingo

    return arreglo


# ==========================================
# Ejemplo de uso
# ==========================================
if __name__ == "__main__":
    lista_2 = [5, 2, 5, 1, 2, 8, 1, 5, 8] # Lista con muchos duplicados
    print("\nBingo Sort Original:", lista_2)
    print("Bingo Sort Ordenada:", bingo_sort(lista_2))
