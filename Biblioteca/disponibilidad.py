import sqlite3
import re
import random
from datetime import datetime, timedelta

# Clase que representa una entrada de disponibilidad (fecha, hora, estado)
class Disponibilidad:
    def __init__(self, fecha, hora, estado):
        self.fecha = fecha
        self.hora = hora
        self.estado = estado  # 'si' o 'no'

    def __str__(self):
        return f"{self.fecha} a las {self.hora}:00 — Disponible: {self.estado}"


# Clase que gestiona todas las operaciones de la base de datos relacionadas con la disponibilidad
class GestorDisponibilidad:
    def __init__(self, db_name="usuarios.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._crear_tabla_si_no_existe()

    # Crea la tabla si no existe en la base de datos 'biblioteca'
    def _crear_tabla_si_no_existe(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS disponibilidad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                hora INTEGER NOT NULL CHECK(hora >= 0 AND hora <= 24),
                disponibilidad TEXT NOT NULL CHECK(disponibilidad IN ('si', 'no'))
            );
        """)
        self.conn.commit()

    # Inserta una nueva entrada de disponibilidad en la base de datos
    def insertar_disponibilidad(self, entrada: Disponibilidad):
        if not (7 <= entrada.hora <= 14):
            print("⚠️ La hora debe estar entre 7 y 14.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO disponibilidad (fecha, hora, disponibilidad)
                VALUES (?, ?, ?)
            """, (entrada.fecha, entrada.hora, entrada.estado.lower()))
            self.conn.commit()
            print("✅ Registro insertado correctamente.")
        except Exception as e:
            print(f"❌ Error al insertar el registro: {e}")

    # Búsqueda por hora (muestra fechas con ese horario)
    def buscar_por_hora(self, hora):
        if not (7 <= hora <= 14):
            print("🚫 La hora debe estar entre 7 y 14.")
            return

        try:
            self.cursor.execute("""
                SELECT fecha, disponibilidad FROM disponibilidad
                WHERE hora = ?
            """, (hora,))
            resultados = self.cursor.fetchall()

            if resultados:
                print(f"\nResultados para la hora {hora}:00")
                solo_no = True
                for fecha, estado in resultados:
                    print(f"📅 {fecha} — Disponibilidad: {estado}")
                    if estado.lower() == "si":
                        solo_no = False
                if solo_no:
                    print("❌ No hay disponibilidad para esa hora.")
            else:
                print("ℹ️ No hay registros para esa hora.")
        except Exception as e:
            print(f"❌ Error al buscar: {e}")

    # Búsqueda por fecha (muestra todas las horas con su estado)
    def buscar_por_fecha(self, fecha):
        if not fecha or not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            print("⚠️ Formato de fecha inválido. Usa YYYY-MM-DD.")
            return

        try:
            self.cursor.execute("""
                SELECT hora, disponibilidad FROM disponibilidad
                WHERE fecha = ?
                ORDER BY hora
            """, (fecha,))
            resultados = self.cursor.fetchall()

            if resultados:
                print(f"\nDisponibilidad para el día {fecha}:")
                solo_no = True
                for hora, estado in resultados:
                    print(f"{hora}:00 — Disponibilidad: {estado}")
                    if estado.lower() == "si":
                        solo_no = False
                if solo_no:
                    print("❌ No hay disponibilidad en esa fecha.")
            else:
                print("ℹ️ No hay registros para esa fecha.")
        except Exception as e:
            print(f"❌ Error al buscar: {e}")

    # Búsqueda específica por fecha y hora
    def buscar_por_fecha_y_hora(self, fecha, hora):
        if not fecha or not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            print("⚠️ Formato de fecha inválido. Usa YYYY-MM-DD.")
            return
        if not (7 <= hora <= 14):
            print("🚫 La hora debe estar entre 7 y 14.")
            return

        try:
            self.cursor.execute("""
                SELECT disponibilidad FROM disponibilidad
                WHERE fecha = ? AND hora = ?
            """, (fecha, hora))
            resultado = self.cursor.fetchone()
            if resultado:
                estado = resultado[0].lower()
                if estado == "si":
                    print(f"✅ Sí hay disponibilidad para {fecha} a las {hora}:00.")
                else:
                    print("❌ No hay disponibilidad para esa fecha y hora.")
            else:
                print("ℹ️ No hay registros para esa combinación.")
        except Exception as e:
            print(f"❌ Error al buscar: {e}")

    # Cierra la conexión con la base de datos al destruir la instancia
    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            print("🔒 Conexión cerrada.")

            
            
# ***** principal *******
# Simulación de uso en un menú principal o pruebas

gestor = GestorDisponibilidad()

# Insertar una nueva disponibilidad
#entrada = Disponibilidad("2025-06-18", 9, "si")
#gestor.insertar_disponibilidad(entrada)

# Buscar por hora
# gestor.buscar_por_hora(9)

# Buscar por fecha
# gestor.buscar_por_fecha("2025-06-18")

# Buscar por fecha y hora
# gestor.buscar_por_fecha_y_hora("2025-06-18", 9)

