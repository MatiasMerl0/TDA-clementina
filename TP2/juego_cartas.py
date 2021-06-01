import sys

def procesar_archivo(ruta):
    '''
    Recibe la ruta al archivo con las cartas, devuelve un arreglo con los valores en el mismo orden
    El archivo debe ser de extension .txt con las cartas separadas por comas
    Ej: 7,5,1,8
    '''
    archivo = open(ruta, 'r')
    texto = archivo.read()
    cartas_strv = texto.split(',')
    for i in range(len(cartas_strv)):
        cartas_strv[i] = int(cartas_strv[i])
    return cartas_strv



def mostrar_resultados(cartas_jugador_1, cartas_jugador_2):
    '''
    Dadas las elecciones de cada jugador, imprime por pantalla las elecciones y la suma total
    '''
    print("Jugador 1: ")
    print("Cartas elegidas:", end=' ')
    for i in range(len(cartas_jugador_1)):
        if i != len(cartas_jugador_1) - 1:
            print(cartas_jugador_1[i], end=',')
        else:
            print(cartas_jugador_1[i])
    print("puntos sumados:", sum(cartas_jugador_1))
    print()
    print("Jugador 2: ")
    print("Cartas elegidas:", end=' ')
    for i in range(len(cartas_jugador_2)):
        if i != len(cartas_jugador_2) - 1:
            print(cartas_jugador_2[i], end=',')
        else:
            print(cartas_jugador_2[i])
    print("puntos sumados:", sum(cartas_jugador_2))



def matriz_vacia(filas, cols):
    m = []
    for i in range(filas):
        m.append([])
        for j in range(cols):
            m[i].append(None)
    return m    


def obtener_optimo(cartas):
    '''
    Devuelve una matriz donde, en la posicion m[i][j] indica si, para
    una instancia del problema donde el extremo izquierdo es la carta en la
    posicion i y el derecho la que esta en la posicion j (i <= j), indica True
    si conviene elegir la de la izquierda, o False si la de la derecha.
    Para los casos de 1 carta o donde sea lo mismo, elegimos izquierda por convencion.  
    En las posiciones tales que j < i, guardamos None ya que no seran tenidas en cuenta 
    '''
    n = len(cartas)
    opt = matriz_vacia(n, n)
    for i in range(n): opt[i][i] = True
    
    #Recorremos por diagonales ascendentemente, son n iteraciones. En el peor caso adentro se realizan n operaciones
    # La complejidad total de estas iteraciones es O(n^2)
    for k in range(1, n):
        i = 0
        j = k
        while j < n: #Cada recorrido diagonal finaliza cuando j llega al final
            puntaje_izq = cartas[i]
            puntaje_izq -= cartas[i+1] if opt[i+1][j] else cartas[j]
            puntaje_der = cartas[j]
            puntaje_der -= cartas[i] if opt[i][j-1] else cartas[j-1]
            if puntaje_izq >= puntaje_der: opt[i][j] = True
            else: opt[i][j] = False
            i += 1
            j += 1
    return opt



def juego(cartas):
    '''
    Recibe una lista de enteros representando los valores de las cartas.
    Devuelve una tupla de la forma (cartas_1, cartas_2) con las elecciones de cada jugador
    Siendo n el largo de la lista, la complejidad temporal es O(n^2). 
    '''
    cartas_j1 = []
    cartas_j2 = []
    opt = obtener_optimo(cartas) #O(n^2)
    n = len(cartas)
    i = 0
    j = n - 1
    turno_jugador_1 = True
    
    #Iteramos sobre el problema original sacando una carta en cada iteracion. Esto es O(n) porque tenemos memorizadas las elecciones
    while i <= j:
        if opt[i][j]: #El jugador elige la carta del extremo izquierdo
            carta_elegida = cartas[i]
            i += 1
        else:
            carta_elegida = cartas[j] #El jugador elige la carta del extremo derecho
            j -= 1
        if turno_jugador_1: cartas_j1.append(carta_elegida)
        else: cartas_j2.append(carta_elegida)    
        turno_jugador_1 = not turno_jugador_1
    return cartas_j1, cartas_j2



def main():
    if len(sys.argv) != 2:
        raise ValueError("Se debe recibir como parametro la ruta al archivo con las cartas")
    cartas = procesar_archivo(sys.argv[1])
    cartas_j1, cartas_j2 = juego(cartas)
    mostrar_resultados(cartas_j1, cartas_j2)


main()


