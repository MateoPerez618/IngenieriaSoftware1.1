import sqlite3

# Clase que representa a un usuario en el sistema
class Usuario:
    def __init__(self, nombre_completo, password, curso, rol, sanciones=0, penalizacion=False):
        # Inicializa los atributos del usuario
        self.nombre_completo = nombre_completo
        self.password = password
        self.curso = curso
        self.rol = rol
        self.sanciones = sanciones
        self.penalizacion = penalizacion

    def __str__(self):
        # Devuelve una representación en texto del usuario, útil para imprimirlo
        return f"{self.nombre_completo} ({self.rol}, Curso: {self.curso})"


# Clase para manejar todas las operaciones relacionadas con la base de datos
class UsuarioDB:
    def __init__(self, db_name="usuarios.db"):
        # Conecta a la base de datos SQLite (o la crea si no existe)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._crear_tabla()  # Asegura que la tabla de usuarios exista

    def _crear_tabla(self):
        # Crea la tabla 'usuarios' si no existe, con todos los campos requeridos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                nombre_completo TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                curso TEXT NOT NULL,
                rol TEXT NOT NULL,
                sanciones INTEGER DEFAULT 0,
                penalizacion BOOLEAN DEFAULT 0
            )
        """)
        self.conn.commit()

    def registrar(self, usuario: Usuario):
        # Registra un nuevo usuario en la base de datos, si no existe previamente
        if self.existe_usuario(usuario.nombre_completo):
            print("❌ El usuario ya existe.")
            return False
        self.cursor.execute("""
            INSERT INTO usuarios (nombre_completo, password, curso, rol, sanciones, penalizacion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (usuario.nombre_completo, usuario.password, usuario.curso, usuario.rol,
              usuario.sanciones, usuario.penalizacion))
        self.conn.commit()
        print("✅ Usuario registrado exitosamente.")
        return True

    def login(self, nombre_completo, password):
        # Intenta iniciar sesión con nombre y contraseña; si tiene éxito, retorna el objeto Usuario
        self.cursor.execute("""
            SELECT * FROM usuarios WHERE nombre_completo = ? AND password = ?
        """, (nombre_completo, password))
        row = self.cursor.fetchone()
        if row:
            usuario = Usuario(*row)  # Crea un objeto Usuario con los datos de la base
            print(f"✅ Bienvenido, {usuario.nombre_completo}.")
            return usuario
        print("❌ Usuario o contraseña incorrectos.")
        return None

    def existe_usuario(self, nombre_completo):
        # Verifica si un usuario ya existe en la base de datos
        self.cursor.execute("SELECT 1 FROM usuarios WHERE nombre_completo = ?", (nombre_completo,))
        return self.cursor.fetchone() is not None

    def cerrar(self):
        # Cierra la conexión con la base de datos
        self.conn.close()


# Función que muestra el menú de autenticación (registro e inicio de sesión)
# Se llama desde main.py y devuelve el usuario si inicia sesión correctamente
def mostrar_menu_autenticacion():
    db = UsuarioDB()  # Creamos una instancia para acceder a la base de datos

    while True:
        # Menú principal de autenticación
        print("\n=== MENÚ DE INICIO ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()

        # Opción de registro
        if opcion == "1":
            print("\n--- REGISTRO ---")
            nombre = input("Nombre completo: ").strip()
            password = input("Contraseña: ").strip()
            curso = input("Curso: ").strip()

            # Solicita el rol y traduce el código a nombre completo
            while True:
                rol_input = input("Rol (E = Estudiante, P = Profesor, A = Administrativo): ").strip().upper()
                if rol_input == "E":
                    rol = "Estudiante"
                    break
                elif rol_input == "P":
                    rol = "Docente"
                    break
                elif rol_input == "A":
                    rol = "Administrativo"
                    break
                else:
                    print("⚠️ Opción no válida. Ingrese E, P o A.")

            # Crea una instancia de Usuario y lo registra en la base de datos
            usuario = Usuario(nombre, password, curso, rol)
            db.registrar(usuario)

        # Opción de inicio de sesión
        elif opcion == "2":
            print("\n--- INICIAR SESIÓN ---")
            nombre = input("Nombre completo: ").strip()
            password = input("Contraseña: ").strip()

            # Intenta iniciar sesión; si es exitoso, retorna el usuario al main
            usuario = db.login(nombre, password)
            if usuario:
                db.cerrar()
                return usuario

        # Salir del programa
        elif opcion == "3":
            print("👋 Hasta luego.")
            db.cerrar()
            return None

        # Cualquier entrada inválida
        else:
            print("⚠️ Opción no válida.")
