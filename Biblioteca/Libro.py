import sqlite3
class Libro:
    def __init__(self, nombre, categoria, autor, cantidad):
        self.nombre = nombre
        self.autor = autor
        self.categoria = categoria
        self.cantidad = cantidad
        self.calificaciones = []
        self.reseñas = []

class LibroDB:
    def __init__(self, db_name="usuarios.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._crear_tabla()

    def _crear_tabla(self):
        # Crear tabla si no existe
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS libros (
                nombre TEXT PRIMARY KEY,
                autor TEXT NOT NULL,
                categoria TEXT NOT NULL,
                cantidad INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def obtener_todos(self):
        self.cursor.execute("SELECT nombre, categoria, autor, cantidad FROM libros")
        filas = self.cursor.fetchall()
        return [Libro(*fila) for fila in filas]
    
    def restar_cantidad(self, nombre_libro):
        self.cursor.execute("""
            UPDATE libros
            SET cantidad = cantidad - 1
            WHERE nombre = ? AND cantidad > 0
        """, (nombre_libro,))
        self.conn.commit()

   

# Lista de libros a insertar
"""libros = [
    ("Cien años de soledad", "Gabriel García Márquez", "Novela", 5),
    ("1984", "George Orwell", "Distopía", 4),
    ("Don Quijote de la Mancha", "Miguel de Cervantes", "Clásico", 3),
    ("El principito", "Antoine de Saint-Exupéry", "Fábula", 6),
    ("Orgullo y prejuicio", "Jane Austen", "Romance", 4),
    ("Rayuela", "Julio Cortázar", "Ficción", 2),
    ("Crónica de una muerte anunciada", "Gabriel García Márquez", "Novela", 5),
    ("La sombra del viento", "Carlos Ruiz Zafón", "Misterio", 3),
    ("El nombre del viento", "Patrick Rothfuss", "Fantasía", 4),
    ("Los juegos del hambre", "Suzanne Collins", "Juvenil", 5),
    ("Harry Potter y la piedra filosofal", "J.K. Rowling", "Fantasía", 6),
    ("La ladrona de libros", "Markus Zusak", "Histórica", 4),
    ("Matar a un ruiseñor", "Harper Lee", "Clásico", 3),
    ("La metamorfosis", "Franz Kafka", "Filosofía", 3),
    ("El código Da Vinci", "Dan Brown", "Thriller", 5),
    ("El alquimista", "Paulo Coelho", "Inspiracional", 5),
    ("Fahrenheit 451", "Ray Bradbury", "Ciencia ficción", 4),
    ("Drácula", "Bram Stoker", "Terror", 3),
    ("Frankenstein", "Mary Shelley", "Terror", 3),
    ("El señor de los anillos", "J.R.R. Tolkien", "Fantasía épica", 2)
]

# Insertar libros (ignorar duplicados si ya existen)
for libro in libros:
    try:
        cursor.execute("INSERT INTO libros (nombre, autor, categoria, cantidad) VALUES (?, ?, ?, ?)", libro)
    except sqlite3.IntegrityError:
        pass  # Ya existe

# Guardar y cerrar
conn.commit()
conn.close()

print("✅ Base de datos 'biblioteca.db' creada con 20 libros.")"""
