# cada pedido va entre la hora 0 (lunes primera hora) hasta la 168 (domingo ultima hora)
# un pedido puede ser 'ciruclar', empezar del otro lado (ej: inicio 157, fin 14)
# Suponemos que los pedidos duran como mucho 168 horas
class Pedido:

    def __init__(self, nombre, inicio, fin):
        self.nombre = nombre
        self.inicio = int(inicio)
        self.fin = int(fin)

    def es_circular(self):
        return self.inicio > self.fin

    def se_superpone_con(self, otro_pedido):
        if self.es_circular():
            return self.fin < otro_pedido.inicio and self.inicio > otro_pedido.fin
        elif otro_pedido.es_circular():
            return otro_pedido.se_superpone_con(self)
        elif self.fin < otro_pedido.inicio or self.inicio > otro_pedido.fin: return False
        return True
