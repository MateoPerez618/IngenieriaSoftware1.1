
    
class Libro:
    def __init__(self, nombre, categoria, autor, cantidad):
        self.nombre = nombre
        self.autor = autor
        self.categoria = categoria
        self.cantidad = cantidad
        self.calificaciones = []   # Lista de números (1 a 5)
        self.reseñas = []          # Lista de strings

    def infoLibro(self):
        print(f"📖 Nombre: {self.nombre}")
        print(f"✍️ Autor: {self.autor}")
        print(f"📚 Categoría: {self.categoria}")
        print(f"📦 Disponibles: {self.cantidad}")
        if self.calificaciones:
            promedio = sum(self.calificaciones) / len(self.calificaciones)
            print(f"⭐ Calificación promedio: {promedio:.2f} ({len(self.calificaciones)} opiniones)")
        else:
            print("⭐ Aún sin calificaciones")


    def agregarCalificacion(self, calificacion, reseña=None):
        if 1 <= calificacion <= 5:
            self.calificaciones.append(calificacion)
            if reseña:
                self.reseñas.append(reseña)
        else:
            print("⚠️ Calificación inválida. Debe estar entre 1 y 5.")

    def mostrarReseñas(self):
        print(f"📝 Reseñas para '{self.nombre}':")
        if not self.reseñas:
            print("⚠️ No hay reseñas para este libro.")
        else:
            for i, res in enumerate(self.reseñas, 1):
                print(f"{i}. {res}")

    def nombreLibro(self):
        print(f"Nombre del libro: {self.nombre}")

    def disponible(self):
        return self.existencias > 0
    
    def prestar(self):
        if self.disponible():
            self.existencias -= 1