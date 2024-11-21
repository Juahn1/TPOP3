import random
import time
import heapq  # Importar el módulo para la cola de prioridad

# Variable global para métricas
nodos_explorados = 0


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
    global nodos_explorados  # Declaración explícita
    tablero = [[0 for i in range(9)] for i in range(9)]
    # Se usa Backtracking para generar un tablero completamente resuelto.
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
        celdas_a_quedar = random.randint(10, 11)
    else:
        raise ValueError("Dificultad no válida. Usa: 'facil', 'medio', 'dificil'.")
    celdas_a_vaciar = 81 - celdas_a_quedar

    while celdas_a_vaciar > 0:
        fila = random.randint(0, 8)
        columna = random.randint(0, 8)
        if tablero_modificado[fila][columna] != 0:
            # Eliminar la celda solo si no afecta la unicidad de la solución
            original = tablero_modificado[fila][columna]
            tablero_modificado[fila][columna] = 0
            if not tiene_una_sola_solucion(tablero_modificado):
                tablero_modificado[fila][columna] = original  # Restaurar la celda si causa múltiples soluciones
            else:
                celdas_a_vaciar -= 1
    return tablero_modificado


# Verificar si un tablero tiene una única solución
def tiene_una_sola_solucion(tablero):
    soluciones = []
    resolver_con_soluciones(tablero, soluciones)
    return len(soluciones) == 1


# Resolver el Sudoku con Backtracking, permitiendo la recolección de todas las soluciones
def resolver_con_soluciones(tablero, soluciones):
    global nodos_explorados  # Declaración explícita
    for fila in range(9):
        for columna in range(9):
            if tablero[fila][columna] == 0:  # Celda vacía
                for numero in range(1, 10):  # Probar números del 1 al 9
                    nodos_explorados += 1  # Incrementar el contador de nodos explorados
                    if es_valido(tablero, fila, columna, numero):
                        tablero[fila][columna] = numero
                        resolver_con_soluciones(tablero, soluciones)
                        if len(soluciones) > 1:
                            return  # Ya hay más de una solución, dejamos de buscar
                        tablero[fila][columna] = 0  # Backtracking
                return
    # Cuando no hay celdas vacías, es una solución válida
    soluciones.append([fila[:] for fila in tablero])


# Imprimir el tablero de forma legible
def imprimir_tablero(tablero):
    for fila in tablero:
        print(" ".join(str(num) if num != 0 else "." for num in fila))


# Resolver el Sudoku con Backtracking
def resolver_backtracking(tablero):
    global nodos_explorados  # Declaración explícita
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


# Resolver el Sudoku con Ramificación y Poda (Branch and Bound)
def resolver_branch_and_bound(tablero):
    """
    Resolver Sudoku utilizando Ramificación y Poda con una cola de prioridad.
    """
    global nodos_explorados  # Declaración explícita
    nodos_explorados = 0  # Reiniciar contador de nodos explorados

    # Calcular prioridad basada en las posibilidades de una celda
    def calcular_prioridad(tablero, fila, columna):
        return len([n for n in range(1, 10) if es_valido(tablero, fila, columna, n)])

    # Generar lista inicial de celdas vacías con su prioridad
    def inicializar_cola_prioridad(tablero):
        heap = []
        for fila in range(9):
            for columna in range(9):
                if tablero[fila][columna] == 0:  # Celda vacía
                    prioridad = calcular_prioridad(tablero, fila, columna)
                    heapq.heappush(heap, (prioridad, fila, columna))
        return heap

    # Implementación de Ramificación y Poda
    def branch_and_bound(tablero):
        global nodos_explorados  # Declaración explícita
        heap = inicializar_cola_prioridad(tablero)  # Inicializar la cola de prioridad
        if not heap:  # Si no hay celdas vacías, el tablero está resuelto
            return True

        # Extraer celda con menor prioridad
        _, fila, columna = heapq.heappop(heap)
        posibilidades = [n for n in range(1, 10) if es_valido(tablero, fila, columna, n)]

        for numero in posibilidades:
            nodos_explorados += 1  # Incrementar contador de nodos explorados
            tablero[fila][columna] = numero  # Asignar número temporal
            if branch_and_bound(tablero):  # Llamada recursiva
                return True
            tablero[fila][columna] = 0  # Backtracking

        # Si no se encuentra solución
        return False

    solucion = branch_and_bound(tablero)
    return solucion


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
        while True:
            print("\n1- Resolver con Backtracking")
            print("2- Resolver con Branch and Bound")
            print("0- Salir")
            resolver_opcion = input("Seleccionar un método de resolución: ")

            if resolver_opcion == "0":
                break

            elif resolver_opcion in ["1", "2"]:
                metodo = "Backtracking" if resolver_opcion == "1" else "Branch and Bound"
                print(f"\nResolviendo con {metodo}...")
                global nodos_explorados  # Declaración explícita
                nodos_explorados = 0  # Reiniciar el contador antes de resolver
                tiempo_inicio = time.time()
                tablero_copia = [fila[:] for fila in tablero_incompleto]  # Copiar tablero para preservar estado
                if resolver_opcion == "1":
                    solucion = resolver_backtracking(tablero_copia)
                else:
                    solucion = resolver_branch_and_bound(tablero_copia)
                tiempo_fin = time.time()
                if solucion:
                    print("\nTablero resuelto:")
                    imprimir_tablero(tablero_copia)
                else:
                    print("\nNo se encontró solución.")
                print(f"\nTiempo de ejecución: {tiempo_fin - tiempo_inicio:.4f} segundos")
                print(f"Nodos explorados: {nodos_explorados}")
            else:
                print("Opción no válida.")

main()
