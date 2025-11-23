import tkinter as tk
from tkinter import messagebox, ttk
from clases.database import DatabaseManager
from clases.users import User
from views.book_view import BookView
from views.user_view import UserView
from views.history_view import HistoryView

# Database Library
DB_NAME = "library.db"

class LibraryApp(tk.Tk):
    """Clase principal de la aplicación Tkinter. Gestiona la conexión a DB y la interfaz principal."""

    def __init__(self):
        super().__init__()
        self.title("Sistema de Biblioteca Modular")
        self.geometry("900x650")
        
        # --- Variables de Sesión ---
        self.logged_in_user_id = None # int o None
        self.user_manager = None
        # ---------------------------

        self.db_manager = None
        self._configure_styles()
        
        if self._connect_db():
            # El User Manager necesita la DB
            self.user_manager = User(self.db_manager) 
            self.create_menu()
            self.create_auth_screen() # Mostramos la pantalla de autenticación primero
        else:
            messagebox.showerror("Error Fatal", "La aplicación no pudo iniciar debido a un error de base de datos.")
            self.quit()

    def _configure_styles(self):
        """Configura los estilos TTK."""
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Accent.TButton', background='#2196F3', foreground='white', borderwidth=0)
        style.map('Accent.TButton', background=[('active', '#1976D2')], foreground=[('active', 'white')])
        style.configure('Danger.TButton', background='#D32F2F', foreground='white', borderwidth=0)
        style.map('Danger.TButton', background=[('active', '#B71C1C')], foreground=[('active', 'white')])


    def _connect_db(self):
        """Intenta conectar con la base de datos. Retorna bool."""
        self.db_manager = DatabaseManager(db_name=DB_NAME)
        # La conexión se realiza en el __init__ de DatabaseManager
        return self.db_manager._connection is not None


    def create_menu(self):
        """Crea la barra de menú superior."""
        menubar = tk.Menu(self); self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0); menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Recargar Vistas", command=self.reload_notebook)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.on_closing)
        
        help_menu = tk.Menu(menubar, tearoff=0); menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Acerca de", "Sistema de Biblioteca Simple v1.0"))


    def create_auth_screen(self):
        """Crea la pantalla de autenticación inicial."""
        if hasattr(self, 'notebook'): self.notebook.destroy()
        if hasattr(self, 'auth_frame'): self.auth_frame.destroy()
            
        self.auth_frame = ttk.Frame(self, padding="50"); self.auth_frame.pack(expand=True)
        
        ttk.Label(self.auth_frame, text="🔒 Iniciar Sesión", font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        self.auth_user_var = tk.StringVar(); self.auth_pass_var = tk.StringVar()
        
        form_frame = ttk.Frame(self.auth_frame); form_frame.pack()

        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.auth_user_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.auth_pass_var, show="*", width=30).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="🔑 Entrar", command=self.attempt_login, style='Accent.TButton').grid(row=2, column=0, columnspan=2, pady=15, sticky="ew")


    def attempt_login(self):
        username = self.auth_user_var.get().strip(); password = self.auth_pass_var.get().strip()
        if not username or not password: messagebox.showerror("Error", "Ingrese usuario y contraseña."); return

        user_id = self.user_manager.authenticate(username, password)
        
        if user_id:
            self.logged_in_user_id = user_id
            messagebox.showinfo("Login Exitoso", f"Bienvenido, {username} (ID: {user_id})")
            self.auth_frame.destroy()
            self.create_main_notebook()
        else:
            messagebox.showerror("Login Fallido", "Usuario o contraseña incorrectos.")


    def create_main_notebook(self):
        """Crea las pestañas principales de la aplicación."""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        self.reload_notebook()


    def reload_notebook(self):
        """Destruye y recrea las pestañas para refrescar las vistas."""
        if not hasattr(self, 'notebook'): return

        # 1. Limpiar pestañas existentes
        for tab in self.notebook.winfo_children():
            tab.destroy()

        # 2. Crear las nuevas pestañas
        # Vista de Libros
        book_frame = BookView(self.notebook, self.db_manager, logged_in_user_id=self.logged_in_user_id)
        self.notebook.add(book_frame, text="📚 Gestión de Libros")

        # Vista de Usuarios (Solo para administradores o desarrollo)
        user_frame = UserView(self.notebook, self.db_manager)
        self.notebook.add(user_frame, text="👤 Gestión de Usuarios")
        
        # Vista de Historial
        history_frame = HistoryView(self.notebook, self.db_manager)
        self.notebook.add(history_frame, text="📜 Historial de Préstamos")


    def on_closing(self):
        """Maneja el cierre de la aplicación."""
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
            if self.db_manager:
                self.db_manager.close()
            self.destroy()

if __name__ == "__main__":
    app = LibraryApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()