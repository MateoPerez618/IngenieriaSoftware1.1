from Libro import Libro
class Catalogo:
    def __init__(self):
        self.libros = []

    def agregarLibro(self, libro):
        self.libros.append(libro)

    def mostrarCatalogo(self):
        print("📘 === CATÁLOGO DE LIBROS ===")
        if not self.libros:
            print("⚠️ No hay libros en el catálogo.")
        for libro in self.libros:
            libro.infoLibro()
            print("-" * 30)
    
    def filtrarCategoria(self, categoria):
        print("Libros de: " +categoria)
        if not self.libros:
            print("⚠️ No hay libros en el catálogo.")

        encontrados= False    
        for libro in self.libros:
            if libro.categoria.lower()==categoria.lower():
                libro.infoLibro()
                print("-" * 30)
                encontrados= True

        if not encontrados:
            print("⚠️ No hay libros en esa categoría.")        

