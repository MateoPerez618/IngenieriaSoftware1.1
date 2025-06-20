# main.py
from autenticacion import mostrar_menu_autenticacion    



#Crear instancias para libros


# Función de ejemplo que representa el resto del sistema después del login
def menu_funcionalidades():
    while True:
        print("\n=== FUNCIONALIDADES ===")
        print("1. Funcionalidad 1")
        print("2. Funcionalidad 2")
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
            #BORRAR ESTO Y AÑADIR FUNCIONALIDAD
            print("🔧 Ejecutando funcionalidad 2...")
        elif opcion == "3":
            #BORRAR ESTO Y AÑADIR FUNCIONALIDAD
            print("🔒 Sesión cerrada.")
            break
        # AÑADIR MAS IF SI SE AÑADEN MAS FUNCIONALIDADES
        else:
            print("⚠️ Opción no válida.")

# Punto de entrada del programa
if __name__ == "__main__":
    # Llamamos al menú de autenticación. Si retorna True, iniciamos funcionalidades.
    if mostrar_menu_autenticacion():
        menu_funcionalidades()
