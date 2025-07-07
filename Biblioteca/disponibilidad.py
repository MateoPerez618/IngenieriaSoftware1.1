import sqlite3
import re
import random
from datetime import datetime, timedelta

# Clase que representa una entrada de disponibilidad con el usuario asociado (si existe)
class Disponibilidad:
    def __init__(self, fecha, hora, estado, usuario=None):
        self.fecha = fecha
        self.hora = hora
        self.estado = estado  # 'si' o 'no'
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

    def buscar_disponibilidad(self, fecha=None, hora=None):
        consulta = "SELECT fecha, hora, disponibilidad, usuario FROM disponibilidad WHERE disponibilidad = 'si'"
        condiciones = []
        parametros = []
    
        if fecha:
            condiciones.append("fecha = ?")
            parametros.append(fecha)
        if hora:
            condiciones.append("hora = ?")
            parametros.append(hora)
    
        if condiciones:
            consulta += " AND " + " AND ".join(condiciones)
    
        consulta += " ORDER BY fecha, hora"
    
        self.cursor.execute(consulta, tuple(parametros))
        registros = self.cursor.fetchall()
    
        return [Disponibilidad(f, h, d, u) for f, h, d, u in registros]



# Insertar una nueva disponibilidad
#entrada = Disponibilidad("2025-06-18", 9, "si")
#gestor.insertar_disponibilidad(entrada)

# Buscar por hora
# gestor.buscar_por_hora(9)

# Buscar por fecha
# gestor.buscar_por_fecha("2025-06-18")

# Buscar por fecha y hora
# gestor.buscar_por_fecha_y_hora("2025-06-18", 9)


