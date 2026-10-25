from Base import BinaryTreeNode

# Variable global que cuenta las fusiones realizadas.
TOTAL_OPERACIONES_FUSION = 0


class medicamento:
    def __init__(self, id, nombre, stock, año, precio):
        # Cada objeto representa un medicamento.
        self.id = id
        self.nombre = nombre
        self.stock = stock
        self.año = año
        self.precio = precio

    def __str__(self):
        # Define cómo se muestra el medicamento al imprimirlo.
        return (
            f"ID: {self.id} | Nombre: {self.nombre} | "
            f"Stock: {self.stock} | Vence: {self.año} | "
            f"Precio: {self.precio:.2f}"
        )


class arbol:
    def __init__(self):
        self.raiz = None  # El árbol empieza vacío.
        self.alertas_stock = 0  # Cuenta medicamentos con stock menor a 5.
        self.valor_total_inventario = 0.0  # Valor económico del inventario.

    def buscar(self, id):
        actual = self.raiz  # Se comienza desde la raíz.

        while actual is not None:
            if id == actual.data.id:
                return actual.data  # Se encontró: devuelve el medicamento.
            elif id < actual.data.id:
                actual = actual.leftchild  # Busca por la izquierda.
            else:
                actual = actual.rightchild  # Busca por la derecha.

        return None  # Si llega a un nodo vacío, el ID no existe.

    def insertar(self, nodo, nuevo):
        if nodo is None:
            # Se crea un nodo cuando se encuentra una posición vacía.
            return BinaryTreeNode(nuevo)

        # Los ID menores se guardan a la izquierda.
        if nuevo.id < nodo.data.id:
            nodo.leftchild = self.insertar(nodo.leftchild, nuevo)

        # Los ID mayores se guardan a la derecha.
        elif nuevo.id > nodo.data.id:
            nodo.rightchild = self.insertar(nodo.rightchild, nuevo)

        return nodo  # Devuelve la raíz del subárbol modificado.

    def registrar(self, nuevo):
        # Evita registrar dos medicamentos con el mismo ID.
        if self.buscar(nuevo.id) is not None:
            print("El medicamento ya existe")
            return  # Termina el método sin registrar.

        # No permite valores negativos en stock ni precio.
        if nuevo.stock < 0 or nuevo.precio < 0:
            print("El stock y el precio no pueden ser negativos")
            return

        # Los medicamentos con ID par reciben un 10 % de descuento.
        if nuevo.id % 2 == 0:
            nuevo.precio *= 0.90

        # Inserta el medicamento en el árbol.
        self.raiz = self.insertar(self.raiz, nuevo)

        # Se considera alerta cuando el stock es menor a 5.
        if nuevo.stock < 5:
            self.alertas_stock += 1

        # El valor del inventario se calcula como precio por unidades.
        self.valor_total_inventario += nuevo.precio * nuevo.stock

        print("Medicamento registrado correctamente")

    def busqueda_venta(self, id, cantidad, nodo):
        # Una venta debe tener una cantidad positiva.
        if cantidad <= 0:
            return "La cantidad debe ser mayor que cero"

        # Si se llega a un nodo vacío, el ID no está en el árbol.
        if nodo is None:
            return "Medicamento no encontrado"

        # Busca recursivamente según el orden de los ID.
        if id < nodo.data.id:
            return self.busqueda_venta(id, cantidad, nodo.leftchild)

        if id > nodo.data.id:
            return self.busqueda_venta(id, cantidad, nodo.rightchild)

        # Si el stock es cero o negativo, no se puede vender.
        if nodo.data.stock <= 0:
            # Primero busca el ID inmediatamente superior.
            sustituto = self.sucesor_inorder(id)

            # Si no existe o está agotado, intenta con el anterior.
            if sustituto is None or sustituto.stock <= 0:
                sustituto = self.predecesor_inorder(id)

            # Comprueba si hay algún sustituto con stock disponible.
            if sustituto is None or sustituto.stock <= 0:
                return "Medicamento agotado. No hay sustitutos disponibles."

            return "Medicamento agotado. Sustituto sugerido:\n" + str(sustituto)

        # No permite vender más unidades de las disponibles.
        if nodo.data.stock < cantidad:
            return "Stock insuficiente"

        stock_anterior = nodo.data.stock  # Guarda el stock antes de vender.

        nodo.data.stock -= cantidad  # Descuenta las unidades vendidas.

        # Reduce el valor del inventario según el precio de esas unidades.
        self.valor_total_inventario -= nodo.data.precio * cantidad

        # Si pasa de 5 o más unidades a menos de 5, genera una alerta.
        if stock_anterior >= 5 and nodo.data.stock < 5:
            self.alertas_stock += 1

        return "Venta realizada correctamente"

    def nodo_mas_profundo(self, nodo):
        actual = nodo

        # Busca el nodo más a la izquierda del subárbol.
        # En un árbol de búsqueda, ese nodo tiene el menor ID del subárbol.
        while actual.leftchild is not None:
            actual = actual.leftchild

        return actual

    def eliminar(self, id, nodo, actualizar=True):
        if nodo is None:
            return None  # No hay nodo que eliminar.

        # Busca el ID que se quiere eliminar.
        if id < nodo.data.id:
            nodo.leftchild = self.eliminar(id, nodo.leftchild, actualizar)

        elif id > nodo.data.id:
            nodo.rightchild = self.eliminar(id, nodo.rightchild, actualizar)

        else:
            # Actualiza las estadísticas solo para el medicamento eliminado.
            # El parámetro actualizar evita descontar dos veces al reemplazar.
            if actualizar:
                if nodo.data.stock < 5:
                    self.alertas_stock -= 1

                self.valor_total_inventario -= (
                    nodo.data.precio * nodo.data.stock
                )

            # CASO 1: no tiene hijo izquierdo.
            # Se reemplaza por su hijo derecho, incluso si es None.
            if nodo.leftchild is None:
                return nodo.rightchild

            # CASO 2: no tiene hijo derecho.
            # Se reemplaza por su hijo izquierdo.
            if nodo.rightchild is None:
                return nodo.leftchild

            # CASO 3: tiene dos hijos.
            # Se busca el menor ID del subárbol derecho (sucesor).
            sucesor = self.nodo_mas_profundo(nodo.rightchild)

            # Copia los datos del sucesor al nodo que se está eliminando.
            nodo.data = sucesor.data

            # Elimina el nodo original del sucesor sin actualizar estadísticas.
            # Sus datos ya quedaron en el nodo que ocupa su lugar.
            nodo.rightchild = self.eliminar(
                sucesor.data.id, nodo.rightchild, False
            )

        return nodo  # Devuelve la raíz del subárbol actualizado.

    def eliminar_id(self, id):
        # Comprueba primero si existe el medicamento.
        if self.buscar(id) is None:
            print("Medicamento no encontrado")
            return

        self.raiz = self.eliminar(id, self.raiz)
        print("Medicamento eliminado correctamente")

    def mostrar_estado(self):
        # Muestra las dos estadísticas generales del inventario.
        print("Alertas de stock:", self.alertas_stock)
        print(
            f"Valor total del inventario: "
            f"${self.valor_total_inventario:.2f}"
        )

    def limpiar_caducados(self, año, nodo):
        if nodo is None:
            return None

        # Revisa recursivamente los dos subárboles.
        nodo.leftchild = self.limpiar_caducados(año, nodo.leftchild)
        nodo.rightchild = self.limpiar_caducados(año, nodo.rightchild)

        # Elimina medicamentos vencidos en el año indicado o antes.
        if nodo.data.año <= año:
            return self.eliminar(nodo.data.id, nodo)

        return nodo

    def reporte_caducidad(self, año):
        # Actualiza la raíz con el árbol después de la limpieza.
        self.raiz = self.limpiar_caducados(año, self.raiz)
        print("Limpieza de caducados completada")

    def visualizar_inverso(self, nodo):
        if nodo is not None:
            # Derecha, nodo y luego izquierda: ID de mayor a menor.
            self.visualizar_inverso(nodo.rightchild)
            print(nodo.data)
            self.visualizar_inverso(nodo.leftchild)

    def consultar_rango(self, minimo, maximo, nodo):
        if nodo is None or minimo > maximo:
            return

        # Solo revisa la izquierda si podría haber ID mayores al mínimo.
        if nodo.data.id > minimo:
            self.consultar_rango(minimo, maximo, nodo.leftchild)

        # Imprime el medicamento si su ID está dentro del rango.
        if minimo <= nodo.data.id <= maximo:
            print(nodo.data)

        # Solo revisa la derecha si podría haber ID menores al máximo.
        if nodo.data.id < maximo:
            self.consultar_rango(minimo, maximo, nodo.rightchild)

    def sucesor_inorder(self, id):
        actual = self.raiz
        sucesor = None

        while actual is not None:
            if actual.data.id > id:
                # Es candidato: es mayor que el ID buscado.
                sucesor = actual.data
                # Busca otro candidato más pequeño a la izquierda.
                actual = actual.leftchild
            else:
                actual = actual.rightchild

        # Devuelve el menor ID que sea mayor que el ID buscado.
        return sucesor

    def predecesor_inorder(self, id):
        actual = self.raiz
        predecesor = None

        while actual is not None:
            if actual.data.id < id:
                # Es candidato: es menor que el ID buscado.
                predecesor = actual.data
                # Busca otro candidato más grande a la derecha.
                actual = actual.rightchild
            else:
                actual = actual.leftchild

        # Devuelve el mayor ID que sea menor que el ID buscado.
        return predecesor

    def fusionar(self, id_origen, id_destino):
        global TOTAL_OPERACIONES_FUSION

        # No tiene sentido fusionar un medicamento consigo mismo.
        if id_origen == id_destino:
            print("Los IDs deben ser diferentes")
            return

        # Busca ambos medicamentos.
        origen = self.buscar(id_origen)
        destino = self.buscar(id_destino)

        if origen is None or destino is None:
            print("Uno de los medicamentos no existe")
            return

        stock_origen = origen.stock
        stock_destino = destino.stock  # Guarda el stock previo al cambio.

        # Transfiere todas las unidades del origen al destino.
        destino.stock += stock_origen

        # El stock transferido pasa a valorarse al precio del destino.
        self.valor_total_inventario += destino.precio * stock_origen

        # Si el destino pasa de menos de 5 a 5 o más, deja de estar en alerta.
        if stock_destino < 5 and destino.stock >= 5:
            self.alertas_stock -= 1

        # Elimina el medicamento de origen.
        # Esto descuenta su valor anterior y su alerta si corresponde.
        self.raiz = self.eliminar(id_origen, self.raiz)

        # Registra una fusión completada.
        TOTAL_OPERACIONES_FUSION += 1

        print("Fusión realizada correctamente")
        print("Total de fusiones:", TOTAL_OPERACIONES_FUSION)
