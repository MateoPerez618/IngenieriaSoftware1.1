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
    
    # Mostrar todos los préstamos
    def ver_todos_los_prestamos(self):
        self.cursor.execute("""
            SELECT usuario, libro, fecha_prestamo FROM prestamos
        """)
        prestamos = self.cursor.fetchall()
        if not prestamos:
            print("📭 No hay préstamos registrados.")
        else:
            print("📋 Lista de préstamos:")
            for usuario, libro, fecha in prestamos:
                print(f"📖 {libro} — 📅 {fecha} — 👤 {usuario}")

    # Buscar préstamo por nombre de libro o autor
    def buscar_por_libro(self, texto):
        self.cursor.execute("""
            SELECT usuario, libro, fecha_prestamo FROM prestamos
            WHERE libro LIKE ?
        """, ('%' + texto + '%',))
        resultados = self.cursor.fetchall()
        if resultados:
            print(f"🔍 Resultados para libros que contienen '{texto}':")
            for usuario, libro, fecha in resultados:
                print(f"📖 {libro} — 📅 {fecha} — 👤 {usuario}")
        else:
            print("❌ No se encontraron préstamos para ese libro.")

    # Buscar préstamos por nombre de usuario
    def buscar_por_usuario(self, nombre_usuario):
        self.cursor.execute("""
            SELECT libro, fecha_prestamo FROM prestamos
            WHERE usuario = ?
        """, (nombre_usuario,))
        resultados = self.cursor.fetchall()
        if resultados:
            print(f"📚 Libros prestados a {nombre_usuario}:")
            for libro, fecha in resultados:
                print(f"📖 {libro} — 📅 {fecha}")
        else:
            print("❌ Ese usuario no tiene libros prestados.")
            

    def cerrar(self):
        self.conn.close()