#Historia de usuario: Consultar horarios

import sqlite3
import re

#Es importante filtrar a los usuarios que quieran usar esta funcionalidad, para que solo puedan acceder a ella docentes/administrativos.

class disponibilidad:
    
    #El siguiente método se ejecuta automáticamente cuando creas una instancia de esta clase. Aquí se conecta a la base de datos y crea la tabla **disponibilidad** si esta aún no existe.
    
    def __init__(self, db_name="disponibilidad.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor =  self.conn.cursor()
        self._crear_tabla_si_no_existe()
    
    #La tabla que se crea para disponibilidad debe de estar en la base de datos general de la bilbioteca!!! (Faltaría esto) Es decir, en una misma base de datos llamada **biblioteca** deben encontrarse las tablas de **usuarios**, **disponibilidad**  y **catálogo**.

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
        
    #El estado de disponibilidad (si/no), debe ser introducido manualmente. Inicialmente y, preferiblemente, es editado por la secretaria (quien marca en un principio los horarios en los que SI hay disponibilidad). Pero docentes/administrativos (y, por supuesto, la secretaria), tienen la capacidad de cambiar esto.
    #Lo anterior es, claro, para que las personas con dichos roles puedan reservar el espacio por su cuenta (cambiando el estado de disponibilidad de "si" a "no").
    #PROBLEMA! El siguiente método entonces, esta directamente relacionado con HU07 (Solicitar reserva). De hecho, es buena parte de en lo que consiste la funcioalidad de reserva.
    #Esto puede significar que las historias de usuario no están bien diseñadas.
    
    def insertar_disponibilidad(self):
        # Solicitar datos al usuario
        fecha = input("Ingrese la fecha (YYYY-MM-DD): ")
        try:
            hora = int(input("Ingrese la hora (entre 7 y 14): "))
        except ValueError:
            print("La hora debe ser un número entero.")
            return
        
        disponibilidad_valor = input("¿Está disponible? (si/no): ").lower()

        if not (7 <= hora <= 14):
            print("La hora debe estar entre 7 y 14.")
            return

        # Insertar en la base de datos
        try:
            self.cursor.execute("""
                INSERT INTO disponibilidad (fecha, hora, disponibilidad)
                VALUES (?, ?, ?)
            """, (fecha, hora, disponibilidad_valor))
            self.conn.commit()
            print("Registro insertado correctamente.")
        except Exception as e:
            print(f"Ocurrió un error al insertar el registro: {e}")
    
    #Busqueda de disponibilidad por filtros de fecha u hora.
    #Cumple con lo mencionado en el desglose de tareas c:
    #Aquí si ninguna hora en la fecha buscada está disponible o al contrario (no hay ningún día disponible para la hora buscada), se muestra en pantalla el mensaje "No hay disponibilidad para esa fecha u hora"
    #También impide que ingreses carácteres inválidos (como letras o signos de puntuación) o dejes campos vacíos.
    
    def buscar_por_hora(self):
        try:
            hora = int(input("⏰ Ingrese la hora a buscar (entre 7 y 14): "))
        except ValueError:
            print("⚠️ La hora está en un formato de 24 horas. Recuerda que debes ingresar un número entero.")
            return
    
        if not (7 <= hora <= 14):
            print("🚫 La hora debe estar entre 7 a.m. y 14 p.m.")
            return
    
        try:
            self.cursor.execute("""
                SELECT fecha, disponibilidad FROM disponibilidad
                WHERE hora = ?
            """, (hora,))
            resultados = self.cursor.fetchall()
    
            if resultados:
                print(f"\nResultados para la hora {hora}:")
                solo_no = True  # Suponemos que todas son "no" hasta demostrar lo contrario
    
                for fila in resultados:
                    fecha, disponibilidad_valor = fila
                    print(f"Fecha: {fecha} | Disponibilidad: {disponibilidad_valor}")
                    if disponibilidad_valor.strip().lower() == "si":
                        solo_no = False  # Hay al menos una disponibilidad "si"
    
                if solo_no:
                    print("❌ No hay disponibilidad para esa fecha u hora.")
            else:
                print(f"No hay registros para la hora {hora}.")
        except Exception as e:
            print(f"Error al buscar registros: {e}")

    def buscar_por_fecha(self):
        fecha = input("📅 Ingrese la fecha a buscar (YYYY-MM-DD): ").strip()
    
        # Validar que la fecha no esté vacía y cumpla el formato correcto usando regex
        if not fecha or not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            print("🚫 Recuerda que para buscar la fecha que quieres debes ingresar año-mes-día (con el guión de por medio)")
            return
    
        try:
            self.cursor.execute("""
                SELECT hora, disponibilidad FROM disponibilidad
                WHERE fecha = ?
                ORDER BY hora
            """, (fecha,))
            resultados = self.cursor.fetchall()
    
            if resultados:
                print(f"\nResultados para la fecha {fecha}:")
                solo_no = True  # Suponemos que todas son "no" hasta demostrar lo contrario
    
                for fila in resultados:
                    hora, disponibilidad_valor = fila
                    print(f"Hora: {hora} | Disponibilidad: {disponibilidad_valor}")
                    if disponibilidad_valor.strip().lower() == "si":
                        solo_no = False  # Hay al menos una disponibilidad "si"
    
                if solo_no:
                    print("❌ No hay disponibilidad para esa fecha u hora.")
            else:
                print(f"No hay registros para la fecha {fecha}.")
        except Exception as e:
            print(f"Error al buscar registros: {e}")
    
    #También puedes buscar por fecha y hora al mismo tiempo.
    
    def buscar_por_fecha_y_hora(self):
        fecha = input("📅 Ingrese la fecha a buscar (YYYY-MM-DD): ").strip()
        
        # Validar que la fecha no esté vacía y cumpla el formato correcto usando regex
        if not fecha or not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            print("🚫 Recuerda que para buscar la fecha que quieres debes ingresar año-mes-día")
            return
        
        try:
            hora = int(input("⏰ Ingrese la hora a buscar (entre 7 y 14): "))
        except ValueError:
            print("⚠️ La hora está en un formato de 24 horas. Recuerda que debes ingresar un número entero.")
            return
    
        if not (7 <= hora <= 14):
            print("🚫 La hora debe estar entre 7 a.m. y 14 p.m.")
            return
    
        try:
            self.cursor.execute("""
                SELECT disponibilidad FROM disponibilidad
                WHERE fecha = ? AND hora = ?
            """, (fecha, hora))
            resultado = self.cursor.fetchone()
    
            if resultado:
                disponibilidad_valor = resultado[0].strip().lower()
                if disponibilidad_valor == "no":
                    print("❌ No hay disponibilidad para esa fecha y hora.")
                else:
                    print(f"\n✅ Si hay disponibilidad para {fecha} a las {hora}:00")
            else:
                print(f"No hay registro para {fecha} a las {hora}:00.")
        except Exception as e:
            print(f"Error al buscar registros: {e}")
        
    
    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            print("Conexión cerrada.")
            
            
# ***** principal *******
d = disponibilidad()
#d.insertar_disponibilidad()
#d.buscar_por_hora()
#d.buscar_por_fecha()
#d.buscar_por_fecha_y_hora()