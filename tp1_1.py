import csv

#cada pedido va entre la hora 0 (lunes primera hora) hasta la 168 (domingo ultima hora)
#un pedido puede ser 'ciruclar', empezar del otro lado (ej: inicio 157, fin 14)
#Suponemos que los pedidos duran como mucho 168 horas
class Pedido:

    def __init__(self, nombre, inicio, fin):
        self.nombre = nombre
        self.inicio = inicio
        self.fin = fin

    def es_circular(self):
        return self.inicio > self.final

    def se_superpone_con(self, otro_pedido):
        pass #Falta implementar


#El archivo lo asumimos con formato CSV, cada linea es "nombre,fecha_inicio,fecha_fin"
def procesar_archivo(ruta_archivo):
    SEPARADOR = ','
    pedidos = []
    with open(ruta_archivo, "r") as archivo:
        csvreader = csv.reader(archivo, delimiter=SEPARADOR)
        for entrada in csvreader:
            p = Pedido(entrada[0], entrada[1], entrada[2])
            pedidos.append(p)
    return pedidos


def interval_scheduling(pedidos):
    if len(pedidos) <= 0: return None
    pedidos = sorted(pedidos, key = lambda pedido: pedido.fin)
    s = []
    s.append(pedidos[0])
    ultima_finalizacion = pedidos[0].fin
    for i in range(1, len(pedidos)):
        if pedidos[i].inicio >= ultima_finalizacion:
            s.append(pedidos[i])
            ultima_finalizacion = pedidios[i].fin
    return s

def armado_desde_pedido(pedidos, un_pedido):
    if len(pedidos) <= 0: return None
    
    nuevo_pedidos = []
    #Elimino los pedidos que se superponen a un_pedido
    for i in range(len(pedidos)):
        if not pedidos[i].se_superpone_con(un_pedido):
            nuevo_pedidos.append(nuevo_pedidos)
    s = interval_scheduling(nuevo_pedidos)
    s.append(un_pedido)
    return s


def arreglo_mas_largo(arreglos):
    if len(arreglos) == 0: return None
    pos_max = 0
    for i in range(1, len(arreglos)):
        if len(arreglos[i]) > len(arreglos[pos_max]):
            pos_max = i
    return arreglos[i]



def interval_scheduling_circular(pedidos):
    if len(pedidos) <= 0: return None

    #O(n.log(n))
    pedidos_totales = sorted(pedidos, key = lambda pedido: pedido.fin)
    
    compentencia_pedidos = []
    
    #Todo esto es O(n ^ 2), se repite n veces una operacion O(n)
    for i in range(len(pedidos_totales)): #Me armo un arreglo con tantas posiciones como pedidos, en cada uno guardo otro arreglo
        compentencia_pedidos.append(armado_desde_pedido(pedidos, pedidos_totales[i])) #O(n)

    #Elijo el arreglo mas largo, lo devuelvo en O(n)
    return arreglo_mas_largo(compentencia_pedidos)


pedidos = procesar_archivo("prueba_entrada.csv")

for p in pedidos:
    print("Nombre: " + p.nombre + ", Inicio: " + str(p.inicio) + ", Fin: " + str(p.fin))


