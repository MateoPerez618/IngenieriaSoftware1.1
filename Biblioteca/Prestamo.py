import sqlite3
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

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
                fecha_devolucion TEXT NOT NULL,
                estado_devolucion TEXT DEFAULT 'pendiente'
            )
        """)
        self.conn.commit()

    # Registrar un préstamo en la base de datos
    def realizar_prestamo(self, usuario, libro):
        fecha_prestamo = datetime.today()
        fecha_devolucion = fecha_prestamo + timedelta(days=7)
        self.cursor.execute("""
            INSERT INTO prestamos (usuario, libro, fecha_prestamo, fecha_devolucion, estado_devolucion, estado_prestamo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            usuario.nombre_completo,
            libro.nombre,
            fecha_prestamo.strftime("%Y-%m-%d"),
            fecha_devolucion.strftime("%Y-%m-%d"),
            estado_devolucion := 'pendiente',
            estado_prestamo := 'solicitado'
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
            

    def _enviar_correo_real(self, correo, asunto, mensaje):
        remitente = "carolinaespinosajurado@gmail.com"
        clave = "bfzp pgmz yexk uymt"
    
        msg = MIMEText(mensaje)
        msg['Subject'] = asunto
        msg['From'] = remitente
        msg['To'] = correo
    
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(remitente, clave)
                smtp.send_message(msg)
                print(f"📤 Correo enviado a {correo}")
        except Exception as e:
            print(f"❌ Error al enviar a {correo}: {e}")
            
    def _enviar_correo_simulado(self, correo, asunto, mensaje):
        print(f"--- Enviando a: {correo} ---")
        print(f"Asunto: {asunto}")
        print(mensaje)
        print("-" * 50)
            
            
    def enviar_alertas_vencimiento(self):
        hoy = datetime.today().date()
        dos_dias_despues = hoy + timedelta(days=2)
    
        # Obtener todos los préstamos
        self.cursor.execute("""
            SELECT usuario, libro, fecha_devolucion
            FROM prestamos
        """)
        prestamos = self.cursor.fetchall()
    
        # Diccionario: usuario → lista de libros con alerta
        alertas_por_usuario = {}
    
        for nombre_usuario, libro, fecha_dev_str in prestamos:
            fecha_dev = datetime.strptime(fecha_dev_str, "%Y-%m-%d").date()
    
            if fecha_dev < hoy:
                estado = "❌ ¡VENCIDO!"
            elif fecha_dev == hoy:
                estado = "⚠️ Vence HOY"
            elif fecha_dev == dos_dias_despues:
                estado = "⏳ Vence en 2 días"
            else:
                continue  # no hay alerta
    
            if nombre_usuario not in alertas_por_usuario:
                alertas_por_usuario[nombre_usuario] = []
    
            alertas_por_usuario[nombre_usuario].append((libro, fecha_dev_str, estado))
    
        # Obtener correos desde la tabla usuarios
        for usuario, prestamos in alertas_por_usuario.items():
            self.cursor.execute("""
                SELECT correo FROM usuarios WHERE nombre_completo = ?
            """, (usuario,))
            resultado = self.cursor.fetchone()
    
            if resultado and resultado[0]:
                correo = resultado[0]
                asunto = "📚 Alerta de vencimiento de préstamo(s)"
                mensaje = f"Hola {usuario},\n\nTienes los siguientes libros con próximos vencimientos o ya vencidos:\n\n"
                for libro, fecha, estado in prestamos:
                    mensaje += f"• '{libro}' → {fecha} → {estado}\n"
                mensaje += "\nPor favor realiza la devolución a tiempo para evitar sanciones.\n\nBiblioteca Escolar 📖"
    
                # Aquí puedes elegir entre impresión o envío real
                # self._enviar_correo_simulado(correo, asunto, mensaje)
                self._enviar_correo_real(correo, asunto, mensaje)  # si configuras SMTP
            else:
                print(f"⚠️ Usuario {usuario} no tiene correo registrado.")
            

    def cerrar(self):
        self.conn.close()