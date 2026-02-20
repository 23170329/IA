class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.izquierdo = None
        self.derecho = None


class Arbol:
    def __init__(self):
        self.raiz = None

    def vacio(self):
        return self.raiz is None

    # MÉTODO INSERTAR
    def insertar(self, nombre):
        if self.raiz is None:
            self.raiz = Nodo(nombre)
        else:
            self._insertar_recursivo(self.raiz, nombre)

    def _insertar_recursivo(self, actual, nombre):
        if nombre < actual.nombre:
            if actual.izquierdo is None:
                actual.izquierdo = Nodo(nombre)
            else:
                self._insertar_recursivo(actual.izquierdo, nombre)
        else:
            if actual.derecho is None:
                actual.derecho = Nodo(nombre)
            else:
                self._insertar_recursivo(actual.derecho, nombre)

    # MÉTODO IMPRIMIR ARBOL
    def imprimir_arbol(self):
        print("Contenido del árbol (Orden Alfabético):")
        self._imprimir_inorder(self.raiz)
        print()

    def _imprimir_inorder(self, actual):
        if actual:
            self._imprimir_inorder(actual.izquierdo)
            print(f"- {actual.nombre}", end=" ")
            self._imprimir_inorder(actual.derecho)

    # MÉTODO DE BúSQUEDA
    def buscar_nodo(self, nombre):
        return self._buscar_recursivo(self.raiz, nombre)

    def _buscar_recursivo(self, actual, nombre):
        if actual is None or actual.nombre == nombre:
            return actual
        if nombre < actual.nombre:
            return self._buscar_recursivo(actual.izquierdo, nombre)
        return self._buscar_recursivo(actual.derecho, nombre)


if __name__ == "__main__":
    pass
