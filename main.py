import tkinter as tk
from tkinter import messagebox, ttk
from clases.database import DatabaseManager
from views.book_view import BookView
from views.user_view import UserView
from views.history_view import HistoryView

# Database Library
DB_NAME = "library.db"

class LibraryApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Biblioteca Modular")
        self.geometry("900x650")
        
        # Configuración de estilo TTK
        style = ttk.Style(self) # <-- Ya no se guarda como self.style
        style.theme_use('clam')
        # Estilo principal
        style.configure('Accent.TButton', background='#2196F3', foreground='white', borderwidth=0)
        style.map('Accent.TButton', background=[('active', '#1976D2')], foreground=[('active', 'white')])

        self.db_manager = None
        
        if self._connect_db():
            self.create_menu()
            self.create_notebook()
        else:
            messagebox.showerror("Error Fatal", "La aplicación no pudo iniciar debido a un error de base de datos.")
            self.quit()


    def _connect_db(self):
        """Intenta conectar con la base de datos y establece la conexión."""
        self.db_manager = DatabaseManager(db_name=DB_NAME)
        self.db_manager.connect_db()
        # Nota: Asegúrate de eliminar el archivo library.db para que la columna author_id se cree
        return self.db_manager._conn is not None


    def create_menu(self):
        """Crea la barra de menú superior."""
        menubar = tk.Menu(self); self.config(menu=menubar)

        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Recargar Vistas", command=self.reload_notebook)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.on_closing)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Acerca de", "Sistema de Biblioteca Simple v1.0"))


    def create_notebook(self):
        """Crea el widget Notebook (pestañas) y añade las vistas (Frames)."""
        if hasattr(self, 'notebook'): self.notebook.destroy()
            
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Pestaña de Libros
        book_frame = BookView(self.notebook, self.db_manager)
        self.notebook.add(book_frame, text="📚 Libros / Préstamos")

        # Pestaña de Usuarios
        user_frame = UserView(self.notebook, self.db_manager)
        self.notebook.add(user_frame, text="👤 Usuarios")

        # Pestaña de Historial
        history_frame = HistoryView(self.notebook, self.db_manager)
        self.notebook.add(history_frame, text="📜 Historial")


    def reload_notebook(self):
        """Recarga todas las pestañas."""
        self.create_notebook()
        messagebox.showinfo("Recarga", "Vistas recargadas correctamente.")


    def on_closing(self):
        """Maneja el cierre de la ventana principal y cierra la conexión DB."""
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
            if self.db_manager: self.db_manager.close_db()
            self.destroy()

if __name__ == '__main__':
    app = LibraryApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()