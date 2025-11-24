# views/history_view.py
import customtkinter as ctk
from tkinter import ttk
from clases.loan import Loan # Ahora importamos Loan en lugar de History

class HistoryView(ctk.CTkFrame):
    """
    Muestra el historial completo de préstamos (activos y devueltos).
    """

    def __init__(self, master, db):
        super().__init__(master)
        # Instanciamos Loan, que ahora contiene la lógica de reportes.
        self.manager = Loan(db) 

        ctk.CTkLabel(self, text="📜 Historial Completo de Préstamos 📜", font=("Arial", 16, "bold")).pack(pady=10)

        # Configuración de la tabla
        cols = ("ID", "Libro", "Usuario", "Prestado", "Devuelto")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols: 
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150, anchor='center')
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh()


    def refresh(self):
        """Carga el historial completo usando el método get_history."""
        self.tree.delete(*self.tree.get_children())
        
        # Usamos el método get_history de la clase Loan (sin filtrar por usuario)
        for row in self.manager.get_history():
            vals = list(row)
            # Si return_date es NULL, se muestra como "ACTIVO"
            if not vals[4]: vals[4] = "ACTIVO"
            self.tree.insert("", "end", values=vals)