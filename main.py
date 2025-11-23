import customtkinter as ctk
from tkinter import messagebox

from clases.database import Database
from clases.books import Book
from clases.users import User
from clases.history import History

from views.book_view import BookView
from views.user_view import UserView
from views.loan_view import LoanView
from views.history_view import HistoryView

class LibraryApp(ctk.CTk):
    """Aplicación principal de la biblioteca con pestañas para libros, usuarios, préstamos e historial."""

    def __init__(self):
        """Inicializa la aplicación, la base de datos y las pestañas de la interfaz."""
        super().__init__()
        self.title("Biblioteca")
        self.geometry("800x700")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Instancia la base de datos y las clases del dominio
        self.db = Database()
        self.book_class = Book(self.db)
        self.user_class = User(self.db)
        self.history_class = History(self.db)

        # Contenedor principal con pestañas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabview.add("Libros")
        self.tabview.add("Usuarios")
        self.tabview.add("Préstamos")
        self.tabview.add("Historial")

        # Inicializa las vistas
        self.init_views()

    def init_views(self):
        """Crea e incrusta cada vista en la pestaña correspondiente."""
        # Libros
        self.book_view = BookView(self.tabview.tab("Libros"), self.book_class, self.user_class)
        self.book_view.pack(fill="both", expand=True)

        # Usuarios
        self.user_view = UserView(self.tabview.tab("Usuarios"), self.user_class)
        self.user_view.pack(fill="both", expand=True)

        # Préstamos
        self.loan_view = LoanView(self.tabview.tab("Préstamos"), self.book_class)
        self.loan_view.pack(fill="both", expand=True)

        # Historial
        self.history_view = HistoryView(self.tabview.tab("Historial"), self.history_class)
        self.history_view.pack(fill="both", expand=True)

    def on_exit(self):
        """
        Maneja el cierre de la aplicación.

        Pregunta al usuario si desea salir, cierra la base de datos y destruye la ventana.
        """
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            self.db.close()
            self.destroy()


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
