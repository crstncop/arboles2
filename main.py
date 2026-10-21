from Base import BinaryTreeNode

class medicamento:
    def __init__(self, id, nombre, stock, año, precio):
        self.id: int = id
        self.nombre: str = nombre
        self.stock: int = stock
        self.año: int = año
        self.precio: int = precio

class arbol:
    def __init__(self):
        self.arbol = BinaryTreeNode()
        
        
        
        
        