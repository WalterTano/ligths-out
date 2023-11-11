import numpy as np
import lights_out_sim

# Genera el sistema de ecuaciones correspondiente al tablero de lights out provisto.
def generar_sistema(tablero):
    tamano = len(tablero)
    tamano_cuadrado = tamano ** 2
    matriz_sistema = np.zeros((tamano_cuadrado, tamano_cuadrado), dtype=int) # Generamos matriz vacía
    for i in range(0, tamano_cuadrado):
        for j in range(0, tamano_cuadrado):
            if i == j: # Es el mismo botón
                matriz_sistema[i, j] = 1
            elif (i // tamano == j // tamano and abs(i - j) == 1) or (  # El botón está a la izquierda o a la derecha
                    i % tamano == j % tamano and abs(i - j) == tamano): # El botón está arriba o abajo
                matriz_sistema[i, j] = 1
                
    entradas = np.array(tablero).flatten().T
    entradas.resize(tamano_cuadrado, 1)
    matriz_sistema = np.hstack((matriz_sistema, entradas))
    return matriz_sistema

# Dada la matriz aumentada del sistema de ecuaciones de un tablero y su tamaño, se construye la forma
# escalonada de la matriz.
def escalonar_tablero(matriz_aumentada, tamano_cuadrado):
    for fila in range(0, tamano_cuadrado - 1):
        # Si hay un 0 en la diagonal principal, cambiamos la fila por la siguiente con un 1.
        if matriz_aumentada[fila, fila] == 0: 
            prox_fila_no_cero = np.argmax(matriz_aumentada[fila + 1:, fila]) + fila + 1
            matriz_aumentada[[fila, prox_fila_no_cero]] = matriz_aumentada[[prox_fila_no_cero, fila]]

        # Por cada fila siguiente, verificamos si es afectada por el primer 1 de la fila actual y, de ser así, 
        # se la sumamos (con suma binaria).
        # De esta forma, nos aseguramos que solo hayan 0s por debajo de los primeros 1s de todas las filas.
        for i in range(fila + 1, tamano_cuadrado):
            if matriz_aumentada[i, fila] == 1:
                matriz_aumentada[i] = lights_out_sim.suma_binaria(matriz_aumentada[i], matriz_aumentada[fila])
                
    return matriz_aumentada
                
# Dada la forma triangular superior de la matriz aumentada del sistema de ecuaciones de un tablero y su tamaño, 
# se realiza una eliminación hacia atrás usando operaciones elementales.
def eliminar_hacia_atras(matriz_escalonada, tamano_cuadrado):
    for columna in range(tamano_cuadrado - 1, 0, -1):
        for i in range(columna - 1, -1, -1):
            # Por cada fila y columna, en orden ascendente, si en una fila anterior hay un 1 en la misma columna,
            # se le suma (con suma binaria) la fila actual para eliminar el 1.
            if matriz_escalonada[i, columna] == 1:
                matriz_escalonada[i] = lights_out_sim.suma_binaria(matriz_escalonada[i], matriz_escalonada[columna])
                
    return matriz_escalonada

# Genera un vector de solución a partir de un tablero de lights out.
def obtener_solucion(tablero):
    tamano = len(tablero)
    tamano_cuadrado = tamano ** 2
    matriz_sistema_aumentada = generar_sistema(tablero)

    # Escalonamos la matriz.
    msa_escalonada = escalonar_tablero(matriz_sistema_aumentada, tamano_cuadrado)

    # Realizamos eliminación hacia atrás para obtener la solución.
    msa_solucion = eliminar_hacia_atras(msa_escalonada, tamano_cuadrado)

    vector_solucion = msa_solucion[:, -1]
    return vector_solucion

tablero = lights_out_sim.generar_tablero_aleatorio(6)
print(f'Tablero inicial:\n{tablero}')
vector_solucion = obtener_solucion(tablero)
print(f'Vector de solución:\n{vector_solucion}')
print(f'Solución en formato de matriz:\n{vector_solucion.reshape((len(tablero), len(tablero)))}')
lights_out_sim.resolver_tablero(tablero, vector_solucion)