import csv
import sys
from pedidos import Pedido


# El archivo lo asumimos con formato CSV, cada linea es "nombre,fecha_inicio,fecha_fin"
def procesar_archivo(ruta_archivo):
    pedidos = []
    with open(ruta_archivo, "r") as archivo:
        csvreader = csv.reader(archivo)
        for entrada in csvreader:
            if len(entrada) == 3:
                p = Pedido(entrada[0], entrada[1], entrada[2])
                pedidos.append(p)
    return pedidos


# Asumimos que viene ordenado por fecha de finalizacion. Esto es O(n)
def interval_scheduling(pedidos):
    if len(pedidos) <= 0: return None
    solucion = [pedidos[0]]
    ultima_finalizacion = pedidos[0].fin
    for i in range(1, len(pedidos)):
        if pedidos[i].inicio >= ultima_finalizacion:
            solucion.append(pedidos[i])
            ultima_finalizacion = pedidos[i].fin
    return solucion


# O(n)
# Arma un interval scheduling donde ninguno se superponga con un_pedido
def armado_desde_pedido(pedidos, un_pedido):
    if len(pedidos) <= 0: return None
    nuevo_pedidos = []
    # Elimino los pedidos que se superponen a un_pedido
    for i in range(len(pedidos)):
        if not pedidos[i].se_superpone_con(un_pedido) or pedidos[i].nombre is un_pedido.nombre:
            nuevo_pedidos.append(pedidos[i])
    s = interval_scheduling(nuevo_pedidos)

    return s


# pedidos ya esta ordenado, entonces es O(n). Filtra los entre_semana y hace interval scheduling
def interval_scheduling_sin_entre_semana(pedidos):
    pedidos_sin_entre_semana = []
    for p in pedidos:
        if not p.es_circular(): pedidos_sin_entre_semana.append(p)
    return interval_scheduling(pedidos_sin_entre_semana)


# O(n^2) + O(nlog(n)) = O(n^2)
def interval_scheduling_circular(pedidos):
    if len(pedidos) <= 0: return

    # sorted es O(n.log(n))
    pedidos_ordenado = sorted(pedidos, key=lambda pedido: pedido.fin)

    pedidos_entre_semana = []
    # O(n)
    for p in pedidos:
        if p.es_circular():
            pedidos_entre_semana.append(p)

    solucion_actual = interval_scheduling_sin_entre_semana(pedidos_ordenado)  # O(n)

    # Hace n iteraciones en el peor caso. Adentro hace operaciones O(n), entonces en total es O(n^2)
    for p in pedidos_entre_semana:
        solucion = armado_desde_pedido(pedidos_ordenado, p)  # O(n)
        if len(solucion) > len(solucion_actual):
            solucion_actual = solucion

    return solucion_actual


def main():
    pedidos = procesar_archivo(sys.argv[1])  # Llega el path como parametro en terminal

    pedidos = interval_scheduling_circular(pedidos)
    if pedidos is not None:
        for p in pedidos:
            print("Nombre: " + p.nombre + ", Inicio: " + str(p.inicio) + ", Fin: " + str(p.fin))


main()
