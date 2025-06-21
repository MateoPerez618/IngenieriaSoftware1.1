import sqlite3
from datetime import datetime, timedelta

# Esta clase maneja los préstamos de libros en la base de datos
class PrestamoDB:
    def __init__(self, db_name="usuarios.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._crear_tabla()

    # Crear tabla de préstamos si no existe
    def _crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                libro TEXT NOT NULL,
                fecha_prestamo TEXT NOT NULL,
                fecha_devolucion TEXT NOT NULL
            )
        """)
        self.conn.commit()

    # Registrar un préstamo en la base de datos
    def realizar_prestamo(self, usuario, libro):
        fecha_prestamo = datetime.today()
        fecha_devolucion = fecha_prestamo + timedelta(days=7)
        self.cursor.execute("""
            INSERT INTO prestamos (usuario, libro, fecha_prestamo, fecha_devolucion)
            VALUES (?, ?, ?, ?)
        """, (
            usuario.nombre_completo,
            libro.nombre,
            fecha_prestamo.strftime("%Y-%m-%d"),
            fecha_devolucion.strftime("%Y-%m-%d")
        ))
        self.conn.commit()
        return fecha_devolucion.strftime("%Y-%m-%d")

    def cerrar(self):
        self.conn.close()