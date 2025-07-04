from Libro import Libro
class Catalogo:
    def __init__(self):
        self.libros = []
    #Este metodo sirve para agregar los libros al catalogo
    def agregarLibro(self, libro):
        self.libros.append(libro)
    #Este metodo muestra el catalogo de libros en la biblioteca
    def mostrarCatalogo(self):
        print("📘 === CATÁLOGO DE LIBROS ===")
        #Verificamos que hayan libros en el catalogo
        if not self.libros:
            print("⚠️ No hay libros en el catálogo.")
        #Mostramos libro por libro    
        for libro in self.libros:
            libro.infoLibro()
            print("-" * 30)

    def mostrarLibrosCalificacion(self):
        print("📘 === CATÁLOGO DE LIBROS ===")
        #Verificamos que hayan libros en el catalogo
        if not self.libros:
            print("⚠️ No hay libros en el catálogo.")
        #Mostramos libro por libro    
        for libro in self.libros:
            libro.nombreLibro()
            print("-" * 30)

    #Este metodo sirve para filtrar el catalogo por categoria
    def filtrarCategoria(self, categoria):
        print("Libros de: " +categoria)
        #Primero verificamos que hayan libros en el catalogo
        if not self.libros:
            print("⚠️ No hay libros en el catálogo.")

        encontrados= False    
        for libro in self.libros:
            #Verificamos que libros comparten la categoria que el usuario deseo
            if libro.categoria.lower()==categoria.lower():
                libro.infoLibro()
                #Mostramos los libros filtrados
                print("-" * 30)
                encontrados= True
        #Si no encuentra libros de esa categoria muestra un mensaje de advertencia
        if not encontrados:
            print("⚠️ No hay libros en esa categoría.")  

    #Este metodo sirve para filtrar el catalogo por titulo o autor
    def filtrarBusquedaPersonalizada(self, busqueda):

        #Primero verificamos que hayan libros en el catalogo
        if not self.libros:
            print("⚠️ No hay libros en el catálogo.")
        
        encontrados= False    
        for libro in self.libros:
            #Buscamos en el catalogo que libros comparten la busqueda que quiere el usuario
            if busqueda == libro.nombre.lower() or busqueda == libro.autor.lower():
                libro.infoLibro()
                #Mostramos los libros
                print("-" * 30)
                encontrados= True

        #Si no encuentra libros de esa categoria muestra un mensaje de advertencia
        if not encontrados:
            print("⚠️ No hay libros con ese autor o nombre")                

# Método para calificar un libro por su nombre
    def calificarLibro(self, nombreLibro, calificacion, reseña=None):
        for libro in self.libros:
            if libro.nombre.lower() == nombreLibro.lower():
                libro.agregarCalificacion(calificacion, reseña)
                print("✅ Calificación agregada con éxito.")
                return
        print("⚠️ No se encontró un libro con ese nombre.")

    # Método para ver las reseñas de un libro específico
    def verReseñasLibro(self, nombreLibro):
        for libro in self.libros:
            if libro.nombre.lower() == nombreLibro.lower():
                libro.mostrarReseñas()
                return
        print("⚠️ No se encontró un libro con ese nombre.")

    # Método para mostrar calificaciones promedio de todos los libros
    def mostrarCalificacionesPromedio(self):
        print("📊 Calificaciones promedio de los libros:")
        for libro in self.libros:
            print(f"📖 {libro.nombre}: ", end="")
            if libro.calificaciones:
                promedio = sum(libro.calificaciones) / len(libro.calificaciones)
                print(f"{promedio:.2f} ⭐ ({len(libro.calificaciones)} opiniones)")
            else:
                print("Sin calificaciones")