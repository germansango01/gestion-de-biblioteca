# views/history_view.py
import customtkinter as ctk
from tkinter import ttk
from clases.loan import Loan 

class HistoryView(ctk.CTkFrame):
    """
    Muestra el historial completo de préstamos (activos y devueltos).
    """

    def __init__(self, master, db):
        super().__init__(master)
        # Instanciamos Loan, que ahora contiene la lógica de reportes (get_history).
        self.manager = Loan(db) 

        # Configuración del layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # La tabla estará en la fila 2

        # --- Configuración de Estilos para el Hover ---
        style = ttk.Style()
        style.map("Treeview.Heading", 
                background=[('active', '#D6D6D6')],
                foreground=[('active', 'black')])
        style.configure("Treeview.Heading", 
                        font=('Arial', 10, 'bold'),
                        background='#EDEDED', 
                        foreground='black')

        # Título (Fila 0)
        ctk.CTkLabel(self, text="📜 Historial Completo de Préstamos 📜", font=("Arial", 16, "bold")).grid(
            row=0, column=0, pady=(10, 5), sticky="ew"
        )
        
        #Frame de Controles (Fila 1)
        controls_frame = ctk.CTkFrame(self)
        controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Botón de Refrescar
        ctk.CTkButton(controls_frame, text="🔄 Refrescar Historial", command=self.refresh).pack(side="left", padx=5, pady=5)


        # Configuración de la tabla
        cols = ("ID", "Libro", "Usuario", "Prestado", "Devuelto")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        
        for c in cols: 
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150, anchor='center')
        
        self.tree.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        self.refresh()


    def refresh(self):
        """Carga el historial completo usando el método get_history."""
        self.tree.delete(*self.tree.get_children())
        
        # Usamos el método get_history de la clase Loan 
        for row in self.manager.get_history():
            vals = list(row)
            # Si return_date es NULL, se muestra como "ACTIVO"
            if not vals[4]: vals[4] = "ACTIVO"
            self.tree.insert("", "end", values=vals)