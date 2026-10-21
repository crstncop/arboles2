class BinaryTreeNode:

  def __init__(self, data):
    self.data = data
    self.leftchild = None
    self.rightchild = None


  def __str__(self, level=0):
    ret = "  " *level + str(self.data) + "\n"
    if self.leftchild:
       ret += self.leftchild.__str__(level+1)
    if self.rightchild:
       ret += self.rightchild.__str__(level+1)
    return ret


def printTree(Node, prefix="", is_left=True):
    if not Node:
        return

    if Node.rightchild:
        printTree(Node.rightchild, prefix + ("│    " if is_left else "    "), False)

    print(prefix + ("└── " if is_left else "┌── ") + str(Node.data))

    if Node.leftchild:
        printTree(Node.leftchild, prefix + ("     " if is_left else "│   "), True)


    def Pre_Order(root):

        if root is None:
            return

        print(root.data) #Procesar/Recorro/Visito el nodo actual
        Pre_Order(root.leftchild)
        Pre_Order(root.rightchild)

    def Post_Order(root):

        if root is None:
            return

        Post_Order(root.leftchild)
        Post_Order(root.rightchild)
        print(root.data) #Procesar/Recorro/Visito el nodo actual

    def In_Order(root):

        if root is None:
            return

        In_Order(root.leftchild)
        print(root.data) #Procesar/Recorro/Visito el nodo actual
        In_Order(root.rightchild)