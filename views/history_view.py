import tkinter as tk
from tkinter import ttk, messagebox
from clases.history import History

class HistoryView(tk.Frame):
    """Interfaz principal para ver el historial de préstamos."""
    def __init__(self, master, db_manager):
        super().__init__(master); self.db_manager = db_manager; self.history_manager = History(db_manager)
        self.user_search_var = tk.StringVar(); self.is_active_only = tk.BooleanVar(value=True)
        self.create_widgets(); self.load_history()


    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10"); main_frame.pack(fill="both", expand=True)
        filter_frame = ttk.Frame(main_frame); filter_frame.pack(fill="x", pady=10)

        ttk.Label(filter_frame, text="Username:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(filter_frame, textvariable=self.user_search_var, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Checkbutton(filter_frame, text="Solo Activos", variable=self.is_active_only, 
                        command=self.load_history).pack(side=tk.LEFT, padx=15)

        ttk.Button(filter_frame, text="🔍 Buscar/Refrescar", command=self.load_history, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        self.history_tree = self._setup_treeview(main_frame); self.history_tree.pack(fill="both", expand=True, pady=5)


    def _setup_treeview(self, parent_frame):
        columns = ("ID", "Título", "Usuario", "Préstamo", "Devolución"); tree = ttk.Treeview(parent_frame, columns=columns, show="headings")
        tree.heading("ID", text="ID", anchor=tk.CENTER); tree.column("ID", width=50, anchor=tk.CENTER)
        tree.heading("Título", text="Título"); tree.column("Título", width=250)
        tree.heading("Usuario", text="Usuario"); tree.column("Usuario", width=120)
        tree.heading("Préstamo", text="Fecha Préstamo"); tree.column("Préstamo", width=150)
        tree.heading("Devolución", text="Fecha Devolución"); tree.column("Devolución", width=150, anchor=tk.CENTER)
        tree.tag_configure('activo', foreground='red'); tree.tag_configure('devuelto', foreground='green')
        return tree


    def load_history(self):
        for item in self.history_tree.get_children(): self.history_tree.delete(item)

        user_id = None; username = self.user_search_var.get().strip(); active_only = self.is_active_only.get()

        if username:
            # Usar la DB directamente para verificar el ID del usuario
            result = self.db_manager.execute("SELECT id FROM users WHERE username = ?", (username,), fetch_one=True)
            if result: user_id = result[0]
            else: self.history_tree.insert("", tk.END, values=("—", f"Usuario '{username}' no encontrado.", "—", "—", "—")); return

        query = """
            SELECT l.id, b.title, u.username, l.loan_date, l.return_date
            FROM loans l JOIN books b ON l.book_id = b.id JOIN users u ON l.user_id = u.id
        """
        params = []; conditions = []

        if active_only: conditions.append("l.return_date IS NULL")
        if user_id is not None: conditions.append("l.user_id = ?"); params.append(user_id)
        
        if conditions: query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY l.loan_date DESC"

        history_data = self.db_manager.execute(query, tuple(params))

        if history_data is False or not history_data: 
            self.history_tree.insert("", tk.END, values=("—", "No hay registros que coincidan con el filtro.", "—", "—", "—")); return

        for row in history_data:
            loan_id, title, username_loan, loan_date, return_date = row
            is_active = return_date is None
            display_return_date = return_date if not is_active else "ACTIVO"
            tag = 'activo' if is_active else 'devuelto'
            self.history_tree.insert("", tk.END, values=(loan_id, title, username_loan, loan_date, display_return_date), tags=(tag,))

