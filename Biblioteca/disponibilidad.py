import sqlite3
import re
import random
from datetime import datetime, timedelta

# Clase que representa una entrada de disponibilidad con el usuario asociado (si existe)
class Disponibilidad:
    def __init__(self, id, fecha, hora, disponibilidad, usuario=None):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.disponibilidad = disponibilidad  # 'si' o 'no'
        self.usuario = usuario  # nombre completo del usuario que reservó (None si está disponible)

    def __str__(self):
        reservado_por = f" — Reservado por: {self.usuario}" if self.usuario else ""
        return f"{self.fecha} a las {self.hora}:00 — Disponible: {self.estado}{reservado_por}"


# Clase que gestiona todas las operaciones de la base de datos relacionadas con la disponibilidad
class GestorDisponibilidad:
    def __init__(self, db_name="usuarios.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._crear_tabla_si_no_existe()

    def _crear_tabla_si_no_existe(self):
        # Crea la tabla con la columna usuario si aún no existe
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS disponibilidad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                hora INTEGER NOT NULL CHECK(hora >= 0 AND hora <= 24),
                disponibilidad TEXT NOT NULL CHECK(disponibilidad IN ('si', 'no')),
                usuario TEXT DEFAULT NULL
            );
        """)
        self.conn.commit() 

    def buscar_disponibilidad(self, fecha=None, hora=None, mostrar_todo=False):
        query = "SELECT * FROM disponibilidad WHERE 1=1"
        params = []
    
        if fecha:
            query += " AND fecha = ?"
            params.append(fecha)
        if hora:
            query += " AND hora = ?"
            params.append(hora)
        if not mostrar_todo:
            query += " AND disponibilidad = 'si'"
    
        self.cursor.execute(query, params)
        resultados = self.cursor.fetchall()
    
        return [Disponibilidad(*r) for r in resultados]
