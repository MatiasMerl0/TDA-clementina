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
        if self.fin < otro_pedido.inicio or self.inicio > otro_pedido.fin: return False
        return True



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


#Asumimos que viene ordenado, es O(n)
def interval_scheduling(pedidos):
    if len(pedidos) <= 0: return None
    #pedidos = sorted(pedidos, key = lambda pedido: pedido.fin)
    s = []
    s.append(pedidos[0])
    ultima_finalizacion = pedidos[0].fin
    for i in range(1, len(pedidos)):
        if pedidos[i].inicio >= ultima_finalizacion:
            s.append(pedidos[i])
            ultima_finalizacion = pedidios[i].fin
    return s

#O(n)
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


#pedidos ya esta ordenado, entonces es O(n)
def interval_scheduling_sin_entre_semana(pedidos):
    nuevo_pedidos = []
    for p in pedidos:
        if not p.es_circular(): nuevo_pedidos.append(p)
    return interval_scheduling(pedidos)

# O(n^2) + O(nlog(n)) = O(n^2)
def interval_scheduling_circular(pedidos):
    if len(pedidos) <= 0: return None

    #sorted es O(n.log(n))
    pedidos_ordenado = sorted(pedidos, key = lambda pedido: pedido.fin)
    
    pedidos_entre_semana = []
    #O(n)
    for p in pedidos:
        if p.es_circular():
            pedidos_entre_semana.append(p) 
    
    solucion_actual = interval_scheduling_sin_entre_semana(pedidos_ordenado) #O(n)
    #Hace n iteraciones en el peor caso. Adentro hace operaciones O(n), entonces en total es O(n^2)
    for p in pedidos_entre_semana:
        s = armado_desde_pedido(pedidos_totales, p) #O(n)
        if len(s) > len(solucion_actual):
            solucion_actual = s

    return solucion_actual


pedidos = procesar_archivo("prueba_entrada.csv")

for p in pedidos:
    print("Nombre: " + p.nombre + ", Inicio: " + str(p.inicio) + ", Fin: " + str(p.fin))




