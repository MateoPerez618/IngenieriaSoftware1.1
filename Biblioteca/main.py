# main.py
from autenticacion import mostrar_menu_autenticacion    
from Catalogo import Catalogo
from Libro import Libro
from Prestamo import PrestamoDB 


#Crear instancias para libros
catalogo = Catalogo()
# Cargar libros de ejemplo los cambiamos luego
catalogo.agregar_libro(Libro("Cien años de soledad", "Novela", 3))
catalogo.agregar_libro(Libro("El Principito", "Fantasía", 2))
catalogo.agregar_libro(Libro("Álgebra de Baldor", "Matemáticas", 1))

# Función de ejemplo que representa el resto del sistema después del login
def menu_funcionalidades(usuario):
    while True:
        print("\n=== FUNCIONALIDADES ===")
        print("1. Funcionalidad 1")
        print("2. Prestar libro")
        print("3. Cerrar sesión")

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
                #Catalogo.verCatalogo()
            elif opcion1=="2":
                print("Filtrando Categoria...")
                #Catalogo.verCatalogo()
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