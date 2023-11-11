import numpy as np
from random import randint

# Genera un vector de solución a partir de un tablero de lights out.
def obtener_solucion(tablero):
    tamano = len(tablero)
    tamano_cuadrado = tamano ** 2
    matriz_sistema = generar_sistema(tablero)
    entradas = np.array(tablero).flatten().T
    entradas.resize(tamano_cuadrado, 1)
    matriz_aumentada = np.hstack((matriz_sistema, entradas))

    # Escalonamos la matriz.
    matriz_aumentada_escalonada = escalonar_tablero(matriz_aumentada, tamano_cuadrado)

    # Convertimos la matriz escalonada a la matriz identidad para obtener la solución.
    matriz_aumentada_identidad = obtener_matriz_identidad(matriz_aumentada_escalonada, tamano_cuadrado)

    respuesta = matriz_aumentada_identidad[:, -1]
    return respuesta

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
                matriz_aumentada[i] = suma_binaria(matriz_aumentada[i], matriz_aumentada[fila])
                
    return matriz_aumentada
                
def obtener_matriz_identidad(matriz_escalonada, tamano_cuadrado):
    for columna in range(tamano_cuadrado - 1, 0, -1):
        for i in range(columna - 1, -1, -1):
            # Por cada fila y columna, en orden ascendente, si en una fila anterior hay un 1 en la misma columna,
            # se le suma (con suma binaria) la fila actual para eliminar el 1.
            if matriz_escalonada[i, columna] == 1:
                matriz_escalonada[i] = suma_binaria(matriz_escalonada[i], matriz_escalonada[columna])
                
    return matriz_escalonada
    
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
                
    return matriz_sistema

# Popula un tablero aleatoriamente.
# Esta función no garantiza generar un tablero con solución para las dimensiones 4x4 y 5x5.
def generar_tablero_aleatorio(tamano):
    tablero = []
    for i in range(0, tamano):
        fila = []
        for j in range(0, tamano):
            fila.append(randint(0, 1))
            
        tablero.append(fila)
                        
    return np.array(tablero)

# Resuelve un tablero a partir de un vector de solución.
def resolver_tablero(tablero, vector_solucion):
    if len(tablero) ** 2 != len(vector_solucion):
        print('El vector solución no es compatible con el tablero.')
        
    pasos = 0
    pos_vector_solucion = 0
    print('======== Resolviendo Tablero ========')
    for i in range(0, len(tablero)):
        for j in range(0, len(tablero)):
            if vector_solucion[pos_vector_solucion] == 1:
                pasos += 1
                tablero = simular_boton(tablero, i, j)
                print(f'Paso {pasos} (Botón [{i}, {j}]):\n{tablero}')
                
            pos_vector_solucion += 1
                
    print('======== Tablero Resuelto ========')

# Simula la presión de un botón en un tablero de lights out.
def simular_boton(tablero, i, j):
    tablero[i, j] = suma_binaria(tablero[i, j], 1)
    # Aplicamos cambios sobre los botones adyancentes
    if i > 0: # Arriba
        tablero[i - 1, j] = suma_binaria(tablero[i - 1, j], 1)
    if i < len(tablero) - 1: # Abajo
        tablero[i + 1, j] = suma_binaria(tablero[i + 1, j], 1)
        
    if j > 0: # Izquierda
        tablero[i, j - 1] = suma_binaria(tablero[i, j - 1], 1)
    if j < len(tablero[i]) - 1: # Derecha
        tablero[i, j + 1] = suma_binaria(tablero[i, j + 1], 1)
        
    return tablero
    
def suma_binaria(a, b):
    return (a + b) % 2
    
# Tablero de ejemplo
tablero = np.array([
    [1, 1, 1, 1, 0],
    [0, 0, 1, 1, 0],
    [1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 1, 1]
])
tablero = generar_tablero_aleatorio(7)
print(f'Tablero inicial:\n{tablero}')
vector_solucion = obtener_solucion(tablero)
print(f'Vector de solución:\n{vector_solucion}')
print(f'Solución en formato de matriz:\n{vector_solucion.reshape((len(tablero), len(tablero)))}')
resolver_tablero(tablero, vector_solucion)