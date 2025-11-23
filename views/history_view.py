import customtkinter as ctk

class HistoryView(ctk.CTkFrame):
    """Vista para mostrar el historial completo de préstamos."""

    def __init__(self, parent, history_class):
        """
        Inicializa la vista de historial.

        Args:
            parent: frame padre donde se incrusta.
            history_class: instancia de la clase History.
        """
        super().__init__(parent)
        self.history_class = history_class

        # Lista del historial
        self.history_listbox = ctk.CTkTextbox(self, width=700, height=500)
        self.history_listbox.pack(padx=5, pady=5)

        self.refresh_history()


    def refresh_history(self):
        """Actualiza la lista del historial de préstamos."""
        self.history_listbox.delete("1.0", "end")
        loans = self.history_class.get_loans()
        for l in loans:
            return_date = l[4] if l[4] else "Pendiente"
            self.history_listbox.insert("end", f"ID:{l[0]} Libro:{l[1]} Usuario:{l[2]} Prestado:{l[3]} Devuelto:{return_date}\n")
