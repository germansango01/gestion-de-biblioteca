import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class HistoryView(ctk.CTkFrame):
    """Vista historial usando Treeview para presentación tipo tabla."""

    def __init__(self, parent, history_class):
        """
        Args:
            parent: contenedor padre.
            history_class: instancia de la clase History.
        """
        super().__init__(parent)
        self.history_class = history_class

        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkButton(toolbar, text="Refrescar", command=self.render_table).pack(side="right", padx=6)

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=8, pady=8)

        self.tree = ttk.Treeview(table_frame, columns=("title", "user", "loan", "return"), show="headings")
        self.tree.heading("title", text="Título")
        self.tree.heading("user", text="Usuario")
        self.tree.heading("loan", text="Prestado")
        self.tree.heading("return", text="Devuelto")
        self.tree.column("title", width=320, anchor="w")
        self.tree.column("user", width=140, anchor="w")
        self.tree.column("loan", width=160, anchor="center")
        self.tree.column("return", width=160, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.render_table()

    def render_table(self):
        """Carga el historial completo (incluye libros soft-deleted)."""
        for r in self.tree.get_children():
            self.tree.delete(r)
        loans = self.history_class.get_loans()
        for l in loans:
            ret = l[4] if l[4] else "Pendiente"
            self.tree.insert("", "end", values=(l[1] or "—", l[2] or "—", l[3] or "—", ret))
