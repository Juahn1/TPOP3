import random
import time

# Variable global para métricas
nodos_explorados = 0


# Resolver el Sudoku con Branch and Bound
def resolver_branch_and_bound(tablero):
    global nodos_explorados
    nodos_explorados = 0  # Reiniciar el contador de nodos explorados

    # Función para encontrar la celda con menos opciones posibles (heurística MRV)
    def encontrar_celda_mas_restringida(tablero):
        min_opciones = 10  # Más que cualquier opción posible
        celda_mas_restringida = (-1, -1)
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] == 0:  # Solo considerar celdas vacías
                    # Contar opciones válidas para esta celda
                    opciones = sum(1 for num in range(1, 10) if es_valido(tablero, fila, col, num))
                    if opciones < min_opciones:  # Actualizar si es la celda más restringida hasta ahora
                        min_opciones = opciones
                        celda_mas_restringida = (fila, col)
        return celda_mas_restringida

    # Función recursiva para aplicar Branch and Bound
    def branch_and_bound(tablero):
        global nodos_explorados
        # Encontrar la celda más restringida (aplicación de la heurística MRV)
        celda = encontrar_celda_mas_restringida(tablero)  # MRV: selecciona la celda más restringida
        if celda == (-1, -1):  # No hay celdas vacías, el tablero está resuelto
            return True

        fila, col = celda
        for num in range(1, 10):
            nodos_explorados += 1  # Contador de nodos explorados
            if es_valido(tablero, fila, col, num):  # Verificar si el número es válido en esta celda
                tablero[fila][col] = num  # Asignar número

                # Cota inferior: continuar si el tablero sigue siendo válido
                if branch_and_bound(tablero):  # Recursión
                    return True

                # Retroceder (backtracking)
                tablero[fila][col] = 0

        # Si no se puede asignar ningún número válido, es necesario retroceder
        return False

    # Llamar al algoritmo de Branch and Bound
    return branch_and_bound(tablero)


# Función para verificar si un número es válido en una celda
def es_valido(tablero, fila, columna, numero):
    if numero in tablero[fila]:
        return False
    for i in range(9):
        if tablero[i][columna] == numero:
            return False
    inicio_fila = (fila // 3) * 3
    inicio_columna = (columna // 3) * 3
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_columna, inicio_columna + 3):
            if tablero[i][j] == numero:
                return False
    return True


# Generar un tablero completo usando Backtracking
def generar_tablero_completo():
    tablero = [[0 for i in range(9)] for i in range(9)]
    numeros_colocados = 0
    while numeros_colocados < 9:
        fila = random.randint(0, 8)
        columna = random.randint(0, 8)
        numero = random.randint(1, 9)
        if tablero[fila][columna] == 0 and es_valido(tablero, fila, columna, numero):
            tablero[fila][columna] = numero
            numeros_colocados += 1
    if not resolver_backtracking(tablero):
        raise ValueError("No se pudo generar un tablero válido.")
    return tablero


# Modificar el tablero según la dificultad seleccionada
def eliminar_celdas(tablero, dificultad):
    tablero_modificado = [fila[:] for fila in tablero]  # Copia del tablero
    if dificultad == "facil":
        celdas_a_quedar = random.randint(35, 50)
    elif dificultad == "medio":
        celdas_a_quedar = random.randint(22, 34)
    elif dificultad == "dificil":
        celdas_a_quedar = random.randint(10, 21)
    else:
        raise ValueError("Dificultad no válida. Usa: 'facil', 'medio', 'dificil'.")
    celdas_a_vaciar = 81 - celdas_a_quedar
    while celdas_a_vaciar > 0:
        fila = random.randint(0, 8)
        columna = random.randint(0, 8)
        if tablero_modificado[fila][columna] != 0:
            tablero_modificado[fila][columna] = 0
            celdas_a_vaciar -= 1
    return tablero_modificado

# Permitir al usuario ingresar un tablero manualmente con validación
def ingresar_tablero():
    print("Ingresa el tablero fila por fila. Usa espacios para separar los números y 0 para celdas vacías.")
    tablero = [[0] * 9 for fila in range(9)]  # Inicializa un tablero vacío
    
    for i in range(9):
        while True:
            try:
                fila = list(map(int, input(f"Fila {i + 1}: ").split()))
                
                # Verificar longitud y rango de números
                if len(fila) != 9 or not all(0 <= num <= 9 for num in fila):
                    print("Cada fila debe tener exactamente 9 números entre 0 y 9.")
                    continue
                
                # Verificar duplicados en la fila ingresada
                numeros_no_vacios = [num for num in fila if num != 0]
                if len(numeros_no_vacios) != len(set(numeros_no_vacios)):
                    print("La fila ingresada contiene números repetidos. Intenta de nuevo.")
                    continue
                
                # Validar reglas del Sudoku para cada celda
                es_valida = True
                for j, num in enumerate(fila):
                    if num != 0 and not es_valido(tablero, i, j, num):
                        es_valida = False
                        break
                
                if es_valida:
                    tablero[i] = fila  # Fila válida, asignarla al tablero
                    break
                else:
                    print("La fila ingresada viola las reglas del Sudoku. Intenta de nuevo.")
            
            except ValueError:
                print("Entrada inválida. Asegúrate de ingresar números separados por espacios.")
    
    return tablero


# Imprimir el tablero de forma legible
def imprimir_tablero(tablero):
    for fila in tablero:
        print(" ".join(str(num) if num != 0 else "." for num in fila))

# Resolver el Sudoku con Backtracking, contando nodos explorados
def resolver_backtracking(tablero):
    global nodos_explorados
    for fila in range(9):
        for columna in range(9):
            if tablero[fila][columna] == 0:  # Celda vacía
                for numero in range(1, 10):  # Probar números del 1 al 9
                    nodos_explorados += 1  # Incrementar el contador de nodos explorados
                    if es_valido(tablero, fila, columna, numero):
                        tablero[fila][columna] = numero
                        if resolver_backtracking(tablero):
                            return True
                        tablero[fila][columna] = 0  # Backtracking
                return False
    return True  # Tablero resuelto


def resolver_manual(tablero_inicial):
    print("Por favor, ingresa las filas una por una (separadas por espacios). Usar 0 para las celdas vacías.")
    
    # Copiamos el tablero inicial para trabajar sobre él y no modificar el original
    tablero = [fila.copy() for fila in tablero_inicial]
    
    for fila in range(9):
        while True:
            # Mostrar el tablero con los valores actuales, marcando las celdas vacías con '.'
            fila_actual = " ".join([str(tablero[fila][col]) if tablero[fila][col] != 0 else '.' for col in range(9)])
            print(f"Fila {fila + 1}: {fila_actual}")
            
            fila_usuario = input(f"Ingrese la fila {fila + 1}: ").strip().split()
            fila_usuario = [int(x) for x in fila_usuario]
            
            # Verifica que la fila tenga exactamente 9 elementos
            if len(fila_usuario) != 9:
                print("La fila no tiene 9 elementos, por favor ingresar de nuevo.")
                continue
            
            # Verificar que el usuario no intente modificar celdas preexistentes del tablero
            for i in range(9):
                # Solo se permiten cambios si la celda está vacía en el tablero original
                if tablero_inicial[fila][i] == 0:
                    tablero[fila][i] = fila_usuario[i]
                elif tablero_inicial[fila][i] != 0 and tablero[fila][i] != fila_usuario[i]:
                    print(f"No puedes modificar los valores existentes del tablero.")
                    break
            else:
                # Si la fila se ha completado correctamente sin errores, salimos del ciclo
                break

    # Ahora validamos el tablero (filas, columnas y subcuadros)
    valido = True
    
    # Validar filas
    for fila in tablero:
        numeros = [num for num in fila if num != 0]
        if len(numeros) != len(set(numeros)):  # Si hay duplicados, no es válido
            valido = False
            break

    # Validar columnas
    if valido:
        for col in range(9):
            columna = [tablero[fila][col] for fila in range(9)]
            numeros = [num for num in columna if num != 0]
            if len(numeros) != len(set(numeros)):  # Si hay duplicados, no es válido
                valido = False
                break

    # Validar subcuadros 3x3
    if valido:
        for fila in range(0, 9, 3):
            for col in range(0, 9, 3):
                subcuadro = []
                for i in range(3):
                    for j in range(3):
                        subcuadro.append(tablero[fila + i][col + j])
                numeros = [num for num in subcuadro if num != 0]
                if len(numeros) != len(set(numeros)):  # Si hay duplicados, no es válido
                    valido = False
                    break

    if valido:
        print("\n¡El tablero está correctamente resuelto!")
        imprimir_tablero(tablero)
    else:
        print("\nEl tablero NO está bien resuelto. Hay errores.")
        imprimir_tablero(tablero)



# Función principal
def main():
    print("\nTrabajo Práctico Obligatorio - Resolución de un Sudoku")
    while True:
        print("\n1- Generar un tablero de Sudoku automáticamente.")
        print("2- Ingresar el tablero de forma manual.")
        print("0- Salir")
        opcion = input("Seleccionar una opción: ")
        
        if opcion == "0":
            print("Fin del programa.")
            break

        elif opcion == "1":
            tablero_completo = generar_tablero_completo()
            print("\nElegir nivel de dificultad:")
            print("1- Fácil (entre 35 y 50 números en el tablero inicial)")
            print("2- Medio (entre 22 y 34 números en el tablero inicial)")
            print("3- Dificil (entre 10 y 21 números en el tablero inicial)")
            print("0- Salir")
            dificultad_opcion = input("Seleccionar la dificultad: ")

            if dificultad_opcion == "0":
                continue
            dificultad = {"1": "facil", "2": "medio", "3": "dificil"}.get(dificultad_opcion)
            if not dificultad:
                print("Dificultad no válida.")
                continue
            tablero_incompleto = eliminar_celdas(tablero_completo, dificultad)

        elif opcion == "2":
            tablero_incompleto = ingresar_tablero()
        else:
            print("Opción no válida.")
            continue

        print("\nTablero inicial:")
        imprimir_tablero(tablero_incompleto)
        print("\n1- Resolver automáticamente con Backtracking")
        print("2- Resolver manualmente")
        print("3- Resolver automáticamente con Branch and Bound")
        print("0- Salir")
        resolver_opcion = input("Seleccionar un método de resolución: ")

        if resolver_opcion == "0":
            continue
        
        elif resolver_opcion == "1":
            print("\nResolviendo automáticamente con Backtracking...")
            global nodos_explorados
            nodos_explorados = 0  # Reiniciar el contador antes de resolver
            tiempo_inicio = time.time()
            solucion = resolver_backtracking(tablero_incompleto)
            tiempo_fin = time.time()
            if solucion:
                print("\nTablero resuelto:")
                imprimir_tablero(tablero_incompleto)
            else:
                print("\nNo se encontró solución.")
            print(f"\nTiempo de ejecución: {tiempo_fin - tiempo_inicio:.4f} segundos")
            print(f"Nodos explorados: {nodos_explorados}")
        
        elif resolver_opcion == "2":
            resolver_manual(tablero_incompleto)
            print("\nTablero final:")
            imprimir_tablero(tablero_incompleto)
        
        elif resolver_opcion == "3":
            print("\nResolviendo automáticamente con Branch and Bound...")
            nodos_explorados = 0  # Reiniciar el contador antes de resolver
            tiempo_inicio = time.time()
            solucion = resolver_branch_and_bound(tablero_incompleto)
            tiempo_fin = time.time()
            if solucion:
                print("\nTablero resuelto:")
                imprimir_tablero(tablero_incompleto)
            else:
                print("\nNo se encontró solución.")
            print(f"\nTiempo de ejecución: {tiempo_fin - tiempo_inicio:.4f} segundos")
            print(f"Nodos explorados: {nodos_explorados}")
        
        else:
            print("Opción no válida.")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
