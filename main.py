import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from clases.database import Database
from views.user_view import UserView
from views.book_view import BookView
from views.loan_view import LoanView
from views.history_view import HistoryView
from views.statistics_view import StatisticsView

class App(ctk.CTk):
    """
    Aplicación principal que configura la interfaz gráfica.
    """
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Biblioteca")
        self.geometry("900x650")
        
        # Configuración de CustomTkinter
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")
        
        # Configurar y conectar la Base de Datos
        self.db = Database()

        # Configurar el estilo de Treeview
        self._setup_treeview_style()

        # Configurar el TabView principal
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Crear menu
        self._create_menu()

        # Crear las pestañas
        self._create_tabs()


    def _setup_treeview_style(self):
        """
        Aplica un estilo uniforme a todos los Treeviews de la aplicación.
        """
        style = ttk.Style()
        style.theme_use("default")
        
        # Encabezados
        style.configure("Treeview.Heading", 
                        font=("Arial", 11, "bold"), 
                        background="#3A7EBf",
                        foreground="white",
                        padding=[5, 5])
        style.map("Treeview.Heading", 
                background=[('active', '#D6D6D6')], 
                foreground=[('active', 'black')])
        
        # Filas
        style.configure("Treeview",
                        font=("Arial", 10),
                        rowheight=25,
                        fieldbackground="#FFFFFF",
                        background="#FFFFFF",
                        foreground="#000000")
        
        # Selección
        style.map("Treeview", 
                background=[('selected', "#1f6aa5")],
                foreground=[('selected', 'white')])


    def _create_menu(self):
        """Crea la barra de menú estándar de Tkinter."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Salir", command=self.on_closing)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        # Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Acerca de...", command=self._show_about_dialog)
        menubar.add_cascade(label="Ayuda", menu=help_menu)


    def _show_about_dialog(self):
        messagebox.showinfo("Acerca de", "Sistema de Gestión de Biblioteca\nDesarrollado con Python y CustomTkinter")


    def _create_tabs(self):
        """Crea las pestañas y carga las vistas unificadas."""
        tabs = ["Libros", "Usuarios", "Préstamos y Devoluciones", "Historial", "Estadísticas"]
        for tab_name in tabs:
            tab = self.tabview.add(tab_name)
            tab.grid_rowconfigure(0, weight=1)
            tab.grid_columnconfigure(0, weight=1)

        # Cargar vistas
        BookView(self.tabview.tab("Libros"), self.db).grid(row=0, column=0, sticky="nsew")
        UserView(self.tabview.tab("Usuarios"), self.db).grid(row=0, column=0, sticky="nsew")
        LoanView(self.tabview.tab("Préstamos y Devoluciones"), self.db).grid(row=0, column=0, sticky="nsew")
        HistoryView(self.tabview.tab("Historial"), self.db).grid(row=0, column=0, sticky="nsew")
        StatisticsView(self.tabview.tab("Estadísticas"), self.db).grid(row=0, column=0, sticky="nsew")


    def on_closing(self):
        """Cierra la conexión a la base de datos al cerrar la aplicación."""
        if self.db:
            self.db.close()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
