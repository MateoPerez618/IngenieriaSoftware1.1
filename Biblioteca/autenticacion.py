import sqlite3

# Clase que representa un usuario
class Usuario:
    def __init__(self, nombre_completo, password, curso, rol, sanciones=0, penalizacion=False, correo=None, autenticado="no"):
        self.nombre_completo = nombre_completo
        self.password = password
        self.curso = curso
        self.rol = rol
        self.sanciones = sanciones
        self.penalizacion = penalizacion
        self.correo = correo
        self.autenticado = autenticado


# Clase para manejar la base de datos
class UsuarioDB:
    def __init__(self, db_name="usuarios.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
        # Elimina la tabla actual si existe
        #self.cursor.execute("DROP TABLE IF EXISTS usuarios")
    
        # Crea una nueva tabla con los nuevos campos añadidos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                nombre_completo TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                curso TEXT NOT NULL,
                rol TEXT NOT NULL,
                sanciones INTEGER DEFAULT 0,
                penalizacion BOOLEAN DEFAULT 0,
                correo TEXT,
                autenticado TEXT DEFAULT 'no'
            )
        """)
        self.conn.commit()


    def registrar(self, usuario: Usuario):
        if self.existe_usuario_por_nombre_y_curso(usuario.nombre_completo, usuario.curso):
            return False, "El usuario ya existe."
        self.cursor.execute("""
            INSERT INTO usuarios (nombre_completo, password, curso, rol, sanciones, penalizacion, correo, autenticado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (usuario.nombre_completo, usuario.password, usuario.curso,
              usuario.rol, usuario.sanciones, usuario.penalizacion, usuario.correo, usuario.autenticado))
        self.conn.commit()
        return True, "Usuario registrado exitosamente."

    def login(self, nombre_completo, password):
        self.cursor.execute("""
            SELECT * FROM usuarios WHERE nombre_completo = ? AND password = ?
        """, (nombre_completo, password))
        row = self.cursor.fetchone()
        if row:
            return Usuario(*row)
        return None

    def existe_usuario_por_nombre_y_curso(self, nombre, curso):
        self.cursor.execute("SELECT 1 FROM usuarios WHERE nombre_completo = ? AND curso = ?", (nombre, curso))
        return self.cursor.fetchone() is not None


    def cerrar(self):
        self.conn.close()
