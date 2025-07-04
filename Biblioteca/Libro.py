class Libro:
    
    def __init__(self, nombre, categoria, autor, calificacion,  existencias):
        self.nombre = nombre
        self.categoria = categoria
        self.autor = autor
        self.calificacion = calificacion
        self.existencias = existencias
    #Este metodo muestra toda la informacion del libro
    def infoLibro(self):
        print(f"Nombre del libro: {self.nombre}")
        print(f"Categoría: {self.categoria}")
        print(f"Autor: {self.autor}")
        print(f"Calificacion: {self.calificacion}")
        print(f"Existencias: {self.existencias}")

    def disponible(self):
        return self.existencias > 0
    
    def prestar(self):
        if self.disponible():
            self.existencias -= 1