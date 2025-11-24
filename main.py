import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
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
        self.geometry("1000x500") 
        
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
        Aplica un estilo básico al Treeview de Tkinter.
        """
        style = ttk.Style()
        
        # Tema general para el Treeview (fondo, color de línea)
        style.theme_use("default")
        
        # Estilo para los encabezados de las columnas (headings)
        style.configure("Treeview.Heading", 
                        font=("Arial", 11, "bold"), 
                        background="#3A7EBf",
                        foreground="white",
                        padding=[5, 5])
        
        # Estilo para las filas
        style.configure("Treeview",
                        font=("Arial", 10),
                        rowheight=25,
                        fieldbackground="#FFFFFF",
                        background="#FFFFFF",
                        foreground="#000000")
        
        # Estilo para la selección
        style.map("Treeview", 
                background=[('selected', "#1f6aa5")],
                foreground=[('selected', 'white')])
        
        # Estilo para el hover en los encabezados (Heading)
        style.map("Treeview.Heading", 
                background=[('active', '#D6D6D6')], 
                foreground=[('active', 'black')])


    def _create_menu(self):
        """
        Crea la barra de menú estándar de Tkinter y la asocia a la ventana.
        """
        # Crear el objeto Menú principal
        menubar = tk.Menu(self) 
        
        # Asignar la barra de menú a la ventana
        self.config(menu=menubar)

        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        # Añadir el submenú "Salir"
        file_menu.add_command(label="Salir", command=self.on_closing) 
        # Añadir el Menú Archivo a la barra principal
        menubar.add_cascade(label="Archivo", menu=file_menu)

        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        # Añadir el submenú "Acerca de"
        help_menu.add_command(label="Acerca de...", command=self._show_about_dialog)
        # Añadir el Menú Ayuda a la barra principal
        menubar.add_cascade(label="Ayuda", menu=help_menu)


    def _show_about_dialog():
        pass


    def _create_tabs(self):
        """
        Crea las pestañas y carga las vistas.
        """
        
        # Configurar la disposición en grid para las pestañas
        for tab_name in ["Libros", "Usuarios", "Préstamos y Devoluciones", "Historial", "Estadisticas"]:
            tab = self.tabview.add(tab_name)
            tab.grid_rowconfigure(0, weight=1)
            tab.grid_columnconfigure(0, weight=1)

        # Pestaña Libros
        book_tab = self.tabview.tab("Libros")
        BookView(book_tab, self.db).grid(row=0, column=0, sticky="nsew")

        # Pestaña usuarios
        user_tab = self.tabview.tab("Usuarios")
        UserView(user_tab, self.db).grid(row=0, column=0, sticky="nsew")
        
        # Pestaña Prestamos
        loan_tab = self.tabview.tab("Préstamos y Devoluciones")
        LoanView(loan_tab, self.db).grid(row=0, column=0, sticky="nsew")

        # Pestaña Historial
        history_tab = self.tabview.tab("Historial")
        HistoryView(history_tab, self.db).grid(row=0, column=0, sticky="nsew")

        # Pestaña Estadisticas
        statistic_tab = self.tabview.tab("Estadisticas")
        StatisticsView(statistic_tab, self.db).grid(row=0, column=0, sticky="nsew")


    def on_closing(self):
        """
        Cierra la conexión a la base de datos al cerrar la aplicación.
        """
        if self.db:
            self.db.close()
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()