import numpy as np
from random import randint

# Retorna la suma binaria de dos variables.
def suma_binaria(a, b):
    return (a + b) % 2

# Popula un tablero aleatoriamente.
# Esta función no garantiza generar un tablero con solución.
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