
from Base import BinaryTreeNode

TOTAL_OPERACIONES_FUSION = 0


class medicamento:
    def __init__(self, id, nombre, stock, año, precio):
        self.id = id
        self.nombre = nombre
        self.stock = stock
        self.año = año
        self.precio = precio

    def __str__(self):
        return (
            f"ID: {self.id} | Nombre: {self.nombre} | "
            f"Stock: {self.stock} | Vence: {self.año} | "
            f"Precio: {self.precio:.2f}"
        )


class arbol:
    def __init__(self):
        self.raiz = None
        self.alertas_stock = 0
        self.valor_total_inventario = 0.0

    def buscar(self, id):
        actual = self.raiz

        while actual is not None:
            if id == actual.data.id:
                return actual.data
            elif id < actual.data.id:
                actual = actual.leftchild
            else:
                actual = actual.rightchild

        return None

    def insertar(self, nodo, nuevo):
        if nodo is None:
            return BinaryTreeNode(nuevo)

        if nuevo.id < nodo.data.id:
            nodo.leftchild = self.insertar(nodo.leftchild, nuevo)
        elif nuevo.id > nodo.data.id:
            nodo.rightchild = self.insertar(nodo.rightchild, nuevo)

        return nodo

    def registrar(self, nuevo):
        if self.buscar(nuevo.id) is not None:
            print("El medicamento ya existe")
            return

        if nuevo.stock < 0 or nuevo.precio < 0:
            print("El stock y el precio no pueden ser negativos")
            return

        if nuevo.id % 2 == 0:
            nuevo.precio *= 0.90

        self.raiz = self.insertar(self.raiz, nuevo)

        if nuevo.stock < 5:
            self.alertas_stock += 1

        self.valor_total_inventario += nuevo.precio * nuevo.stock

        print("Medicamento registrado correctamente")

    def busqueda_venta(self, id, cantidad, nodo):
        if cantidad <= 0:
            return "La cantidad debe ser mayor que cero"

        if nodo is None:
            return "Medicamento no encontrado"

        if id < nodo.data.id:
            return self.busqueda_venta(id, cantidad, nodo.leftchild)

        if id > nodo.data.id:
            return self.busqueda_venta(id, cantidad, nodo.rightchild)

        if nodo.data.stock <= 0:
            sustituto = self.sucesor_inorder(id)

            if sustituto is None or sustituto.stock <= 0:
                sustituto = self.predecesor_inorder(id)

            if sustituto is None or sustituto.stock <= 0:
                return "Medicamento agotado. No hay sustitutos disponibles."

            return "Medicamento agotado. Sustituto sugerido:\n" + str(sustituto)

        if nodo.data.stock < cantidad:
            return "Stock insuficiente"

        stock_anterior = nodo.data.stock

        nodo.data.stock -= cantidad
        self.valor_total_inventario -= nodo.data.precio * cantidad

        if stock_anterior >= 5 and nodo.data.stock < 5:
            self.alertas_stock += 1

        return "Venta realizada correctamente"

    def nodo_mas_profundo(self, nodo):
        actual = nodo

        while actual.leftchild is not None:
            actual = actual.leftchild

        return actual

    def eliminar(self, id, nodo, actualizar=True):
        if nodo is None:
            return None

        if id < nodo.data.id:
            nodo.leftchild = self.eliminar(id, nodo.leftchild, actualizar)

        elif id > nodo.data.id:
            nodo.rightchild = self.eliminar(id, nodo.rightchild, actualizar)

        else:
            if actualizar:
                if nodo.data.stock < 5:
                    self.alertas_stock -= 1

                self.valor_total_inventario -= (nodo.data.precio * nodo.data.stock)

            if nodo.leftchild is None:
                return nodo.rightchild

            if nodo.rightchild is None:
                return nodo.leftchild

            sucesor = self.nodo_mas_profundo(nodo.rightchild)
            nodo.data = sucesor.data

            nodo.rightchild = self.eliminar(sucesor.data.id, nodo.rightchild, False)

        return nodo

    def eliminar_id(self, id):
        if self.buscar(id) is None:
            print("Medicamento no encontrado")
            return

        self.raiz = self.eliminar(id, self.raiz)
        print("Medicamento eliminado correctamente")

    def mostrar_estado(self):
        print("Alertas de stock:", self.alertas_stock)
        print(
            f"Valor total del inventario: "
            f"${self.valor_total_inventario:.2f}"
        )

    def limpiar_caducados(self, año, nodo):
        if nodo is None:
            return None

        nodo.leftchild = self.limpiar_caducados(año, nodo.leftchild)
        nodo.rightchild = self.limpiar_caducados(año, nodo.rightchild)

        if nodo.data.año <= año:
            return self.eliminar(nodo.data.id, nodo)

        return nodo

    def reporte_caducidad(self, año):
        self.raiz = self.limpiar_caducados(año, self.raiz)
        print("Limpieza de caducados completada")

    def visualizar_inverso(self, nodo):
        if nodo is not None:
            self.visualizar_inverso(nodo.rightchild)
            print(nodo.data)
            self.visualizar_inverso(nodo.leftchild)

    def consultar_rango(self, minimo, maximo, nodo):
        if nodo is None or minimo > maximo:
            return

        if nodo.data.id > minimo:
            self.consultar_rango(minimo, maximo, nodo.leftchild)

        if minimo <= nodo.data.id <= maximo:
            print(nodo.data)

        if nodo.data.id < maximo:
            self.consultar_rango(minimo, maximo, nodo.rightchild)

    def sucesor_inorder(self, id):
        actual = self.raiz
        sucesor = None

        while actual is not None:
            if actual.data.id > id:
                sucesor = actual.data
                actual = actual.leftchild
            else:
                actual = actual.rightchild

        return sucesor

    def predecesor_inorder(self, id):
        actual = self.raiz
        predecesor = None

        while actual is not None:
            if actual.data.id < id:
                predecesor = actual.data
                actual = actual.rightchild
            else:
                actual = actual.leftchild

        return predecesor

    def fusionar(self, id_origen, id_destino):
        global TOTAL_OPERACIONES_FUSION

        if id_origen == id_destino:
            print("Los IDs deben ser diferentes")
            return

        origen = self.buscar(id_origen)
        destino = self.buscar(id_destino)

        if origen is None or destino is None:
            print("Uno de los medicamentos no existe")
            return

        stock_origen = origen.stock
        stock_destino = destino.stock

        # El stock se transfiere al medicamento de destino.
        destino.stock += stock_origen

        # Se actualiza el valor según el precio del destino.
        self.valor_total_inventario += (destino.precio * stock_origen)

        # Si el destino deja de estar en alerta, se descuenta.
        if stock_destino < 5 and destino.stock >= 5:
            self.alertas_stock -= 1

        # Eliminar el origen descuenta su valor y su alerta,
        # cuando corresponda.
        self.raiz = self.eliminar(id_origen, self.raiz)

        TOTAL_OPERACIONES_FUSION += 1

        print("Fusión realizada correctamente")
        print("Total de fusiones:", TOTAL_OPERACIONES_FUSION)



