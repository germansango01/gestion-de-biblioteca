import tkinter as tk
from tkinter import messagebox, ttk

from clases.database import DatabaseManager
from views.book_view import BookView
from views.user_view import UserView
from views.history_view import HistoryView

# Configuración de la base de datos
DB_NAME = "library.db"

class LibraryApp(tk.Tk):
    """
    Aplicación Principal usando tk.Notebook para organizar las vistas.
    """
    def __init__(self):
        super().__init__()
        self.title("Biblioteca")
        self.geometry("800x600")
        
        self.db_manager = None
        
        if self._connect_db():
            self.create_menu()
            self.create_notebook()
        else:
            self.quit()


    def _connect_db(self):
        """Intenta conectar con la base de datos."""
        self.db_manager = DatabaseManager(db_name=DB_NAME)
        self.db_manager.connect()
        
        if self.db_manager.conn is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return False
        
        print(f"Conexión a la base de datos '{DB_NAME}' establecida.")
        return True


    def create_menu(self):
        """Crea la barra de menú con la opción de Salir."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Salir", command=self.on_closing)


    def create_notebook(self):
        """Crea el widget Notebook (pestañas) y añade las vistas."""
        
        # Inicializa el Notebook (necesita ttk)
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # 1. Pestaña de Libros
        book_frame = BookView(notebook, self.db_manager)
        book_frame.pack(fill="both", expand=True)
        notebook.add(book_frame, text="📚 Libros / Préstamos")

        # 2. Pestaña de Usuarios
        user_frame = UserView(notebook, self.db_manager)
        user_frame.pack(fill="both", expand=True)
        notebook.add(user_frame, text="👤 Usuarios")

        # 3. Pestaña de Historial
        history_frame = HistoryView(notebook, self.db_manager)
        history_frame.pack(fill="both", expand=True)
        notebook.add(history_frame, text="📜 Historial")

    def on_closing(self):
        """Maneja el cierre de la ventana principal y cierra la conexión DB."""
        if messagebox.askokcancel("Salir", "¿Estás seguro de que deseas salir?"):
            if self.db_manager:
                self.db_manager.close()
                print("Conexión a la base de datos cerrada.")
            self.destroy()

if __name__ == '__main__':
    app = LibraryApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()