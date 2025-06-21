class Libro:
    
    def __init__(self, nombre, categoria, existencias):
        self.nombre = nombre
        self.categoria = categoria
        self.existencias = existencias

    def mostrarCatalogo(self):
        print(f"Nombre del libro: {self.nombre}")
        print(f"Categoría: {self.categoria}")
        print(f"Existencias: {self.existencias}")

    def disponible(self):
        return self.existencias > 0
    
    def prestar(self):
        if self.disponible():
            self.existencias -= 1