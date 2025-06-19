class Catalogo:
    def __init__(self):
        self.libros = []

    def agregar_libro(self, libro):
        self.libros.append(libro)

    def mostrarCatalogo(self):
        print("📘 === CATÁLOGO DE LIBROS ===")
        if not self.libros:
            print("⚠️ No hay libros en el catálogo.")
        for libro in self.libros:
            libro.mostrar_info()
            print("-" * 30)