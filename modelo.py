
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
        self.alertas_stock=0
        self.valor_total_inventario = 0.0

    def insertar(self, nodo, nuevo):
        if nodo is None:
            if nuevo.id % 2 == 0:
                nuevo.precio *= 0.90
            if nuevo.stock < 5:
                self.alertas_stock += 1
            self.valor_total_inventario += nuevo.precio * nuevo.stock
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
            return "Medicamento agotado"

        if nodo.data.stock < cantidad:
            return "Stock insuficiente"

        nodo.data.stock -= cantidad
        return "Venta realizada correctamente"
    
    def nodo_mas_profundo(self,nodo):
        current = nodo
        while current.leftchild is not None:
            current = current.leftchild
        return current
    
    def eliminar(self, id, nodo):
        if nodo is None:
            return None

        if id < nodo.data.id:
            nodo.leftchild = self.eliminar(id, nodo.leftchild)

        elif id > nodo.data.id:
            nodo.rightchild = self.eliminar(id, nodo.rightchild)

        else:
            if nodo.data.stock < 5:
                self.alertas_stock -= 1
            self.valor_total_inventario -= nodo.data.precio * nodo.data.stock
            
            if nodo.leftchild is None and nodo.rightchild is None:
                return None

            if nodo.leftchild is None:
                temp = nodo.rightchild
                nodo = None
                return temp
            elif nodo.rightchild is None:
                temp = nodo.leftchild
                nodo = None
                return temp

            else:
                if nodo.data.stock < 5:
                    self.alertas_stock += 1
                self.valor_total_inventario += (nodo.data.precio * nodo.data.stock)
                
                actual = self.nodo_mas_profundo(nodo.rightchild)
                nodo.data=actual.data
                nodo.rightchild = self.eliminar(actual.data.id, nodo.rightchild)

        return nodo

    def mostrar_estado(self):
        print(f"Alertas de stock:{self.alertas_stock}")
        print(f"Valor total del inventario:${self.valor_total_inventario:.2f}")

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



