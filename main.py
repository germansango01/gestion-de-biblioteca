import customtkinter as ctk
import tkinter.ttk as ttk
from clases.database import Database
# Importación de Vistas
from views.user_view import UserView
from views.book_view import BookView
from views.loan_view import LoanView
from views.history_view import HistoryView

class App(ctk.CTk):
    """
    Aplicación principal que configura la interfaz gráfica (CustomTkinter)
    y gestiona las pestañas para cada módulo de la biblioteca.
    """
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Biblioteca")
        # Ajustamos el tamaño para que las tablas se vean bien
        self.geometry("900x650") 
        
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
        """Aplica un estilo básico al Treeview de Tkinter para integrarlo con ctk."""
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
                        fieldbackground=self._apply_appearance_mode_color("#FFFFFF", "#2B2B2B"),
                        background=self._apply_appearance_mode_color("#FFFFFF", "#2B2B2B"),
                        foreground=self._apply_appearance_mode_color("#000000", "#FFFFFF"))
        
        # Estilo para la selección
        style.map("Treeview", 
                background=[('selected', self._apply_appearance_mode_color("#1f6aa5", "#1f6aa5"))],
                foreground=[('selected', 'white')])

    def _apply_appearance_mode_color(self, light_color, dark_color):
        """Devuelve el color basado en el modo de apariencia actual."""
        if ctk.get_appearance_mode() == "Dark":
            return dark_color
        return light_color


    def _create_tabs(self):
        """Crea las pestañas y carga las vistas correspondientes."""
        
        # Pestaña USUARIOS
        user_tab = self.tabview.add("Usuarios")
        UserView(user_tab, self.db).pack(fill="both", expand=True)

        # Pestaña LIBROS
        book_tab = self.tabview.add("Libros")
        BookView(book_tab, self.db).pack(fill="both", expand=True)
        
        # Pestaña PRÉSTAMOS Y DEVOLUCIONES
        loan_tab = self.tabview.add("Préstamos y Devoluciones")
        LoanView(loan_tab, self.db).pack(fill="both", expand=True)

        # Pestaña HISTORIAL
        history_tab = self.tabview.add("Historial")
        HistoryView(history_tab, self.db).pack(fill="both", expand=True)

    def on_closing(self):
        """Cierra la conexión a la base de datos al cerrar la aplicación."""
        if self.db:
            self.db.close()
        self.destroy()

if __name__ == "__main__":
    # Configuración de apariencia (puede ser "System", "Dark", "Light")
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    
    app = App()
    
    # Aseguramos que la base de datos se cierre cuando se cierra la ventana
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    app.mainloop()