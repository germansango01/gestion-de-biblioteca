import customtkinter as ctk
from tkinter import messagebox, Menu

from clases.database import Database
from clases.books import Book
from clases.users import User
from clases.history import History

from views.book_view import BookView
from views.user_view import UserView
from views.loan_view import LoanView
from views.history_view import HistoryView

class LibraryApp(ctk.CTk):
    """Aplicación principal de la biblioteca con menú y vistas."""

    def __init__(self):
        """
        Inicializa la aplicación, la base de datos y la interfaz.
        """
        super().__init__()
        self.title("Biblioteca")
        self.geometry("750x650")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        # Instancia de la base de datos y clases
        self.db = Database()
        self.book_class = Book(self.db)
        self.user_class = User(self.db)
        self.history_class = History(self.db)

        # Configura menú principal
        self.create_menu()

        # Contenedor de vistas
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Inicializa vistas
        self.views = {}
        self.init_views()

        # Muestra la vista por defecto
        self.show_view("Book")


    def create_menu(self):
        """Crea el menú principal de la aplicación."""
        menubar = Menu(self)
        self.config(menu=menubar)

        menu_app = Menu(menubar, tearoff=0)
        menu_app.add_command(label="Libros", command=lambda: self.show_view("Book"))
        menu_app.add_command(label="Usuarios", command=lambda: self.show_view("User"))
        menu_app.add_command(label="Préstamos", command=lambda: self.show_view("Loan"))
        menu_app.add_command(label="Historial", command=lambda: self.show_view("History"))
        menu_app.add_separator()
        menu_app.add_command(label="Salir", command=self.on_exit)

        menubar.add_cascade(label="Menú", menu=menu_app)


    def init_views(self):
        """Inicializa todas las vistas y las guarda en un diccionario."""
        self.views["Book"] = BookView(self.container, self.book_class, self.user_class)
        self.views["User"] = UserView(self.container, self.user_class)
        self.views["Loan"] = LoanView(self.container, self.book_class)
        self.views["History"] = HistoryView(self.container, self.history_class)


    def show_view(self, view_name):
        """
        Muestra la vista seleccionada y oculta las demás.

        Args:
            view_name (str): nombre de la vista a mostrar.
        """
        for name, view in self.views.items():
            view.grid_forget()
        self.views[view_name].grid(row=0, column=0, sticky="nsew")


    def on_exit(self):
        """Cierra correctamente la base de datos y la aplicación."""
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            self.db.close()
            self.destroy()

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
