import sqlite3

#Es importante filtrar a los usuarios que quieran usar esta funcionalidad, para que solo puedan acceder a ella docentes/administrativos.

class disponibilidad:
        
    def __init__(self, db_name="disponibilidad.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor =  self.conn.cursor()
        self._crear_tabla_si_no_existe()
    
    #La tabla que se crea para disponibilidad debe de estar en la base de datos general de la bilbioteca.

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
        
   
    def insertar_disponibilidad(self):
        # Solicitar datos al usuario
        fecha = input("Ingrese la fecha (YYYY-MM-DD): ")
        try:
            hora = int(input("Ingrese la hora (entre 6 y 16): "))
        except ValueError:
            print("La hora debe ser un número entero.")
            return
        
        disponibilidad_valor = input("¿Está disponible? (si/no): ").lower()

        if not (6 <= hora <= 16):
            print("La hora debe estar entre 6 y 16.")
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
    
    #Busqueda de disponibilidad por fecha y/u hora
    
    def buscar_por_hora(self):
        try:
            hora = int(input("Ingrese la hora a buscar (entre 6 y 16): "))
        except ValueError:
            print("La hora debe ser un número entero.")
            return
    
        if not (6 <= hora <= 16):
            print("La hora debe estar entre 6 y 16.")
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
                    print("No hay disponibilidad para esa fecha u hora.")
            else:
                print(f"No hay registros para la hora {hora}.")
        except Exception as e:
            print(f"Error al buscar registros: {e}")

    def buscar_por_fecha(self):
        fecha = input("Ingrese la fecha a buscar (YYYY-MM-DD): ").strip()
    
        try:
            self.cursor.execute("""
                SELECT hora, disponibilidad FROM disponibilidad
                WHERE fecha = ?
                ORDER BY hora
            """, (fecha,))
            resultados = self.cursor.fetchall()
    
            if resultados:
                print(f"\nResultados para la fecha {fecha}:")
                # Suponemos que todas son "no" hasta demostrar lo contrario
                solo_no = True
                for hora, disponibilidad_valor in resultados:
                    disponibilidad_valor = disponibilidad_valor.strip().lower()
                    print(f"Hora: {hora} | Disponibilidad: {disponibilidad_valor}")
                    if disponibilidad_valor == "si":
                        solo_no = False
                if solo_no:
                    print("No hay disponibilidad para esa fecha u hora.")
            else:
                print(f"No hay registros para la fecha {fecha}.")
        except Exception as e:
            print(f"Error al buscar registros: {e}")

    def buscar_por_fecha_y_hora(self):
        fecha = input("Ingrese la fecha a buscar (YYYY-MM-DD): ").strip()
        try:
            hora = int(input("Ingrese la hora a buscar (entre 6 y 16): "))
        except ValueError:
            print("La hora debe ser un número entero.")
            return

        if not (6 <= hora <= 16):
            print("La hora debe estar entre 6 y 16.")
            return

        try:
            self.cursor.execute("""
                SELECT disponibilidad FROM disponibilidad
                WHERE fecha = ? AND hora = ?
            """, (fecha, hora))
            resultado = self.cursor.fetchone()

            if resultado:
                print(f"\n¿Hay disponibilidad para {fecha} a las {hora}:00? → {resultado[0]}")
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
# d.buscar_por_hora()
d.buscar_por_fecha()
# d.buscar_por_fecha_y_hora()