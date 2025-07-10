import tkinter as tk
from tkinter import ttk, messagebox
from autenticacion import UsuarioDB, Usuario
from Libro import LibroDB
from disponibilidad import GestorDisponibilidad
from Prestamo import PrestamoDB

COLOR_FONDO = "#003366"
COLOR_BOTON = "#0055A5"
COLOR_TEXTO = "white"

# Clase principal de la aplicacion
class App:
    def __init__(self):
        # Crea la ventana principal de la aplicación
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Usuarios")  # Título de la ventana
        self.ventana.geometry("500x500")           # Tamaño inicial de la ventana
        self.ventana.configure(bg=COLOR_FONDO)     # Color de fondo definido por constante

        # Instancia la base de datos de usuarios
        self.db = UsuarioDB()

        # Variable para guardar el usuario que ha iniciado sesión (si aplica)
        self.usuario_actual = None

        # Crea un marco (contenedor) principal dentro de la ventana para colocar los elementos gráficos
        self.marco = tk.Frame(self.ventana, bg=COLOR_FONDO)
        self.marco.pack(expand=True, fill="both")  # Hace que el marco ocupe todo el espacio disponible

        # Muestra la pantalla inicial de bienvenida con botones de login y registro
        self.mostrar_inicio()

        # Inicia el bucle principal de la interfaz gráfica (mantiene la ventana abierta)
        self.ventana.mainloop()

    def limpiar_marco(self):
        # Elimina todos los widgets (botones, etiquetas, entradas...) que haya dentro del marco
        for widget in self.marco.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        # Limpia el marco antes de mostrar los nuevos elementos (por si venimos de otra pantalla)
        self.limpiar_marco()

        # Muestra el título del sistema en la parte superior
        tk.Label(self.marco, text="Colegio Nuestra Señora de la Providencia",
                 bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Helvetica", 16, "bold")).pack(pady=(30, 40))

        # Botón para ir a la pantalla de inicio de sesión
        tk.Button(self.marco, text="Iniciar sesión", width=20, bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  font=("Helvetica", 12), command=self.mostrar_login).pack(pady=10)

        # Botón para ir a la pantalla de registro de nuevos usuarios
        tk.Button(self.marco, text="Registrarse", width=20, bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  font=("Helvetica", 12), command=self.mostrar_registro_paso1).pack(pady=10)
        
    #Ventana despues del login que muestra las posibles funcionalidades
    def mostrar_funcionalidades(self):
        # Limpia todos los widgets del marco actual antes de mostrar el contenido nuevo
        self.limpiar_marco()
    
        # Muestra un mensaje de bienvenida con el nombre del usuario actualmente autenticado
        tk.Label(
            self.marco,
            text=f"Bienvenido, {self.usuario_actual.nombre_completo}",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            font=("Helvetica", 14, "bold")
        ).pack(pady=(20, 10))
    
        # ------------------------------
        # BOTONES DE FUNCIONALIDADES
        # ------------------------------
    
        # Botón para mostrar el catálogo de libros disponibles en la biblioteca
        tk.Button(
            self.marco,
            text="Mostrar catálogo",
            width=20,
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            command=self.mostrar_catalogo
        ).pack(pady=5)
    
        # Botón para ver la disponibilidad de horarios (clases, reservas, etc.)
        tk.Button(
            self.marco,
            text="Ver disponibilidad",
            width=20,
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            command=self.mostrar_disponibilidad
        ).pack(pady=5)
    
        # Botón para acceder a la funcionalidad de préstamo de libros
        # Esto abre una nueva ventana donde se podrá buscar y prestar un libro
        tk.Button(
            self.marco,
            text="Prestar libro",
            width=20,
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            command=self.prestamo
        ).pack(pady=5)
    
        # Botón para una funcionalidad futura o aún no implementada (UTILIZAR ESTA PARA SEGUIR ESCALANDO LAS FUNCIONALIDADES)
        tk.Button(
            self.marco,
            text="Funcionalidad 4",
            width=20,
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO
        ).pack(pady=5)
    
        # Botón para cerrar la sesión actual y regresar a la pantalla de inicio
        tk.Button(
            self.marco,
            text="Cerrar sesión",
            bg="red",
            fg="white",
            command=self.mostrar_inicio
        ).pack(pady=(30, 10))

    #Funcionalidad de login
    def mostrar_login(self):
        # Limpia todos los widgets actuales del marco antes de mostrar los elementos del login
        self.limpiar_marco()
    
        # Muestra el título "Iniciar sesión"
        tk.Label(self.marco, text="Iniciar sesión", bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 10))
    
        # Etiqueta y campo de entrada para el nombre completo
        tk.Label(self.marco, text="Nombre completo:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        entry_nombre = tk.Entry(self.marco)
        entry_nombre.pack()
    
        # Etiqueta y campo de entrada para la contraseña
        tk.Label(self.marco, text="Contraseña:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        entry_pass = tk.Entry(self.marco, show="*")
        entry_pass.pack()
    
        # Función interna que se ejecuta al presionar el botón "Ingresar"
        def intentar_login():
            nombre = entry_nombre.get().strip()
            password = entry_pass.get().strip()
    
            usuario = self.db.login(nombre, password)
    
            if usuario:
                if usuario.autenticado.lower() == "si":
                    self.usuario_actual = usuario
                    self.mostrar_funcionalidades()
                else:
                    messagebox.showwarning("Acceso denegado", "Este usuario no está autenticado para ingresar.")
            else:
                messagebox.showerror("Error", "Credenciales inválidas.")
    
        # Botón para iniciar sesión
        tk.Button(self.marco, text="Ingresar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=intentar_login).pack(pady=15)
    
        # Botón para volver al menú principal de inicio
        tk.Button(self.marco, text="Volver", command=self.mostrar_inicio).pack()

    
    #Funcionalidad de registro (primera parte, solo nombre y curso para validar que no exista)
    def mostrar_registro_paso1(self):
        # Limpia el marco antes de mostrar los nuevos elementos
        self.limpiar_marco()
    
        # Título de la primera etapa del registro
        tk.Label(self.marco, text="Registro - Paso 1", bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 10))
    
        # Campo para ingresar el nombre completo
        tk.Label(self.marco, text="Nombre completo:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        entry_nombre = tk.Entry(self.marco)
        entry_nombre.pack()
    
        # Campo para ingresar el curso
        tk.Label(self.marco, text="Curso:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        entry_curso = tk.Entry(self.marco)
        entry_curso.pack()
    
        # Función que valida los datos y pasa al segundo paso del registro
        def validar_y_continuar():
            nombre = entry_nombre.get().strip()  # Elimina espacios
            curso = entry_curso.get().strip()
    
            # Verifica que no haya campos vacíos
            if not nombre or not curso:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
    
            # Verifica si ya existe un usuario con ese nombre y curso
            if self.db.existe_usuario_por_nombre_y_curso(nombre, curso):
                messagebox.showerror("Error", "El usuario ya existe.")
                return
    
            # Si pasa todas las validaciones, continúa al paso 2 del registro
            self.mostrar_registro_paso2(nombre, curso)
    
        # Botón para validar y avanzar al paso 2
        tk.Button(self.marco, text="Siguiente", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=validar_y_continuar).pack(pady=15)
    
        # Botón para volver a la pantalla de inicio
        tk.Button(self.marco, text="Volver", command=self.mostrar_inicio).pack()

    #Funcionalidad de registro despues de la validacion del paso 1
    def mostrar_registro_paso2(self, nombre, curso):
        # Limpia el marco para mostrar el paso 2 del registro
        self.limpiar_marco()
    
        # Título del paso 2
        tk.Label(self.marco, text="Registro - Paso 2", bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 10))
    
        # Muestra los datos ya ingresados en el paso anterior (para verificación)
        tk.Label(self.marco, text=f"Nombre: {nombre}", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        tk.Label(self.marco, text=f"Curso: {curso}", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
    
        # Campo para ingresar correo electrónico
        tk.Label(self.marco, text="Correo electrónico:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        entry_correo = tk.Entry(self.marco)
        entry_correo.pack()
    
        # Campo para ingresar contraseña
        tk.Label(self.marco, text="Contraseña:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        entry_pass = tk.Entry(self.marco, show="*")
        entry_pass.pack()
    
        # Campo para seleccionar rol desde un menú desplegable
        tk.Label(self.marco, text="Rol:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        roles = ["Estudiante", "Docente", "Administrativo"]  # Opciones de rol
        rol_var = tk.StringVar()
        rol_menu = ttk.Combobox(self.marco, textvariable=rol_var, values=roles, state="readonly")
        rol_menu.pack()
        rol_menu.current(0)  # Selecciona "Estudiante" por defecto
    
        # Función que crea el usuario y lo registra en la base de datos
        def registrar():
            correo = entry_correo.get().strip()
            password = entry_pass.get().strip()
            rol = rol_var.get()
    
            # Validaciones
            if not correo or not password:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
    
            # Crea un objeto Usuario con los datos proporcionados (autenticado='no' por defecto)
            usuario = Usuario(
                nombre_completo=nombre,
                password=password,
                curso=curso,
                rol=rol,
                sanciones=0,
                penalizacion=False,
                correo=correo,
                autenticado="no"
            )
    
            # Intenta registrar el usuario en la base de datos
            if self.db.registrar(usuario):
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
                self.mostrar_inicio()  # Redirige al inicio después del registro exitoso
    
        # Botón para registrar al usuario
        tk.Button(self.marco, text="Registrar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=registrar).pack(pady=15)
    
        # Botón para volver al paso 1 del registro
        tk.Button(self.marco, text="Volver", command=self.mostrar_registro_paso1).pack()
    
    
    #Funcionalidad de catalogo
    def mostrar_catalogo(self):
        # Crea una nueva ventana para mostrar el catálogo
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Catálogo de libros")
        ventana.configure(bg=COLOR_FONDO)
        ventana.geometry("600x600")
    
        # Título de la sección
        tk.Label(
            ventana, text="Catálogo de la Biblioteca",
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
    
        # ----------------------
        # Filtros de búsqueda
        # ----------------------
        filtro_frame = tk.Frame(ventana, bg=COLOR_FONDO)
        filtro_frame.pack(pady=(0, 10))
    
        # Campo de texto para buscar por nombre o autor del libro
        tk.Label(filtro_frame, text="Buscar (nombre o autor):",
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=0, padx=5)
        entrada_busqueda = tk.Entry(filtro_frame)
        entrada_busqueda.grid(row=0, column=1, padx=5)
    
        # Menú desplegable para filtrar por categoría
        tk.Label(filtro_frame, text="Filtrar por categoría:",
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=2, padx=5)
        
        # Obtiene todas las categorías únicas de los libros para llenar el menú
        categorias = ["Todas"] + list({libro.categoria for libro in LibroDB().obtener_todos()})
        categoria_var = tk.StringVar(value="Todas")  # Valor por defecto: "Todas"
        categoria_menu = ttk.Combobox(
            filtro_frame, textvariable=categoria_var,
            values=categorias, state="readonly"
        )
        categoria_menu.grid(row=0, column=3, padx=5)
    
        # ----------------------
        # Área con scroll para mostrar resultados
        # ----------------------
        frame_scroll = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_scroll.pack(expand=True, fill="both", padx=10, pady=10)
    
        canvas = tk.Canvas(frame_scroll, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_FONDO)
    
        # Ajusta el scroll del canvas cuando cambia el contenido interno
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
    
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        # ----------------------
        # Función para aplicar los filtros y mostrar resultados
        # ----------------------
        def actualizar_lista():
            # Borra resultados anteriores del scrollable_frame
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
    
            # Obtiene los valores de los campos de búsqueda
            texto_busqueda = entrada_busqueda.get().lower()
            categoria_seleccionada = categoria_var.get()
    
            # Recupera todos los libros desde la base de datos
            libros = LibroDB().obtener_todos()
            filtrados = []
    
            # Aplica los filtros por texto y categoría
            for libro in libros:
                coincide_categoria = (
                    categoria_seleccionada == "Todas" or libro.categoria == categoria_seleccionada
                )
                coincide_busqueda = (
                    texto_busqueda in libro.nombre.lower() or texto_busqueda in libro.autor.lower()
                )
                if coincide_categoria and coincide_busqueda:
                    filtrados.append(libro)
    
            # Si no hay resultados, muestra mensaje
            if not filtrados:
                tk.Label(
                    scrollable_frame, text="No se encontraron libros con ese filtro.",
                    bg=COLOR_FONDO, fg=COLOR_TEXTO
                ).pack(pady=10)
            else:
                # Muestra los libros filtrados con su información
                for libro in filtrados:
                    texto = f"{libro.nombre} | Categoría: {libro.categoria} | Autor: {libro.autor} | Cantidad: {libro.cantidad}"
                    tk.Label(
                        scrollable_frame, text=texto,
                        bg=COLOR_FONDO, fg=COLOR_TEXTO,
                        anchor="w", justify="left", wraplength=560
                    ).pack(anchor="w", padx=5, pady=3)
    
        # Botón para activar el filtrado
        tk.Button(
            filtro_frame, text="🔍 Buscar",
            bg=COLOR_BOTON, fg=COLOR_TEXTO,
            command=actualizar_lista
        ).grid(row=0, column=4, padx=10)
    
        # Muestra la lista completa por defecto al abrir la ventana
        actualizar_lista()

#Funcion de disponibilidad de horarios junto la reserva de los mismos
    def mostrar_disponibilidad(self):
        # Crea una nueva ventana para mostrar la disponibilidad de horarios
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Disponibilidad de horarios")
        ventana.configure(bg=COLOR_FONDO)
        ventana.geometry("550x500")
    
        # Crea una instancia del gestor que maneja las operaciones de disponibilidad
        gestor = GestorDisponibilidad()
    
        # Título principal
        tk.Label(ventana, text="Consultar disponibilidad", bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=("Helvetica", 14, "bold")).pack(pady=10)
    
        # -------------------
        # Sección de filtros
        # -------------------
        frame_opciones = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_opciones.pack(pady=5)
    
        # Campo para ingresar una fecha (opcional)
        tk.Label(frame_opciones, text="Fecha (YYYY-MM-DD):", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=0, padx=5)
        entry_fecha = tk.Entry(frame_opciones)
        entry_fecha.grid(row=0, column=1)
    
        # Campo para ingresar una hora específica (opcional)
        tk.Label(frame_opciones, text="Hora (7-14):", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=1, column=0, padx=5)
        entry_hora = tk.Entry(frame_opciones)
        entry_hora.grid(row=1, column=1)
    
        # -------------------------------
        # Área con scroll para resultados
        # -------------------------------
        frame_scroll = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_scroll.pack(expand=True, fill="both", padx=10, pady=10)
    
        canvas = tk.Canvas(frame_scroll, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_FONDO)
    
        # Hace que el área de scroll se actualice cuando cambia el contenido
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        # ----------------------------------
        # Función que muestra los resultados
        # ----------------------------------
        def mostrar_resultados():
            # Borra cualquier resultado anterior
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
    
            # Toma los valores de los filtros
            fecha = entry_fecha.get().strip()
            hora = entry_hora.get().strip()
    
            resultados = []
    
            # Lógica para aplicar filtros
            if fecha and hora:
                try:
                    hora = int(hora)
                    resultados = gestor.buscar_disponibilidad(fecha=fecha, hora=hora)
                except ValueError:
                    # Si la hora no es válida, muestra un error
                    tk.Label(scrollable_frame, text="⚠️ Hora inválida", bg=COLOR_FONDO, fg="red").pack()
            elif fecha:
                resultados = gestor.buscar_disponibilidad(fecha=fecha)
            elif hora:
                try:
                    hora = int(hora)
                    resultados = gestor.buscar_disponibilidad(hora=hora)
                except ValueError:
                    tk.Label(scrollable_frame, text="⚠️ Hora inválida", bg=COLOR_FONDO, fg="red").pack()
            else:
                # Si no se aplica ningún filtro, muestra todo
                resultados = gestor.buscar_disponibilidad()
    
            # Si no hay resultados disponibles con esos filtros
            if not resultados:
                tk.Label(scrollable_frame, text="❌ No hay disponibilidad con esos filtros.",
                         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=10)
            else:
                # Muestra cada entrada disponible junto con su botón de reserva
                for entrada in resultados:
                    fila = tk.Frame(scrollable_frame, bg=COLOR_FONDO)
                    fila.pack(fill="x", padx=5, pady=3)
    
                    texto = f"{entrada.fecha} a las {entrada.hora}:00 — Disponible"
                    tk.Label(fila, text=texto, bg=COLOR_FONDO, fg=COLOR_TEXTO, anchor="w").pack(side="left", expand=True)
    
                    # Función interna para hacer una reserva de ese horario
                    def hacer_reserva(fecha=entrada.fecha, hora=entrada.hora):
                        # Cambia el estado a "no disponible" y asigna al usuario actual
                        gestor.cursor.execute("""
                            UPDATE disponibilidad
                            SET disponibilidad = 'no', usuario = ?
                            WHERE fecha = ? AND hora = ? AND disponibilidad = 'si'
                        """, (self.usuario_actual.nombre_completo, fecha, hora))
                        gestor.conn.commit()
                        # Muestra mensaje de éxito y actualiza la lista
                        messagebox.showinfo("Reserva exitosa", f"Reservaste {fecha} a las {hora}:00")
                        mostrar_resultados()
    
                    # Botón que permite hacer la reserva
                    tk.Button(fila, text="Reservar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                              command=hacer_reserva).pack(side="right", padx=5)
    
        # Botón que permite aplicar los filtros ingresados
        tk.Button(ventana, text="🔍 Buscar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=mostrar_resultados).pack(pady=5)
    
        # Muestra todos los resultados desde el inicio
        mostrar_resultados()


    def prestamo(self):
        # Crea una nueva ventana para gestionar el préstamo de libros
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Prestar libro")
        ventana.configure(bg=COLOR_FONDO)
        ventana.geometry("600x500")
    
        # Título de la ventana
        tk.Label(ventana, text="Funcionalidad: Prestar libro",
                 bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Helvetica", 16, "bold")).pack(pady=10)
    
        # Se crean instancias de las bases de datos de libros y préstamos
        db_libros = LibroDB()
        db_prestamos = PrestamoDB()
    
        # ---------------------
        # Sección de Filtros
        # ---------------------
        filtro_frame = tk.Frame(ventana, bg=COLOR_FONDO)
        filtro_frame.pack(pady=(0, 10))
    
        # Entrada para buscar por nombre o autor
        tk.Label(filtro_frame, text="Buscar (nombre o autor):", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=0, padx=5)
        entrada_busqueda = tk.Entry(filtro_frame)
        entrada_busqueda.grid(row=0, column=1, padx=5)
    
        # Menú para filtrar por categoría
        tk.Label(filtro_frame, text="Filtrar por categoría:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=2, padx=5)
        categorias = ["Todas"] + list({libro.categoria for libro in db_libros.obtener_todos()})
        categoria_var = tk.StringVar(value="Todas")
        categoria_menu = ttk.Combobox(filtro_frame, textvariable=categoria_var, values=categorias, state="readonly")
        categoria_menu.grid(row=0, column=3, padx=5)
    
        # ------------------------------
        # Área con scroll para resultados
        # ------------------------------
        frame_scroll = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_scroll.pack(expand=True, fill="both", padx=10, pady=10)
    
        canvas = tk.Canvas(frame_scroll, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_FONDO)
    
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        # -----------------------------
        # Función para prestar un libro
        # -----------------------------
        def prestar_libro(libro):
            # Valida que el curso del usuario sea numérico
            try:
                curso_num = int(self.usuario_actual.curso)
            except ValueError:
                messagebox.showerror("Error", "El curso del usuario no es válido.")
                return
    
            # Solo se permite prestar libros si el curso es mayor a 5
            if curso_num <= 5:
                messagebox.showwarning("⛔ No autorizado", "Solo los cursos superiores a 5 pueden realizar préstamos.")
                return
    
            # Valida que el usuario no tenga más de 3 sanciones
            if self.usuario_actual.sanciones > 3:
                messagebox.showwarning("⛔ No autorizado", "Tienes más de 3 sanciones. No puedes realizar préstamos.")
                return
    
            # Verifica que haya ejemplares disponibles del libro
            if libro.cantidad <= 0:
                messagebox.showwarning("⛔ No disponible", "No hay ejemplares disponibles de este libro.")
                return
    
            # Registra el préstamo en la base de datos
            fecha_devolucion = db_prestamos.realizar_prestamo(self.usuario_actual, libro)
    
            # Resta 1 a la cantidad del libro prestado
            db_libros.restar_cantidad(libro.nombre)
    
            # Muestra mensaje de éxito
            messagebox.showinfo("✅ Préstamo realizado", f"Devuelve el libro antes del {fecha_devolucion}.")
    
            # Actualiza la lista para reflejar los cambios
            actualizar_lista()
    
        # -----------------------------------------
        # Función para actualizar la lista de libros
        # -----------------------------------------
        def actualizar_lista():
            # Elimina cualquier resultado anterior en el área scrollable
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
    
            # Toma los valores de los filtros ingresados
            texto_busqueda = entrada_busqueda.get().lower()
            categoria_seleccionada = categoria_var.get()
    
            # Se obtienen todos los libros disponibles
            libros = db_libros.obtener_todos()
            filtrados = []
    
            for libro in libros:
                if libro.cantidad <= 0:
                    continue  # No mostrar libros sin disponibilidad
    
                coincide_categoria = (categoria_seleccionada == "Todas" or libro.categoria == categoria_seleccionada)
                coincide_busqueda = (texto_busqueda in libro.nombre.lower() or texto_busqueda in libro.autor.lower())
    
                if coincide_categoria and coincide_busqueda:
                    filtrados.append(libro)
    
            # Muestra mensaje si no hay resultados
            if not filtrados:
                tk.Label(scrollable_frame, text="❌ No se encontraron libros disponibles.",
                         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=10)
            else:
                # Muestra cada libro disponible junto a su botón de préstamo
                for libro in filtrados:
                    texto = f"{libro.nombre} | Categoría: {libro.categoria} | Autor: {libro.autor} | Cantidad: {libro.cantidad}"
                    frame_libro = tk.Frame(scrollable_frame, bg=COLOR_FONDO)
                    frame_libro.pack(fill="x", pady=5, padx=5)
    
                    # Etiqueta con información del libro
                    tk.Label(frame_libro, text=texto, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                             anchor="w", justify="left", wraplength=450).pack(side="left", fill="x", expand=True)
    
                    # Botón para realizar el préstamo
                    tk.Button(frame_libro, text="📚 Prestar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                              command=lambda l=libro: prestar_libro(l)).pack(side="right")
    
        # Botón para ejecutar la búsqueda y actualizar la lista de libros mostrados
        tk.Button(filtro_frame, text="🔍 Buscar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=actualizar_lista).grid(row=0, column=4, padx=10)
    
        # Mostrar la lista por defecto al abrir la ventana
        actualizar_lista()


if __name__ == "__main__":
    App()
    

    

