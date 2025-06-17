# autenticacion.py
import sqlite3

class UsuarioDB:
    def __init__(self, db_name="usuarios.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def registrar(self, username, password):
        if self.existe_usuario(username):
            print("❌ El usuario ya existe.")
            return False
        self.cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()
        print("✅ Usuario registrado exitosamente.")
        return True

    def login(self, username, password):
        self.cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
        if self.cursor.fetchone():
            print(f"✅ Bienvenido, {username}.")
            return True
        print("❌ Usuario o contraseña incorrectos.")
        return False

    def existe_usuario(self, username):
        self.cursor.execute("SELECT 1 FROM usuarios WHERE username = ?", (username,))
        return self.cursor.fetchone() is not None

    def cerrar(self):
        self.conn.close()


# Esta función será llamada desde main.py
def mostrar_menu_autenticacion():
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
                db.cerrar()
                return True  # Devuelve True si inicia sesión correctamente

        elif opcion == "3":
            print("👋 Hasta luego.")
            db.cerrar()
            return False  # Finaliza el programa

        else:
            print("⚠️ Opción no válida.")
