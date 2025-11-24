import customtkinter as ctk
from tkinter import ttk


class StatisticsView(ctk.CTkFrame):
    """
    Muestra la estadisticas generales.
    """

    def __init__(self, master, db):
        super().__init__(master)

        # Configuración del layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # La tabla estará en la fila 2

        # Título (Fila 0)
        ctk.CTkLabel(self, text="📜 Estadisticas 📜", font=("Arial", 16, "bold")).grid(
            row=0, column=0, pady=(10, 5), sticky="ew"
        )
        
        #Frame de Controles (Fila 1)
        controls_frame = ctk.CTkFrame(self)
        controls_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Botón de reporte
        ctk.CTkButton(controls_frame, text="Reporte", command=self.get_report).pack(side="left", padx=5, pady=5)


    def get_report():
        pass
