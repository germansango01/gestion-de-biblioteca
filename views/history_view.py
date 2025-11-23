import customtkinter as ctk

class HistoryView(ctk.CTkFrame):
    """Vista para mostrar el historial completo de préstamos."""

    def __init__(self, master, history_class):
        """
        Inicializa la vista de historial.

        Args:
            master: contenedor padre.
            history_class (History): instancia de la clase History.
        """
        super().__init__(master)
        self.history_class = history_class

        # Widgets
        self.refresh_btn = ctk.CTkButton(self, text="Actualizar Lista", command=self.refresh_history)
        self.listbox = ctk.CTkTextbox(self, width=600, height=400)

        # Layout
        self.refresh_btn.grid(row=0, column=0, padx=5, pady=5)
        self.listbox.grid(row=1, column=0, padx=5, pady=5)

        self.refresh_history()


    def refresh_history(self):
        """Actualiza la lista del historial de préstamos."""
        self.listbox.delete("1.0", "end")
        loans = self.history_class.get_loans()
        for l in loans:
            return_date = l[4] if l[4] else "Pendiente"
            self.listbox.insert("end", f"ID:{l[0]} Libro:{l[1]} Usuario:{l[2]} Prestado:{l[3]} Devuelto:{return_date}\n")
