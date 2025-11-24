import customtkinter as ctk
import tkinter.ttk as ttk
from clases.database import Database
from views.user_view import UserView
from views.book_view import BookView
from views.loan_view import LoanView
from views.history_view import HistoryView

class App(ctk.CTk):
    """
    Aplicación principal que configura la interfaz gráfica
    y gestiona las pestañas para cada módulo de la biblioteca.
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


    def _create_tabs(self):
        """
        Crea las pestañas y carga las vistas.
        """
        
        # Configurar la disposición en grid para las pestañas
        for tab_name in ["Libros", "Usuarios", "Préstamos y Devoluciones", "Historial"]:
            tab = self.tabview.add(tab_name)
            tab.grid_rowconfigure(0, weight=1)
            tab.grid_columnconfigure(0, weight=1)

        # Pestaña LIBROS
        book_tab = self.tabview.tab("Libros")
        BookView(book_tab, self.db).grid(row=0, column=0, sticky="nsew")

        # Pestaña USUARIOS
        user_tab = self.tabview.tab("Usuarios")
        UserView(user_tab, self.db).grid(row=0, column=0, sticky="nsew")
        
        # Pestaña PRÉSTAMOS Y DEVOLUCIONES
        loan_tab = self.tabview.tab("Préstamos y Devoluciones")
        LoanView(loan_tab, self.db).grid(row=0, column=0, sticky="nsew")

        # Pestaña HISTORIAL
        history_tab = self.tabview.tab("Historial")
        HistoryView(history_tab, self.db).grid(row=0, column=0, sticky="nsew")


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