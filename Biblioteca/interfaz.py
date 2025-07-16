import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from autenticacion import UsuarioDB, Usuario
from Libro import LibroDB, Libro
from disponibilidad import GestorDisponibilidad
from Prestamo import PrestamoDB
from Catalogo import Catalogo
from PIL import Image, ImageTk
import os

COLOR_FONDO = "#2A683A"
COLOR_BOTON = "#fcb900"
COLOR_TEXTO = "black"

# Clase principal de la aplicacion
class App:
    def __init__(self):
        # Crea la ventana principal de la aplicación
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Usuarios")  # Título de la ventana
        self.ventana.geometry("1000x1000")           # Tamaño inicial de la ventana
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
        self.limpiar_marco()
    
        # Título
        tk.Label(self.marco, text="Colegio Nuestra Señora de la Providencia",
                 bg=COLOR_FONDO, fg="white", font=("Helvetica", 16, "bold")).pack(pady=(30, 10))

        ruta_absoluta = os.path.join(os.path.dirname(__file__), "Recursos", "logo.png")
        imagen = Image.open(ruta_absoluta)
        imagen = imagen.resize((200, 200), Image.Resampling.LANCZOS)  # Opcional: redimensionar
        self.logo_img = ImageTk.PhotoImage(imagen)  # Guarda la referencia para evitar que se borre
    
        # Mostrar imagen
        tk.Label(self.marco, image=self.logo_img, bg=COLOR_FONDO).pack(pady=(0, 30))
    
        # Botón de login
        tk.Button(self.marco, text="Iniciar sesión", width=20, bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  font=("Helvetica", 12), command=self.mostrar_login).pack(pady=10)
    
        # Botón de registro
        tk.Button(self.marco, text="Registrarse", width=20, bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  font=("Helvetica", 12), command=self.mostrar_registro_paso1).pack(pady=10)
        
    def mostrar_funcionalidades(self):
        self.limpiar_marco()
    
        # Contenedor principal que ocupa todo el espacio
        contenedor = tk.Frame(self.marco, bg=COLOR_FONDO)
        contenedor.place(relx=0, rely=0, relwidth=1, relheight=1)  # 100% ancho y alto
    
        # Marco izquierdo para funcionalidades
        marco_izquierdo = tk.Frame(contenedor, bg=COLOR_FONDO)
        marco_izquierdo.place(relx=0, rely=0, relwidth=0.66, relheight=1)
    
        # Marco derecho para visualización de préstamos
        marco_derecho = tk.Frame(contenedor, bg=COLOR_FONDO, highlightbackground="black", highlightthickness=1)
        marco_derecho.place(relx=0.66, rely=0, relwidth=0.34, relheight=1)
    
        # Submarco centrado dentro del marco izquierdo
        centro = tk.Frame(marco_izquierdo, bg=COLOR_FONDO)
        centro.place(relx=0.5, rely=0.5, anchor="center")
    
        # Mensaje de bienvenida
        tk.Label(
            centro,
            text=f"Bienvenido, {self.usuario_actual.nombre_completo}",
            bg=COLOR_FONDO,
            fg="white",
            font=("Helvetica", 14, "bold")
        ).pack(pady=(0, 10))

        ruta_absoluta = os.path.join(os.path.dirname(__file__), "Recursos", "logo.png")
        imagen_original = Image.open(ruta_absoluta)
        imagen_redimensionada = imagen_original.resize((200, 200))  # Ajusta tamaño si deseas
        self.logo_imagen = ImageTk.PhotoImage(imagen_redimensionada)  # Guardar referencia

        tk.Label(centro, image=self.logo_imagen, bg=COLOR_FONDO).pack(pady=(0, 20))
    
        # Botones comunes a todos los roles
        botones = [
            ("Mostrar catálogo", self.mostrar_catalogo),
            ("Ver disponibilidad", self.mostrar_disponibilidad),
            ("Prestar libro", self.prestamo),
            ("Funcionalidad 4", lambda: None),
            ("Cerrar sesión", self.mostrar_inicio)
        ]

        # --------------------------
        # Botones solo para ADMINISTRATIVO
        # --------------------------
        if self.usuario_actual.rol == "Administrativo":
            tk.Button(
                centro,
                text="Visualizar préstamos",
                width=25,
                bg=COLOR_BOTON,
                fg=COLOR_TEXTO,
                command=self.prestamos_administrativo
            ).pack(pady=7)
    
            tk.Button(
                centro,
                text="Registrar usuario",
                width=25,
                bg=COLOR_BOTON,
                fg=COLOR_TEXTO,
                command=self.registrar_administrativo
            ).pack(pady=7)
    
        for texto, comando in botones:
            tk.Button(
                centro,
                text=texto,
                width=25,
                bg=COLOR_BOTON if texto != "Cerrar sesión" else "red",
                fg=COLOR_TEXTO if texto != "Cerrar sesión" else "white",
                command=comando
            ).pack(pady=7)
    
        # Mostrar los préstamos actuales en el marco derecho
        self.visualizar_prestamos(marco_derecho)
    


    #Funcionalidad de login
    def mostrar_login(self):
        # Limpia todos los widgets actuales del marco antes de mostrar los elementos del login
        self.limpiar_marco()
    
        # Muestra el título "Iniciar sesión"
        tk.Label(self.marco, text="Iniciar sesión", bg=COLOR_FONDO, fg="white",
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 10))

        ruta_absoluta = os.path.join(os.path.dirname(__file__), "Recursos", "logo.png")
        imagen = Image.open(ruta_absoluta)
        imagen = imagen.resize((200, 200), Image.Resampling.LANCZOS)  # Opcional: redimensionar
        self.logo_img = ImageTk.PhotoImage(imagen)  # Guarda la referencia para evitar que se borre
    
        # Mostrar imagen
        tk.Label(self.marco, image=self.logo_img, bg=COLOR_FONDO).pack(pady=(0, 30))
    
        # Etiqueta y campo de entrada para el nombre completo
        tk.Label(self.marco, text="Nombre completo:", bg=COLOR_FONDO, fg="white").pack()
        entry_nombre = tk.Entry(self.marco, fg="gray")
        entry_nombre.insert(0, "Escribe tu nombre completo")
        entry_nombre.pack()
    
        entry_nombre.bind("<FocusIn>", lambda e: self._borrar_placeholder(entry_nombre, "Escribe tu nombre completo"))
        entry_nombre.bind("<FocusOut>", lambda e: self._restaurar_placeholder(entry_nombre, "Escribe tu nombre completo"))
    
        # Etiqueta y campo de entrada para la contraseña
        tk.Label(self.marco, text="Contraseña:", bg=COLOR_FONDO, fg="white").pack()
        entry_pass = tk.Entry(self.marco, fg="gray")
        entry_pass.insert(0, "Escribe tu contraseña")
        entry_pass.pack()
    
        def ocultar_password(event):
            if entry_pass.get() == "Escribe tu contraseña":
                entry_pass.delete(0, "end")
                entry_pass.config(fg="black", show="*")
    
        def mostrar_placeholder_password(event):
            if entry_pass.get() == "":
                entry_pass.insert(0, "Escribe tu contraseña")
                entry_pass.config(fg="gray", show="")
    
        entry_pass.bind("<FocusIn>", ocultar_password)
        entry_pass.bind("<FocusOut>", mostrar_placeholder_password)
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
                    messagebox.showwarning("Acceso denegado", "Este usuario aun no está autenticado para ingresar.")
            else:
                messagebox.showerror("Error", "Credenciales inválidas.")
    
        # Botón para iniciar sesión
        tk.Button(self.marco, text="Ingresar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=intentar_login).pack(pady=15)
    
        # Botón para volver al menú principal de inicio
        tk.Button(self.marco, text="Volver", command=self.mostrar_inicio).pack()

    
    #Funcionalidad de registro (primera parte, solo nombre y curso para validar que no exista)
    def mostrar_registro_paso1(self):
        self.limpiar_marco()
    
        tk.Label(self.marco, text="Registro - Paso 1", bg=COLOR_FONDO, fg="white",
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 10))
        
        ruta_absoluta = os.path.join(os.path.dirname(__file__), "Recursos", "logo.png")
        imagen = Image.open(ruta_absoluta)
        imagen = imagen.resize((200, 200), Image.Resampling.LANCZOS)  # Opcional: redimensionar
        self.logo_img = ImageTk.PhotoImage(imagen)  # Guarda la referencia para evitar que se borre
    
        # Mostrar imagen
        tk.Label(self.marco, image=self.logo_img, bg=COLOR_FONDO).pack(pady=(0, 30))
    
        # ----------------------------
        # Entry: Nombre completo
        # ----------------------------
        tk.Label(self.marco, text="Nombre completo:", bg=COLOR_FONDO, fg="white").pack()
        entry_nombre = tk.Entry(self.marco, fg="gray")
        entry_nombre.insert(0, "Escribe tu nombre completo")
        entry_nombre.pack()
    
        entry_nombre.bind("<FocusIn>", lambda e: self._borrar_placeholder(entry_nombre, "Escribe tu nombre completo"))
        entry_nombre.bind("<FocusOut>", lambda e: self._restaurar_placeholder(entry_nombre, "Escribe tu nombre completo"))
    
        # ----------------------------
        # Entry: Curso
        # ----------------------------
        tk.Label(self.marco, text="Curso:", bg=COLOR_FONDO, fg="white").pack()
        entry_curso = tk.Entry(self.marco, fg="gray")
        entry_curso.insert(0, "Ej: 10A, 11B")
        entry_curso.pack()
    
        entry_curso.bind("<FocusIn>", lambda e: self._borrar_placeholder(entry_curso, "Ej: 10A, 11B"))
        entry_curso.bind("<FocusOut>", lambda e: self._restaurar_placeholder(entry_curso, "Ej: 10A, 11B"))
    
        def validar_y_continuar():
            nombre = entry_nombre.get().strip()
            curso = entry_curso.get().strip()
    
            if nombre in ("", "Escribe tu nombre completo") or curso in ("", "Ej: 10A, 11B"):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
    
            if self.db.existe_usuario_por_nombre_y_curso(nombre, curso):
                messagebox.showerror("Error", "El usuario ya existe.")
                return
    
            self.mostrar_registro_paso2(nombre, curso)
    
        tk.Button(self.marco, text="Siguiente", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=validar_y_continuar).pack(pady=15)
    
        tk.Button(self.marco, text="Volver", command=self.mostrar_inicio).pack()

    def mostrar_registro_paso2(self, nombre, curso):
        self.limpiar_marco()
    
        tk.Label(self.marco, text="Registro - Paso 2", bg=COLOR_FONDO, fg="white",
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 10))
        
        ruta_absoluta = os.path.join(os.path.dirname(__file__), "Recursos", "logo.png")
        imagen = Image.open(ruta_absoluta)
        imagen = imagen.resize((200, 200), Image.Resampling.LANCZOS)  # Opcional: redimensionar
        self.logo_img = ImageTk.PhotoImage(imagen)  # Guarda la referencia para evitar que se borre
    
        # Mostrar imagen
        tk.Label(self.marco, image=self.logo_img, bg=COLOR_FONDO).pack(pady=(0, 30))
    
        tk.Label(self.marco, text=f"Nombre: {nombre}", bg=COLOR_FONDO, fg="white").pack()
        tk.Label(self.marco, text=f"Curso: {curso}", bg=COLOR_FONDO, fg="white").pack()
    
        # ----------------------------
        # Entry: Correo electrónico
        # ----------------------------
        tk.Label(self.marco, text="Correo electrónico:", bg=COLOR_FONDO, fg="white").pack()
        entry_correo = tk.Entry(self.marco, fg="gray")
        entry_correo.insert(0, "ejemplo@correo.com")
        entry_correo.pack()
    
        entry_correo.bind("<FocusIn>", lambda e: self._borrar_placeholder(entry_correo, "ejemplo@correo.com"))
        entry_correo.bind("<FocusOut>", lambda e: self._restaurar_placeholder(entry_correo, "ejemplo@correo.com"))
    
        # ----------------------------
        # Entry: Contraseña
        # ----------------------------
        tk.Label(self.marco, text="Contraseña:", bg=COLOR_FONDO, fg="white").pack()
        entry_pass = tk.Entry(self.marco, fg="gray")
        entry_pass.insert(0, "Escribe tu contraseña")
        entry_pass.pack()
    
        def ocultar_password(event):
            if entry_pass.get() == "Escribe tu contraseña":
                entry_pass.delete(0, "end")
                entry_pass.config(fg="black", show="*")
    
        def mostrar_placeholder_password(event):
            if entry_pass.get() == "":
                entry_pass.insert(0, "Escribe tu contraseña")
                entry_pass.config(fg="gray", show="")
    
        entry_pass.bind("<FocusIn>", ocultar_password)
        entry_pass.bind("<FocusOut>", mostrar_placeholder_password)
    
        # ----------------------------
        # ComboBox: Rol
        # ----------------------------
        tk.Label(self.marco, text="Rol:", bg=COLOR_FONDO, fg="white").pack()
        roles = ["Estudiante", "Docente", "Administrativo"]
        rol_var = tk.StringVar()
        rol_menu = ttk.Combobox(self.marco, textvariable=rol_var, values=roles, state="readonly")
        rol_menu.pack()
        rol_menu.current(0)
    
        def registrar():
            correo = entry_correo.get().strip()
            password = entry_pass.get().strip()
            rol = rol_var.get()
    
            if correo in ("", "ejemplo@correo.com") or password in ("", "Escribe tu contraseña"):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
    
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
    
            if self.db.registrar(usuario):
                messagebox.showinfo("Éxito", "Usuario registrado correctamente. Está en espera de autenticación.")
                self.mostrar_inicio()
    
        tk.Button(self.marco, text="Registrar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=registrar).pack(pady=15)
    
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
            bg=COLOR_FONDO, fg="white",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
    
        # ----------------------
        # Filtros de búsqueda
        # ----------------------
        filtro_frame = tk.Frame(ventana, bg=COLOR_FONDO)
        filtro_frame.pack(pady=(0, 10))
    
        # Campo de texto para buscar por nombre o autor del libro
        tk.Label(filtro_frame, text="Buscar (nombre o autor):",
                 bg=COLOR_FONDO, fg="white").grid(row=0, column=0, padx=5)
        entrada_busqueda = tk.Entry(filtro_frame)
        entrada_busqueda.grid(row=0, column=1, padx=5)
    
        # Menú desplegable para filtrar por categoría
        tk.Label(filtro_frame, text="Filtrar por categoría:",
                 bg=COLOR_FONDO, fg="white").grid(row=0, column=2, padx=5)
        
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
                    bg=COLOR_FONDO, fg="white"
                ).pack(pady=10)
            else:
                # Muestra los libros filtrados con su información
                for libro in filtrados:
                    frame_libro = tk.Frame(scrollable_frame, bg=COLOR_FONDO)
                    frame_libro.pack(fill="x", pady=2)
                
                    info = f"{libro.nombre} | Categoría: {libro.categoria} | Autor: {libro.autor} | Cantidad: {libro.cantidad}"
                    tk.Label(frame_libro, text=info, bg=COLOR_FONDO, fg="white", anchor="w", justify="left").pack(side="left", padx=5)
                
                    if self.usuario_actual.rol == "Administrativo":
                        def eliminar_libro(nombre=libro.nombre):
                            respuesta = messagebox.askyesno("Confirmar", f"¿Deseas eliminar '{nombre}' definitivamente?")
                            if respuesta:
                                db_libro = LibroDB()
                                db_libro.cursor.execute("DELETE FROM libros WHERE nombre = ?", (nombre,))
                                db_libro.conn.commit()
                                actualizar_lista()
                        def modificar_cantidad(delta, nombre_libro):
                            db_libros = LibroDB()
                            if delta == 1:
                                db_libros.sumar_cantidad(nombre_libro)
                            elif delta == -1:
                                db_libros.restar_cantidad(nombre_libro)
                            actualizar_lista()

                        tk.Button(frame_libro, text="Eliminar libro", bg="red", fg="white", command=eliminar_libro).pack(side="right", padx=2)

                        tk.Button(frame_libro, text="Restar cantidad (-1)", bg="orange", fg="white",
                                command=lambda nombre=libro.nombre: modificar_cantidad(-1, nombre)).pack(side="right", padx=2)
                        
                        tk.Button(frame_libro, text="Sumar cantidad (+1)", bg="green", fg="white",
                                command=lambda nombre=libro.nombre: modificar_cantidad(1, nombre)).pack(side="right", padx=2)

    
        # Botón para activar el filtrado
        tk.Button(
            filtro_frame, text="🔍 Buscar",
            bg=COLOR_BOTON, fg=COLOR_TEXTO,
            command=actualizar_lista
        ).grid(row=0, column=4, padx=10)
    
        # Muestra la lista completa por defecto al abrir la ventana
        actualizar_lista()

        if self.usuario_actual.rol == "Administrativo":
            def abrir_agregar_libro():
                ventana_nuevo = tk.Toplevel(ventana)
                ventana_nuevo.title("Agregar nuevo libro")
                ventana_nuevo.geometry("400x400")
                ventana_nuevo.configure(bg=COLOR_FONDO)
        
                tk.Label(ventana_nuevo, text="Nombre:", bg=COLOR_FONDO, fg="white").pack(pady=5)
                entry_nombre = tk.Entry(ventana_nuevo)
                entry_nombre.pack()
        
                tk.Label(ventana_nuevo, text="Autor:", bg=COLOR_FONDO, fg="white").pack(pady=5)
                entry_autor = tk.Entry(ventana_nuevo)
                entry_autor.pack()
        
                tk.Label(ventana_nuevo, text="Categoría:", bg=COLOR_FONDO, fg="white").pack(pady=5)
                entry_categoria = tk.Entry(ventana_nuevo)
                entry_categoria.pack()
        
                tk.Label(ventana_nuevo, text="Cantidad:", bg=COLOR_FONDO, fg="white").pack(pady=5)
                entry_cantidad = tk.Entry(ventana_nuevo)
                entry_cantidad.pack()
        
                def registrar_libro():
                    nombre = entry_nombre.get().strip()
                    autor = entry_autor.get().strip()
                    categoria = entry_categoria.get().strip()
                    try:
                        cantidad = int(entry_cantidad.get().strip())
                    except ValueError:
                        messagebox.showerror("Error", "La cantidad debe ser un número.")
                        return
                
                    if not nombre or not autor or not categoria or cantidad < 0:
                        messagebox.showerror("Error", "Todos los campos son obligatorios y la cantidad no puede ser negativa.")
                        return
                
                    db_libros = LibroDB()
                    if db_libros.existe_libro(nombre):
                        messagebox.showerror("Error", f"Ya existe un libro registrado con el nombre '{nombre}'.")
                        return
                
                    nuevo_libro = Libro(nombre=nombre, autor=autor, categoria=categoria, cantidad=cantidad)
                    if db_libros.registrar(nuevo_libro):
                        messagebox.showinfo("Éxito", "Libro agregado correctamente.")
                        ventana_nuevo.destroy()
                        actualizar_lista()
                    else:
                        messagebox.showerror("Error", "Error al registrar el libro.")
                
                        
                tk.Button(ventana_nuevo, text="Agregar libro", bg=COLOR_BOTON, fg=COLOR_TEXTO, command=registrar_libro).pack(pady=20)
        
            tk.Button(ventana, text="➕ Agregar nuevo libro", bg="blue", fg="white", command=abrir_agregar_libro).pack(pady=5)


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
        tk.Label(ventana, text="Consultar disponibilidad", bg=COLOR_FONDO, fg="white",
                 font=("Helvetica", 14, "bold")).pack(pady=10)
    
        # -------------------
        # Sección de filtros
        # -------------------
        frame_opciones = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_opciones.pack(pady=5)
    
        # Campo para ingresar una fecha (opcional)
        tk.Label(frame_opciones, text="Fecha (YYYY-MM-DD):", bg=COLOR_FONDO, fg="white").grid(row=0, column=0, padx=5)
        entry_fecha = tk.Entry(frame_opciones)
        entry_fecha.grid(row=0, column=1)
    
        # Campo para ingresar una hora específica (opcional)
        tk.Label(frame_opciones, text="Hora (7-14):", bg=COLOR_FONDO, fg="white").grid(row=1, column=0, padx=5)
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
                         bg=COLOR_FONDO, fg="white").pack(pady=10)
            else:
                # Muestra cada entrada disponible junto con su botón de reserva
                for entrada in resultados:
                    fila = tk.Frame(scrollable_frame, bg=COLOR_FONDO)
                    fila.pack(fill="x", padx=5, pady=3)
    
                    texto = f"{entrada.fecha} a las {entrada.hora}:00 — Disponible"
                    tk.Label(fila, text=texto, bg=COLOR_FONDO, fg="white", anchor="w").pack(side="left", expand=True)
    
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
                 bg=COLOR_FONDO, fg="white", font=("Helvetica", 16, "bold")).pack(pady=10)
    
        # Se crean instancias de las bases de datos de libros y préstamos
        db_libros = LibroDB()
        db_prestamos = PrestamoDB()
    
        # ---------------------
        # Sección de Filtros
        # ---------------------
        filtro_frame = tk.Frame(ventana, bg=COLOR_FONDO)
        filtro_frame.pack(pady=(0, 10))
    
        # Entrada para buscar por nombre o autor
        tk.Label(filtro_frame, text="Buscar (nombre o autor):", bg=COLOR_FONDO, fg="white").grid(row=0, column=0, padx=5)
        entrada_busqueda = tk.Entry(filtro_frame)
        entrada_busqueda.grid(row=0, column=1, padx=5)
    
        # Menú para filtrar por categoría
        tk.Label(filtro_frame, text="Filtrar por categoría:", bg=COLOR_FONDO, fg="white").grid(row=0, column=2, padx=5)
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
                         bg=COLOR_FONDO, fg="white").pack(pady=10)
            else:
                # Muestra cada libro disponible junto a su botón de préstamo
                for libro in filtrados:
                    texto = f"{libro.nombre} | Categoría: {libro.categoria} | Autor: {libro.autor} | Cantidad: {libro.cantidad}"
                    frame_libro = tk.Frame(scrollable_frame, bg=COLOR_FONDO)
                    frame_libro.pack(fill="x", pady=5, padx=5)
    
                    # Etiqueta con información del libro
                    tk.Label(frame_libro, text=texto, bg=COLOR_FONDO, fg="white",
                             anchor="w", justify="left", wraplength=450).pack(side="left", fill="x", expand=True)
    
                    # Botón para realizar el préstamo
                    tk.Button(frame_libro, text="📚 Prestar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                              command=lambda l=libro: prestar_libro(l)).pack(side="right")
    
        # Botón para ejecutar la búsqueda y actualizar la lista de libros mostrados
        tk.Button(filtro_frame, text="🔍 Buscar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=actualizar_lista).grid(row=0, column=4, padx=10)
    
        # Mostrar la lista por defecto al abrir la ventana
        actualizar_lista()

    def visualizar_prestamos(self, marco_derecho):
        for widget in marco_derecho.winfo_children():
            widget.destroy()
    
        marco_derecho.config(
            bg=COLOR_FONDO,
            highlightbackground="black",
            highlightthickness=2
        )
    
        contenedor = tk.Frame(marco_derecho, bg=COLOR_FONDO)
        contenedor.pack(fill="both", expand=True)
    
        tk.Label(
            contenedor,
            text="📚 Préstamos actuales",
            bg=COLOR_FONDO,
            fg="white",
            font=("Helvetica", 14, "bold")
        ).pack(pady=(10, 5), fill="x")
    
        frame_scroll = tk.Frame(contenedor, bg=COLOR_FONDO)
        frame_scroll.pack(fill="both", expand=True)
    
        canvas = tk.Canvas(frame_scroll, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_FONDO)
    
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        db_prestamos = PrestamoDB()
        db_prestamos.cursor.execute("""
            SELECT id, libro, fecha_prestamo, fecha_devolucion, estado_devolucion, estado_prestamo
            FROM prestamos
            WHERE usuario = ?
        """, (self.usuario_actual.nombre_completo,))
        prestamos = db_prestamos.cursor.fetchall()
    
        if not prestamos:
            tk.Label(
                scrollable_frame,
                text="No tienes préstamos activos.",
                bg=COLOR_FONDO,
                fg="white"
            ).pack(pady=20)
            return
    
        for id_prestamo, libro, fecha_prestamo, fecha_devolucion, estado_dev, estado_pres in prestamos:
            frame_prestamo = tk.Frame(scrollable_frame, bg=COLOR_FONDO, relief="groove", borderwidth=1)
            frame_prestamo.pack(fill="x", expand=True, padx=5, pady=5)
    
            info = (
                f"Título: {libro}\n"
                f"Fecha préstamo: {fecha_prestamo}\n"
                f"Fecha devolución: {fecha_devolucion}\n"
                f"Estado del préstamo: {estado_pres.capitalize()}\n"
                f"Estado de devolución: {estado_dev.capitalize()}"
            )
    
            tk.Label(
                frame_prestamo,
                text=info,
                bg=COLOR_FONDO,
                fg="white",
                anchor="w",
                justify="left",
                padx=10,
                pady=5
            ).pack(side="left", fill="both", expand=True)
    
            # Botón para devolver (si estado de devolución es pendiente)
            if estado_dev == "pendiente":
                def solicitar_devolucion(id=id_prestamo):
                    db_prestamos.cursor.execute("""
                        UPDATE prestamos SET estado_devolucion = 'solicitada'
                        WHERE id = ?
                    """, (id,))
                    db_prestamos.conn.commit()
                    self.visualizar_prestamos(marco_derecho)
    
                tk.Button(
                    frame_prestamo,
                    text="Devolver",
                    bg=COLOR_BOTON,
                    fg="black",
                    command=solicitar_devolucion
                ).pack(side="right", padx=10, pady=10)
    
            # Botón para cancelar solicitud (si aún está en estado "solicitado")
            if estado_pres == "solicitado":
                def cancelar_solicitud(id=id_prestamo):
                    db_prestamos.cursor.execute("DELETE FROM prestamos WHERE id = ?", (id,))
                    db_prestamos.conn.commit()
                    self.visualizar_prestamos(marco_derecho)
    
                tk.Button(
                    frame_prestamo,
                    text="Cancelar solicitud",
                    bg="red",
                    fg="white",
                    command=cancelar_solicitud
                ).pack(side="right", padx=10, pady=10)
    
    def prestamos_administrativo(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Administrar préstamos")
        ventana.geometry("750x550")
        ventana.configure(bg=COLOR_FONDO)
    
        tk.Label(
            ventana,
            text="📥 Gestión de préstamos",
            bg=COLOR_FONDO,
            fg="white",
            font=("Helvetica", 14, "bold")
        ).pack(pady=10)
    
        # ---- Filtros ----
        frame_filtros = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_filtros.pack(pady=5)
    
        tk.Label(frame_filtros, text="📚 Libro:", bg=COLOR_FONDO, fg="white").grid(row=0, column=0, padx=5)
        entry_libro = tk.Entry(frame_filtros)
        entry_libro.grid(row=0, column=1, padx=5)
    
        tk.Label(frame_filtros, text="👤 Usuario:", bg=COLOR_FONDO, fg="white").grid(row=0, column=2, padx=5)
        entry_usuario = tk.Entry(frame_filtros)
        entry_usuario.grid(row=0, column=3, padx=5)
    
        frame_scroll = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_scroll.pack(fill="both", expand=True)
    
        canvas = tk.Canvas(frame_scroll, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_FONDO)
    
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        db_prestamos = PrestamoDB()
        db_libros = LibroDB()
        db_usuarios = UsuarioDB()
    
        def cargar_prestamos():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
    
            libro_filtro = entry_libro.get().strip().lower()
            usuario_filtro = entry_usuario.get().strip().lower()
    
            # Traer todos los préstamos incluyendo estado_prestamo
            db_prestamos.cursor.execute("""
                SELECT id, usuario, libro, fecha_prestamo, fecha_devolucion, estado_devolucion, estado_prestamo
                FROM prestamos
                ORDER BY fecha_prestamo DESC
            """)
            prestamos = db_prestamos.cursor.fetchall()
            
            # Aplicar filtros
            prestamos_filtrados = []
            for prestamo in prestamos:
                _, usuario, libro, _, _, _, _ = prestamo
                if libro_filtro and libro_filtro not in libro.lower():
                    continue
                if usuario_filtro and usuario_filtro not in usuario.lower():
                    continue
                prestamos_filtrados.append(prestamo)
            
            if not prestamos_filtrados:
                tk.Label(scrollable_frame, text="No hay préstamos que coincidan con los filtros.",
                         bg=COLOR_FONDO, fg="white").pack(pady=20)
                return
            
            for id_prestamo, usuario, libro, fecha_prestamo, fecha_devolucion, estado_dev, estado_pres in prestamos_filtrados:
                frame = tk.Frame(scrollable_frame, bg=COLOR_FONDO, relief="groove", borderwidth=1)
                frame.pack(fill="x", padx=10, pady=5)
            
                texto = (
                    f"Usuario: {usuario}\n"
                    f"Libro: {libro}\n"
                    f"Fecha préstamo: {fecha_prestamo}\n"
                    f"Fecha devolución: {fecha_devolucion}\n"
                    f"Estado del préstamo: {estado_pres.capitalize()}\n"
                    f"Estado de devolución: {estado_dev.capitalize()}"
                )
            
                tk.Label(frame, text=texto, bg=COLOR_FONDO, fg="white",
                         anchor="w", justify="left", padx=10, pady=5).pack(side="left", fill="both", expand=True)
            
                botones = tk.Frame(frame, bg=COLOR_FONDO)
                botones.pack(side="right", padx=5, pady=5)
            
                # Si es una solicitud de préstamo
                if estado_pres == "solicitado":
                    def aprobar_prestamo(id=id_prestamo):
                        db_prestamos.cursor.execute("""
                            UPDATE prestamos SET estado_prestamo = 'activo'
                            WHERE id = ?
                        """, (id,))
                        db_prestamos.conn.commit()
                        messagebox.showinfo("Aprobado", "Préstamo aprobado.")
                        cargar_prestamos()
            
                    def rechazar_prestamo(id=id_prestamo):
                        db_prestamos.cursor.execute("DELETE FROM prestamos WHERE id = ?", (id,))
                        db_prestamos.conn.commit()
                        messagebox.showinfo("Rechazado", "Préstamo rechazado y eliminado.")
                        cargar_prestamos()
            
                    tk.Button(botones, text="Aprobar préstamo", bg="#3A7CA5", fg="white", command=aprobar_prestamo).pack(pady=2)
                    tk.Button(botones, text="Rechazar solicitud", bg="#FFA500", fg="black", command=rechazar_prestamo).pack(pady=2)
            
                # Si es una solicitud de devolución
                if estado_dev == "solicitada":
                    def aceptar_devolucion(id=id_prestamo, libro_nombre=libro):
                        db_prestamos.cursor.execute("DELETE FROM prestamos WHERE id = ?", (id,))
                        db_prestamos.conn.commit()
                        db_libros.cursor.execute("""
                            UPDATE libros SET cantidad = cantidad + 1
                            WHERE nombre = ?
                        """, (libro_nombre,))
                        db_libros.conn.commit()
                        messagebox.showinfo("Éxito", f"Devolución de '{libro_nombre}' aceptada.")
                        cargar_prestamos()
            
                    def rechazar_devolucion(id=id_prestamo, usuario_nombre=usuario):
                        db_usuarios.cursor.execute("""
                            UPDATE usuarios SET sanciones = sanciones + 1
                            WHERE nombre_completo = ?
                        """, (usuario_nombre,))
                        db_usuarios.conn.commit()
                        nueva_fecha = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
                        db_prestamos.cursor.execute("""
                            UPDATE prestamos
                            SET estado_devolucion = 'pendiente',
                                fecha_devolucion = ?
                            WHERE id = ?
                        """, (nueva_fecha, id))
                        db_prestamos.conn.commit()
                        messagebox.showinfo("Rechazado", f"Devolución rechazada. Nueva fecha: {nueva_fecha}")
                        cargar_prestamos()
            
                    tk.Button(botones, text="Aceptar devolución ✅", bg="green", fg="white", command=aceptar_devolucion).pack(pady=2)
                    tk.Button(botones, text="Rechazar devolución ❌", bg="red", fg="white", command=rechazar_devolucion).pack(pady=2)
            
    
        # Botón para aplicar filtros
        tk.Button(
            frame_filtros,
            text="🔍 Filtrar",
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            command=cargar_prestamos
        ).grid(row=0, column=4, padx=10)
    
        cargar_prestamos()

    
    def registrar_administrativo(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Registrar usuarios pendientes")
        ventana.geometry("600x400")
        ventana.configure(bg=COLOR_FONDO)
    
        tk.Label(ventana, text="Usuarios pendientes de autenticación", bg=COLOR_FONDO, fg="white",
                 font=("Helvetica", 14, "bold")).pack(pady=10)
    
        # Marco scrollable para la lista
        frame_scroll = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_scroll.pack(expand=True, fill="both", padx=10, pady=10)
    
        canvas = tk.Canvas(frame_scroll, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        lista_frame = tk.Frame(canvas, bg=COLOR_FONDO)
    
        lista_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=lista_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        # Función para recargar los datos
        def cargar_usuarios():
            for widget in lista_frame.winfo_children():
                widget.destroy()
    
            usuarios = self.db.obtener_no_autenticados()
    
            if not usuarios:
                tk.Label(lista_frame, text="✅ No hay usuarios pendientes de autenticación.",
                         bg=COLOR_FONDO, fg="white").pack(pady=20)
            else:
                for u in usuarios:
                    fila = tk.Frame(lista_frame, bg=COLOR_FONDO)
                    fila.pack(fill="x", pady=5)
                
                    texto = f"{u['nombre_completo']} | Curso: {u['curso']} | Rol: {u['rol']} | Correo: {u['correo']}"
                    tk.Label(fila, text=texto, bg=COLOR_FONDO, fg="white",
                             anchor="w", justify="left", wraplength=350).pack(side="left", fill="x", expand=True)
                    
                    # Botón para eliminar el registro
                    def borrar(nombre=u['nombre_completo']):
                        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de borrar a '{nombre}'?")
                        if confirmacion:
                            self.db.eliminar_usuario(nombre)
                            messagebox.showinfo("Registro eliminado", f"El usuario '{nombre}' ha sido borrado.")
                            cargar_usuarios()
                
                    tk.Button(fila, text="Borrar registro", bg="red", fg="white",
                              command=borrar).pack(side="right", padx=5)
                    # Botón para aceptar el registro
                    def aceptar(nombre=u['nombre_completo']):
                        self.db.autenticar_usuario(nombre)
                        messagebox.showinfo("Registro aprobado", f"El usuario '{nombre}' ha sido autenticado.")
                        cargar_usuarios()
                
                    tk.Button(fila, text="Aceptar registro", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                              command=aceptar).pack(side="right", padx=5)
    
        cargar_usuarios()
    

    def interfaz_calificacion_libros(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Calificar y Ver Reseñas")
        ventana.configure(bg=COLOR_FONDO)
        ventana.geometry("600x600")

    # --- Título ---
        tk.Label(
            ventana, text="Calificar y Ver Reseñas de Libros",
            bg=COLOR_FONDO, fg="white",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)

    # --- Formulario ---
        frame_formulario = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_formulario.pack(pady=10)

    # 1. Selección del libro
        tk.Label(frame_formulario, text="Seleccionar libro:",
                bg=COLOR_FONDO, fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        libros_disponibles = [libro.nombre for libro in self.libros]
        libro_var = tk.StringVar()
        combo_libros = ttk.Combobox(frame_formulario, textvariable=libro_var, values=libros_disponibles, state="readonly", width=40)
        combo_libros.grid(row=0, column=1, padx=5, pady=5)

    # 2. Calificación
        tk.Label(frame_formulario, text="Calificación (1 a 5):",
             bg=COLOR_FONDO, fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        calificacion_var = tk.IntVar(value=5)
        spin_calificacion = tk.Spinbox(frame_formulario, from_=1, to=5, textvariable=calificacion_var, width=5)
        spin_calificacion.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # 3. Reseña
        tk.Label(frame_formulario, text="Reseña (opcional):",
             bg=COLOR_FONDO, fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="ne")
        texto_reseña = tk.Text(frame_formulario, width=40, height=4)
        texto_reseña.grid(row=2, column=1, padx=5, pady=5)

    
        def calificar():
            nombre = libro_var.get()
            calif = calificacion_var.get()
            resena = texto_reseña.get("1.0", tk.END).strip()

            if not nombre:
                messagebox.showwarning("Error", "Selecciona un libro.")
                return
            self.calificarLibro(nombre, calif, resena if resena else None)
            messagebox.showinfo("Éxito", "✅ Calificación registrada con éxito.")

    # Botón para calificar libro
        tk.Button(ventana, text="Calificar libro", command=calificar).pack(pady=10)

        def mostrar_ventana_reseñas(libro):
            reseña_win = tk.Toplevel()
            reseña_win.title(f"Reseñas de {libro.nombre}")
            reseña_win.configure(bg=COLOR_FONDO)
            reseña_win.geometry("500x400")

            tk.Label(reseña_win, text=f"📖 Reseñas de '{libro.nombre}'",
                bg=COLOR_FONDO, fg=COLOR_TEXTO,
                font=("Helvetica", 14, "bold")).pack(pady=10)

            frame = tk.Frame(reseña_win, bg=COLOR_FONDO)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            canvas = tk.Canvas(frame, bg=COLOR_FONDO, highlightthickness=0)
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas, bg=COLOR_FONDO)

            scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            if libro.reseñas:
                for idx, (calif, res) in enumerate(zip(libro.calificaciones, libro.reseñas), start=1):
                    texto = f"{idx}. ⭐ {calif} - {res if res else '(Sin reseña)'}"
                    tk.Label(scroll_frame, text=texto, bg=COLOR_FONDO, fg="white", anchor="w", justify="left", wraplength=400).pack(anchor="w", pady=3)
            else:
                tk.Label(scroll_frame, text="No hay reseñas aún.", bg=COLOR_FONDO, fg="white").pack(pady=10)

    # Botón para ver reseñas
        def ver_reseñas():
            nombre = libro_var.get()
            if not nombre:
                messagebox.showwarning("Error", "Selecciona un libro.")
                return
            for libro in self.libros:
                if libro.nombre.lower() == nombre.lower():  
                    mostrar_ventana_reseñas(libro)
                    return
                messagebox.showwarning("Error", "Libro no encontrado.")

        tk.Button(ventana, text="Ver reseñas del libro", command=ver_reseñas).pack(pady=5)

    # Botón para mostrar promedio de todos los libros
        def mostrar_promedios():
            texto = ""
            for libro in self.libros:
                if libro.calificaciones:
                    promedio = sum(libro.calificaciones) / len(libro.calificaciones)
                    texto += f"📖 {libro.nombre}: {promedio:.2f} ⭐ ({len(libro.calificaciones)} opiniones)\n"
                else:
                    texto += f"📖 {libro.nombre}: Sin calificaciones\n"
                    messagebox.showinfo("Calificaciones promedio", texto)

        tk.Button(ventana, text="Mostrar calificaciones promedio", command=mostrar_promedios).pack(pady=5)


       

    def _borrar_placeholder(self, entry, texto_placeholder):
        if entry.get() == texto_placeholder:
            entry.delete(0, "end")
            entry.config(fg="black")

    def _restaurar_placeholder(self, entry, texto_placeholder):
        if entry.get() == "":
            entry.insert(0, texto_placeholder)
            entry.config(fg="gray")
    
        
if __name__ == "__main__":
    App()
    

    

