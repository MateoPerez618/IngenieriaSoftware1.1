# main.py
from autenticacion import UsuarioDB

def menu_principal():
    db = UsuarioDB()

    while True:
        print("\n=== MENÚ DE INICIO ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            username = input("Nuevo usuario: ").strip()
            password = input("Contraseña: ").strip()
            db.registrar(username, password)

        elif opcion == "2":
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            if db.login(username, password):
                menu_funcionalidades()
                break

        elif opcion == "3":
            print("👋 Hasta luego.")
            db.cerrar()
            break
        else:
            print("⚠️ Opción no válida.")

def menu_funcionalidades():
    while True:
        print("\n=== FUNCIONALIDADES ===")
        print("1. Cerrar sesión")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            print("🔒 Sesión cerrada.")
            break
        else:
            print("⚠️ Opción no válida.")

if __name__ == "__main__":
    menu_principal()
