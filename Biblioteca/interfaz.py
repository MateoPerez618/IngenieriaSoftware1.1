import tkinter as tk
from tkinter import ttk, messagebox
from autenticacion import UsuarioDB, Usuario
from Libro import LibroDB
from disponibilidad import GestorDisponibilidad

COLOR_FONDO = "#003366"
COLOR_BOTON = "#0055A5"
COLOR_TEXTO = "white"

class App:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Usuarios")
        self.ventana.geometry("500x500")
        self.ventana.configure(bg=COLOR_FONDO)

        self.db = UsuarioDB()
        self.usuario_actual = None

        self.marco = tk.Frame(self.ventana, bg=COLOR_FONDO)
        self.marco.pack(expand=True, fill="both")

        self.mostrar_inicio()

        self.ventana.mainloop()

    def limpiar_marco(self):
        for widget in self.marco.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_marco()

        tk.Label(self.marco, text="Colegio Nuestra Señora de la Providencia",
                 bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Helvetica", 16, "bold")).pack(pady=(30, 40))

        tk.Button(self.marco, text="Iniciar sesión", width=20, bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  font=("Helvetica", 12), command=self.mostrar_login).pack(pady=10)

        tk.Button(self.marco, text="Registrarse", width=20, bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  font=("Helvetica", 12), command=self.mostrar_registro_paso1).pack(pady=10)

    def mostrar_login(self):
        self.limpiar_marco()

        tk.Label(self.marco, text="Iniciar sesión", bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 10))

        tk.Label(self.marco, text="Nombre completo:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        entry_nombre = tk.Entry(self.marco)
        entry_nombre.pack()

        tk.Label(self.marco, text="Contraseña:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        entry_pass = tk.Entry(self.marco, show="*")
        entry_pass.pack()

        def intentar_login():
            nombre = entry_nombre.get().strip()
            password = entry_pass.get().strip()
            usuario = self.db.login(nombre, password)
            if usuario:
                self.usuario_actual = usuario
                self.mostrar_funcionalidades()
            else:
                messagebox.showerror("Error", "Credenciales inválidas.")

        tk.Button(self.marco, text="Ingresar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=intentar_login).pack(pady=15)
        tk.Button(self.marco, text="Volver", command=self.mostrar_inicio).pack()

    def mostrar_registro_paso1(self):
        self.limpiar_marco()
        tk.Label(self.marco, text="Registro - Paso 1", bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 10))

        tk.Label(self.marco, text="Nombre completo:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        entry_nombre = tk.Entry(self.marco)
        entry_nombre.pack()

        tk.Label(self.marco, text="Curso:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        entry_curso = tk.Entry(self.marco)
        entry_curso.pack()

        def validar_y_continuar():
            nombre = entry_nombre.get().strip()
            curso = entry_curso.get().strip()

            if not nombre or not curso:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            if self.db.existe_usuario_por_nombre_y_curso(nombre,curso):
                messagebox.showerror("Error", "El usuario ya existe.")
                return

            self.mostrar_registro_paso2(nombre, curso)

        tk.Button(self.marco, text="Siguiente", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=validar_y_continuar).pack(pady=15)
        tk.Button(self.marco, text="Volver", command=self.mostrar_inicio).pack()

    def mostrar_registro_paso2(self, nombre, curso):
        self.limpiar_marco()
        tk.Label(self.marco, text="Registro - Paso 2", bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 10))
        
        tk.Label(self.marco, text=f"Nombre: {nombre}", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        tk.Label(self.marco, text=f"Curso: {curso}", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()

        tk.Label(self.marco, text="Contraseña:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        entry_pass = tk.Entry(self.marco, show="*")
        entry_pass.pack()

        tk.Label(self.marco, text="Rol:", bg=COLOR_FONDO, fg=COLOR_TEXTO).pack()
        roles = ["Estudiante", "Docente", "Administrativo"]
        rol_var = tk.StringVar()
        rol_menu = ttk.Combobox(self.marco, textvariable=rol_var, values=roles, state="readonly")
        rol_menu.pack()
        rol_menu.current(0)

        def registrar():
            password = entry_pass.get().strip()
            rol = rol_var.get()
            if not password:
                messagebox.showerror("Error", "La contraseña es obligatoria.")
                return
            usuario = Usuario(nombre, password, curso, rol)
            if self.db.registrar(usuario):
                messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
                self.mostrar_inicio()

        tk.Button(self.marco, text="Registrar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=registrar).pack(pady=15)
        tk.Button(self.marco, text="Volver", command=self.mostrar_registro_paso1).pack()

    def mostrar_funcionalidades(self):
        self.limpiar_marco()
        tk.Label(self.marco, text=f"Bienvenido, {self.usuario_actual.nombre_completo}",
             bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Helvetica", 14, "bold")).pack(pady=(20, 10))

        # Funcionalidad 1: Mostrar catálogo
        tk.Button(self.marco, text="Mostrar catálogo", width=20,
              bg=COLOR_BOTON, fg=COLOR_TEXTO, command=self.mostrar_catalogo).pack(pady=5)
        
        tk.Button(self.marco, text="Ver disponibilidad", width=20,
              bg=COLOR_BOTON, fg=COLOR_TEXTO, command=self.mostrar_disponibilidad).pack(pady=5)

        # Funcionalidades vacías como ejemplo
        for i in range(3, 5):
            tk.Button(self.marco, text=f"Funcionalidad {i}", width=20,
                  bg=COLOR_BOTON, fg=COLOR_TEXTO).pack(pady=5)

        tk.Button(self.marco, text="Cerrar sesión", bg="red", fg="white",
              command=self.mostrar_inicio).pack(pady=(30, 10))

    def mostrar_catalogo(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Catálogo de libros")
        ventana.configure(bg=COLOR_FONDO)
        ventana.geometry("600x600")
    
        tk.Label(ventana, text="Catálogo de la Biblioteca",
                 bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Helvetica", 16, "bold")).pack(pady=10)
    
        # ----- Filtros -----
        filtro_frame = tk.Frame(ventana, bg=COLOR_FONDO)
        filtro_frame.pack(pady=(0, 10))
    
        # Campo de búsqueda
        tk.Label(filtro_frame, text="Buscar (nombre o autor):", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=0, padx=5)
        entrada_busqueda = tk.Entry(filtro_frame)
        entrada_busqueda.grid(row=0, column=1, padx=5)
    
        # Menú desplegable para categoría
        tk.Label(filtro_frame, text="Filtrar por categoría:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=2, padx=5)
        categorias = ["Todas"] + list({libro.categoria for libro in LibroDB().obtener_todos()})
        categoria_var = tk.StringVar(value="Todas")
        categoria_menu = ttk.Combobox(filtro_frame, textvariable=categoria_var, values=categorias, state="readonly")
        categoria_menu.grid(row=0, column=3, padx=5)
    
        # Área scroll
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
    
        # Función para actualizar la lista
        def actualizar_lista():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
    
            texto_busqueda = entrada_busqueda.get().lower()
            categoria_seleccionada = categoria_var.get()
    
            libros = LibroDB().obtener_todos()
            filtrados = []
            for libro in libros:
                coincide_categoria = (categoria_seleccionada == "Todas" or libro.categoria == categoria_seleccionada)
                coincide_busqueda = (texto_busqueda in libro.nombre.lower() or texto_busqueda in libro.autor.lower())
                if coincide_categoria and coincide_busqueda:
                    filtrados.append(libro)
    
            if not filtrados:
                tk.Label(scrollable_frame, text="No se encontraron libros con ese filtro.",
                         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=10)
            else:
                for libro in filtrados:
                    texto = f"{libro.nombre} | Categoría: {libro.categoria} | Autor: {libro.autor} | Cantidad: {libro.cantidad}"
                    tk.Label(scrollable_frame, text=texto, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                             anchor="w", justify="left", wraplength=560).pack(anchor="w", padx=5, pady=3)
    
        # Botón para aplicar filtros
        tk.Button(filtro_frame, text="🔍 Buscar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=actualizar_lista).grid(row=0, column=4, padx=10)
    
        actualizar_lista()

    def mostrar_disponibilidad(self):
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Disponibilidad de horarios")
        ventana.configure(bg=COLOR_FONDO)
        ventana.geometry("550x500")
    
        gestor = GestorDisponibilidad()
    
        tk.Label(ventana, text="Consultar disponibilidad", bg=COLOR_FONDO, fg=COLOR_TEXTO,
                 font=("Helvetica", 14, "bold")).pack(pady=10)
    
        # --- Filtros ---
        frame_opciones = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_opciones.pack(pady=5)
    
        tk.Label(frame_opciones, text="📅 Fecha (YYYY-MM-DD):", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=0, padx=5)
        entry_fecha = tk.Entry(frame_opciones)
        entry_fecha.grid(row=0, column=1)
    
        tk.Label(frame_opciones, text="🕓 Hora (7-14):", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=1, column=0, padx=5)
        entry_hora = tk.Entry(frame_opciones)
        entry_hora.grid(row=1, column=1)
    
        # --- Área scrollable ---
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
    
        # --- Mostrar resultados ---
        def mostrar_resultados():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
    
            fecha = entry_fecha.get().strip()
            hora = entry_hora.get().strip()
    
            resultados = []
            if fecha and hora:
                try:
                    hora = int(hora)
                    resultados = gestor.buscar_disponibilidad(fecha=fecha, hora=hora)
                except ValueError:
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
                resultados = gestor.buscar_disponibilidad()
    
            if not resultados:
                tk.Label(scrollable_frame, text="❌ No hay disponibilidad con esos filtros.",
                         bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=10)
            else:
                for entrada in resultados:
                    texto = f"{entrada.fecha} a las {entrada.hora}:00 — Disponible: {entrada.estado}"
                    tk.Label(scrollable_frame, text=texto, bg=COLOR_FONDO, fg=COLOR_TEXTO,
                             anchor="w", justify="left").pack(anchor="w", padx=5, pady=3)
    
        # Botón buscar
        tk.Button(ventana, text="🔍 Buscar", bg=COLOR_BOTON, fg=COLOR_TEXTO,
                  command=mostrar_resultados).pack(pady=5)
    
        # Mostrar todos los horarios por defecto
        mostrar_resultados()




if __name__ == "__main__":
    App()

