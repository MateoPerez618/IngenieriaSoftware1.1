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

    # Inserta una nueva disponibilidad, opcionalmente con un usuario asignado
    def insertar_disponibilidad(self, entrada: Disponibilidad):
        if not (7 <= entrada.hora <= 14):
            print("⚠️ La hora debe estar entre 7 y 14.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO disponibilidad (fecha, hora, disponibilidad, usuario)
                VALUES (?, ?, ?, ?)
            """, (entrada.fecha, entrada.hora, entrada.estado.lower(), entrada.usuario))
            self.conn.commit()
            print("✅ Registro insertado correctamente.")
        except Exception as e:
            print(f"❌ Error al insertar el registro: {e}")

    def buscar_por_hora(self, hora):
        if not (7 <= hora <= 14):
            print("🚫 La hora debe estar entre 7 y 14.")
            return

        try:
            self.cursor.execute("""
                SELECT fecha, disponibilidad, usuario FROM disponibilidad
                WHERE hora = ?
            """, (hora,))
            resultados = self.cursor.fetchall()

            if resultados:
                print(f"\nResultados para la hora {hora}:00")
                solo_no = True
                for fecha, estado, usuario in resultados:
                    entrada = Disponibilidad(fecha, hora, estado, usuario)
                    print(entrada)
                    if estado.lower() == "si":
                        solo_no = False
                if solo_no:
                    print("❌ No hay disponibilidad para esa hora.")
            else:
                print("ℹ️ No hay registros para esa hora.")
        except Exception as e:
            print(f"❌ Error al buscar: {e}")

    def buscar_por_fecha(self, fecha):
        if not fecha or not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            print("⚠️ Formato de fecha inválido. Usa YYYY-MM-DD.")
            return

        try:
            self.cursor.execute("""
                SELECT hora, disponibilidad, usuario FROM disponibilidad
                WHERE fecha = ?
                ORDER BY hora
            """, (fecha,))
            resultados = self.cursor.fetchall()

            if resultados:
                print(f"\nDisponibilidad para el día {fecha}:")
                solo_no = True
                for hora, estado, usuario in resultados:
                    entrada = Disponibilidad(fecha, hora, estado, usuario)
                    print(entrada)
                    if estado.lower() == "si":
                        solo_no = False
                if solo_no:
                    print("❌ No hay disponibilidad en esa fecha.")
            else:
                print("ℹ️ No hay registros para esa fecha.")
        except Exception as e:
            print(f"❌ Error al buscar: {e}")

    def buscar_por_fecha_y_hora(self, fecha, hora):
        if not fecha or not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            print("⚠️ Formato de fecha inválido. Usa YYYY-MM-DD.")
            return
        if not (7 <= hora <= 14):
            print("🚫 La hora debe estar entre 7 y 14.")
            return

        try:
            self.cursor.execute("""
                SELECT disponibilidad, usuario FROM disponibilidad
                WHERE fecha = ? AND hora = ?
            """, (fecha, hora))
            resultado = self.cursor.fetchone()
            if resultado:
                estado, usuario = resultado
                if estado.lower() == "si":
                    print(f"✅ Sí hay disponibilidad para {fecha} a las {hora}:00.")
                else:
                    reservado_por = usuario if usuario else "desconocido"
                    print(f"❌ No hay disponibilidad. Reservado por: {reservado_por}.")
            else:
                print("ℹ️ No hay registros para esa combinación.")
        except Exception as e:
            print(f"❌ Error al buscar: {e}")
    def mostrar_disponibles_y_reservar(self, usuario_nombre):
        print("\n=== Horarios disponibles ===")
        self.cursor.execute("""
            SELECT id, fecha, hora FROM disponibilidad
            WHERE disponibilidad = 'si'
            ORDER BY fecha, hora
        """)
        disponibles = self.cursor.fetchall()
    
        if not disponibles:
            print("❌ No hay horarios disponibles para reservar.")
            return
    
        # Mostrar las opciones con un índice
        for i, (id_, fecha, hora) in enumerate(disponibles, start=1):
            print(f"{i}. {fecha} a las {hora}:00")
    
        try:
            opcion = int(input("Seleccione el número del horario que desea reservar: "))
            if not (1 <= opcion <= len(disponibles)):
                print("⚠️ Opción inválida.")
                return
        except ValueError:
            print("⚠️ Debe ingresar un número.")
            return
    
        # Obtener la fila seleccionada
        id_seleccionado, fecha, hora = disponibles[opcion - 1]
    
        # Actualizar en base de datos
        self.cursor.execute("""
            UPDATE disponibilidad
            SET disponibilidad = 'no', usuario = ?
            WHERE id = ? AND disponibilidad = 'si'
        """, (usuario_nombre, id_seleccionado))
        self.conn.commit()
    
        print(f"✅ Horario reservado: {fecha} a las {hora}:00 por {usuario_nombre}.")


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


