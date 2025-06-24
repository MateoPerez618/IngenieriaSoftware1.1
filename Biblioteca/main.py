# main.py
from autenticacion import mostrar_menu_autenticacion    
from Catalogo import Catalogo
from Libro import Libro
from Prestamo import PrestamoDB 
from disponibilidad import GestorDisponibilidad


#Crear instancias para libros
catalogo = Catalogo()
# Cargar libros de ejemplo los cambiamos luego
catalogo.agregarLibro(Libro("Cien años de soledad", "Novela","Gabriel Garcia Marquez" ,3))
catalogo.agregarLibro(Libro("El Principito","Fantasia","Antoine de Saint-Exupéry" ,2))
catalogo.agregarLibro(Libro("Álgebra de Baldor", "Matematicas","Aurelio Baldor" ,1))
catalogo.agregarLibro(Libro("1984", "Novela", "George Orwell", 4))
catalogo.agregarLibro(Libro("El Hobbit", "Fantasia", "J.R.R. Tolkien", 5))
catalogo.agregarLibro(Libro("Breve historia del tiempo", "Ciencia", "Stephen Hawking", 2))
catalogo.agregarLibro(Libro("La Odisea", "Clasico", "Homero", 3))
catalogo.agregarLibro(Libro("Orgullo y prejuicio", "Romance", "Jane Austen", 4))
catalogo.agregarLibro(Libro("Crónica de una muerte anunciada", "Novela", "Gabriel Garcia Marquez", 3))
catalogo.agregarLibro(Libro("Harry Potter y la piedra filosofal", "Fantasia", "J.K. Rowling", 6))
catalogo.agregarLibro(Libro("Los juegos del hambre", "Fantasia", "Suzanne Collins", 4))
catalogo.agregarLibro(Libro("El código Da Vinci", "Suspenso", "Dan Brown", 5))
catalogo.agregarLibro(Libro("El alquimista", "Autoayuda", "Paulo Coelho", 7))
catalogo.agregarLibro(Libro("Padre rico, padre pobre", "Finanzas", "Robert Kiyosaki", 6))
catalogo.agregarLibro(Libro("Sapiens", "Historia", "Yuval Noah Harari", 3))
catalogo.agregarLibro(Libro("El nombre del viento", "Fantasia", "Patrick Rothfuss", 4))
catalogo.agregarLibro(Libro("Cumbres borrascosas", "Romance", "Emily Brontë", 2))
catalogo.agregarLibro(Libro("La divina comedia", "Poesia", "Dante Alighieri", 2))
catalogo.agregarLibro(Libro("Rayuela", "Novela", "Julio Cortázar", 3))
catalogo.agregarLibro(Libro("Fahrenheit 451", "Ciencia ficcion", "Ray Bradbury", 3))
catalogo.agregarLibro(Libro("Ensayo sobre la ceguera", "Novela", "José Saramago", 2))
catalogo.agregarLibro(Libro("El arte de la guerra", "Filosofia", "Sun Tzu", 4))
catalogo.agregarLibro(Libro("Meditaciones", "Filosofia", "Marco Aurelio", 2))
catalogo.agregarLibro(Libro("Don Quijote de la Mancha", "Clasico", "Miguel de Cervantes", 4))
catalogo.agregarLibro(Libro("El señor de los anillos", "Fantasia", "J.R.R. Tolkien", 5))
catalogo.agregarLibro(Libro("Drácula", "Terror", "Bram Stoker", 3))
catalogo.agregarLibro(Libro("Frankenstein", "Terror", "Mary Shelley", 3))
catalogo.agregarLibro(Libro("Los miserables", "Clasico", "Victor Hugo", 3))
catalogo.agregarLibro(Libro("Matar a un ruiseñor", "Novela", "Harper Lee", 4))
catalogo.agregarLibro(Libro("Las venas abiertas de América Latina", "Historia", "Eduardo Galeano", 3))
catalogo.agregarLibro(Libro("Un mundo feliz", "Ciencia ficcion", "Aldous Huxley", 3))
catalogo.agregarLibro(Libro("El retrato de Dorian Gray", "Novela", "Oscar Wilde", 3))
catalogo.agregarLibro(Libro("La insoportable levedad del ser", "Novela", "Milan Kundera", 2))
catalogo.agregarLibro(Libro("El psicoanalista", "Thriller", "John Katzenbach", 4))
catalogo.agregarLibro(Libro("Cien años de soledad", "Novela", "Gabriel Garcia Marquez", 3))  # Ya lo tenías
catalogo.agregarLibro(Libro("El túnel", "Novela", "Ernesto Sabato", 2))
catalogo.agregarLibro(Libro("La tregua", "Novela", "Mario Benedetti", 3))
catalogo.agregarLibro(Libro("La metamorfosis", "Ficcion", "Franz Kafka", 4))
catalogo.agregarLibro(Libro("La rebelión de la granja", "Fabula politica", "George Orwell", 3))
catalogo.agregarLibro(Libro("Cómo ganar amigos e influir sobre las personas", "Autoayuda", "Dale Carnegie", 5))

# Función de ejemplo que representa el resto del sistema después del login
def menu_funcionalidades(usuario):
    while True:
        print("\n=== FUNCIONALIDADES ===")
        print("1. Visualizar Catalogo")
        print("2. Prestar libro")
        print("3. Consultar disponibilidad")
        print("4. Cerrar sesión")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            #BORRAR ESTO Y AÑADIR FUNCIONALIDAD
            print("🔧 Ejecutando funcionalidad 1...")
            print("¿Que deseas hacer?")
            print("1. Ver Catalogo")
            print("2. Filtrar Categoria")
            print("3. Busqueda Personalizada")

            opcion1 = input("Selecciona una opcion: ").strip()
            if opcion1=="1":
                print("Mostrando Catalogo...")
                catalogo.mostrarCatalogo()
            elif opcion1=="2":
                print("Filtrando Categoria...")
                print("¿Cuales son tus gustos?:")
                print("1.Novela")
                print("2.Fantasia")
                print("3.Matematicas")
                print("4.Autoayuda")
                print("5.Fabula Politica")
                print("6.Ficcion")
                print("7.Thriller")
                print("8.Ciencia ficcion")
                print("9.Historia")
                print("10.Clasico")
                print("11.Terror")
                print("12.Filosofia")
                print("13.Poesia")
                print("14.Romance")
                print("15.Finanzas")
                print("16.Autoayuda")
                print("17.Suspenso")
                print("18.Ciencia")
                opcion3= input("Ingresa el nombre la categoria que deseas: ").strip()
                catalogo.filtrarCategoria(opcion3)
        
            elif opcion1=="3":
                print("Mostrando Busqueda Personalizada...")
                #Catalogo.verCatalogo()
    
    


        elif opcion == "2":
            # Mostramos el módulo de solicitud de préstamo
            print("📖 SOLICITUD DE PRÉSTAMO")

            # Solicitamos el nombre del libro que quiere prestar
            nombre_libro = input("🔍 Ingrese el nombre del libro: ").strip()

            # Buscamos el libro en el catálogo
            libro_encontrado = None
            for libro in catalogo.libros:
                if libro.nombre.lower() == nombre_libro.lower():
                    libro_encontrado = libro
                    break

            # Si no se encuentra el libro, se muestra un mensaje
            if not libro_encontrado:
                print("❌ Libro no encontrado en el catálogo.")

            else:
                # Si el libro no tiene ejemplares disponibles
                if not libro_encontrado.disponible():
                    print("🚫 No hay ejemplares disponibles en este momento.")
                    print("🔔 Puede solicitar ser notificado cuando haya disponibilidad.")

                # Si el usuario tiene sanciones o es de un curso menor a 5°
                elif usuario.sanciones >= 3 or (usuario.rol == "Estudiante" and int(usuario.curso[0]) < 5):
                    print("⛔ No puede solicitar préstamos por sanciones o por ser de un grado menor a 5°.")

                else:
                    # Se realiza el préstamo
                    libro_encontrado.prestar()
                    prestamo_db = PrestamoDB()
                    fecha_devolucion = prestamo_db.realizar_prestamo(usuario, libro_encontrado)
                    prestamo_db.cerrar()

                    # Se muestra mensaje de confirmación
                    print("✅ Préstamo confirmado.")
                    print(f"📅 Puede recoger el libro en la biblioteca.")
                    print(f"🔁 Fecha de devolución: {fecha_devolucion}")
        elif opcion == "3":
            if usuario.rol not in ["Docente", "Administrativo"]:
                print("⛔ Acceso denegado: Esta funcionalidad es solo para docentes o administrativos.")
                continue
            gestor = GestorDisponibilidad()

            while True:
                print("\n--- CONSULTAR DISPONIBILIDAD ---")
                print("1. Buscar por hora")
                print("2. Buscar por fecha")
                print("3. Mostrar horarios disponibles y reservar")
                print("4. Volver al menú anterior")
                opcion = input("Seleccione una opción: ").strip()
        
                if opcion == "1":
                    try:
                        hora = int(input("⏰ Ingrese la hora (7 a 14): "))
                        gestor.buscar_por_hora(hora)
                    except ValueError:
                        print("⚠️ Debes ingresar un número entero.")
                elif opcion == "2":
                    fecha = input("📅 Ingrese la fecha (YYYY-MM-DD): ").strip()
                    gestor.buscar_por_fecha(fecha)
                elif opcion == "3":
                    gestor.mostrar_disponibles_y_reservar(usuario.nombre_completo)
                elif opcion == "4":
                    break
                else:
                    print("⚠️ Opción no válida.")


        elif opcion == "4":
            #BORRAR ESTO Y AÑADIR FUNCIONALIDAD
            print("🔒 Sesión cerrada.")
            break
        # AÑADIR MAS IF SI SE AÑADEN MAS FUNCIONALIDADES
        else:
            print("⚠️ Opción no válida.")

# Punto de entrada del programa

if __name__ == "__main__":
    usuario = mostrar_menu_autenticacion()
    if usuario:
        menu_funcionalidades(usuario)