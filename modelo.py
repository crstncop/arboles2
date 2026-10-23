
from Base import BinaryTreeNode

TOTAL_OPERACIONES_FUSION = 0


class medicamento:
    def __init__(self, id, nombre, stock, año, precio):
        self.id: int = id
        self.nombre: str = nombre
        self.stock: int = stock
        self.año: int = año
        self.precio: float = precio

    def __str__(self):
        return (
            f"ID: {self.id} | Nombre: {self.nombre} | "
            f"Stock: {self.stock} | Vence: {self.año} | "
            f"Precio: {self.precio:.2f}"
        )


class arbol:
    def __init__(self):
        self.raiz = None

    def insertar(self, nodo, nuevo):
        if nodo is None:
            if nuevo.id % 2 == 0:
                nuevo.precio *= 0.90
            return BinaryTreeNode(nuevo)

        if nuevo.id < nodo.data.id:
            nodo.leftchild = self.insertar(nodo.leftchild, nuevo)
        elif nuevo.id > nodo.data.id:
            nodo.rightchild = self.insertar(nodo.rightchild, nuevo)
        else:
            print("El medicamento ya existe")

        return nodo

    def registrar(self, nuevo):
        self.raiz = self.insertar(self.raiz, nuevo)

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

    def busqueda_venta(self, id, cantidad, nodo):
        if nodo is None:
            return "No encontrado"

        if id < nodo.data.id:
            return self.busqueda_venta(id, cantidad, nodo.leftchild)

        if id > nodo.data.id:
            return self.busqueda_venta(id, cantidad, nodo.rightchild)

        if cantidad <= 0:
            return "La cantidad debe ser mayor que cero"

        if nodo.data.stock == 0:
            self.sugerir_sustituto(id)
            return "Medicamento agotado"

        if nodo.data.stock < cantidad:
            return "Stock insuficiente"

        nodo.data.stock -= cantidad
        return "Venta realizada correctamente"

    def eliminar(self, id, nodo):
        if nodo is None:
            return None

        if id < nodo.data.id:
            nodo.leftchild = self.eliminar(id, nodo.leftchild)

        elif id > nodo.data.id:
            nodo.rightchild = self.eliminar(id, nodo.rightchild)

        else:
            if nodo.leftchild is None and nodo.rightchild is None:
                return None

            elif nodo.leftchild is None:
                return nodo.rightchild

            elif nodo.rightchild is None:
                return nodo.leftchild

            else:
                actual = nodo.rightchild

                while actual.leftchild is not None:
                    actual = actual.leftchild

                nodo.data = actual.data
                nodo.rightchild = self.eliminar(actual.data.id, nodo.rightchild)

    return nodo


        return nodo

    def eliminar_id(self, id):
        if self.buscar(id) is None:
            print("Medicamento no encontrado")
            return

        self.raiz = self.eliminar(id, self.raiz)
        print("Medicamento eliminado correctamente")

    def contar_alertas_stock(self, nodo):
        if nodo is None:
            return 0

        alerta = 1 if nodo.data.stock < 5 else 0

        return (
            alerta
            + self.contar_alertas_stock(nodo.leftchild)
            + self.contar_alertas_stock(nodo.rightchild)
        )

    def calcular_valor_inventario(self, nodo):
        if nodo is None:
            return 0

        valor = nodo.data.precio * nodo.data.stock

        return (
            valor
            + self.calcular_valor_inventario(nodo.leftchild)
            + self.calcular_valor_inventario(nodo.rightchild)
        )

    def mostrar_estado(self):
        print("Alertas de stock:", self.contar_alertas_stock(self.raiz))
        print(
            "Valor total del inventario:",
            f"${self.calcular_valor_inventario(self.raiz):.2f}"
        )

    def limpiar_caducados(self, año, nodo):
        if nodo is None:
            return None

        nodo.leftchild = self.limpiar_caducados(
            año, nodo.leftchild
        )
        nodo.rightchild = self.limpiar_caducados(
            año, nodo.rightchild
        )

        if nodo.data.año <= año:
            return self.eliminar(nodo.data.id, nodo)

        return nodo

    def reporte_caducidad(self, año):
        self.raiz = self.limpiar_caducados(año, self.raiz)

    def visualizar_inverso(self, nodo):
        if nodo is not None:
            self.visualizar_inverso(nodo.rightchild)
            print(nodo.data)
            self.visualizar_inverso(nodo.leftchild)

    def consultar_rango(self, minimo, maximo, nodo):
        if nodo is None:
            return

        if minimo > maximo:
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
            if id < actual.data.id:
                sucesor = actual.data
                actual = actual.leftchild
            else:
                actual = actual.rightchild

        return sucesor

    def predecesor_inorder(self, id):
        actual = self.raiz
        predecesor = None

        while actual is not None:
            if id > actual.data.id:
                predecesor = actual.data
                actual = actual.rightchild
            else:
                actual = actual.leftchild

        return predecesor

    def sugerir_sustituto(self, id):
        producto = self.buscar(id)

        if producto is None:
            print("Medicamento no encontrado")
            return

        if producto.stock > 0:
            print("El medicamento tiene stock disponible")
            return

        sustituto = self.sucesor_inorder(id)

        if sustituto is None:
            sustituto = self.predecesor_inorder(id)

        if sustituto is None:
            print("No hay medicamentos sustitutos")
        else:
            print("Medicamento sugerido:")
            print(sustituto)

    def fusionar(self, id_origen, id_destino):
        global TOTAL_OPERACIONES_FUSION

        origen = self.buscar(id_origen)
        destino = self.buscar(id_destino)

        if id_origen == id_destino:
            print("Los IDs deben ser diferentes")
            return

        if origen is None or destino is None:
            print("Uno de los medicamentos no existe")
            return

        destino.stock += origen.stock
        self.raiz = self.eliminar(id_origen, self.raiz)

        TOTAL_OPERACIONES_FUSION += 1

        print("Fusión realizada correctamente")



