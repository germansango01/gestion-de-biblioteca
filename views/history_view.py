import tkinter as tk
from clases.history import History
from clases.users import User

class HistoryView(tk.Frame):
    """Interfaz para ver Préstamos Activos e Historial Completo."""
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.history_manager = History(db_manager)
        
        self.user_search_var = tk.StringVar()
        self.is_active_only = tk.BooleanVar(value=True)
        
        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # --- Controles de Filtro ---
        top_frame = tk.Frame(self, padx=10, pady=10)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="Username:").pack(side=tk.LEFT, padx=5)
        tk.Entry(top_frame, textvariable=self.user_search_var, width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Checkbutton(top_frame, text="Solo Activos", variable=self.is_active_only, 
                       command=self.load_history).pack(side=tk.LEFT, padx=15)

        tk.Button(top_frame, text="Buscar/Refrescar", command=self.load_history, 
                  bg="#FFC107").pack(side=tk.LEFT, padx=5)
        
        # --- Listbox para Resultados ---
        list_frame = tk.LabelFrame(self, text="Historial de Préstamos (ID | Título | Usuario | Fecha Préstamo | Fecha Devolución)", padx=10, pady=5)
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.history_listbox = tk.Listbox(list_frame, height=20)
        self.history_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(list_frame, command=self.history_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)

    def load_history(self):
        self.history_listbox.delete(0, tk.END)

        user_id = None
        username = self.user_search_var.get()
        active_only = self.is_active_only.get()

        # Obtener user_id si se busca por username
        if username:
            result = self.history_manager.db.execute_query("SELECT id FROM users WHERE username = ?", (username,))
            if result:
                user_id = result[0][0]
            else:
                self.history_listbox.insert(tk.END, f"Usuario '{username}' no encontrado.")
                return

        if active_only:
            # Reutilizamos la lógica del BookView para filtrar activos con un solo query si el user_id existe
            query = """
                SELECT l.id, b.title, u.username, l.loan_date, l.return_date
                FROM loans l
                JOIN books b ON l.book_id = b.id
                JOIN users u ON l.user_id = u.id
                WHERE l.return_date IS NULL {}
                ORDER BY l.loan_date DESC
            """
            params = ()
            if user_id is not None:
                query = query.format("AND l.user_id = ?")
                params = (user_id,)
            else:
                 query = query.format("")
            history_data = self.history_manager.db.execute_query(query, params)
        else:
            # Historial completo (usa el método de History)
            history_data = self.history_manager.get_loans(user_id=user_id)
        
        if not history_data:
            self.history_listbox.insert(tk.END, "No hay registros que coincidan con el filtro.")
            return

        for row in history_data:
            loan_id, title, username, loan_date, return_date = row
            display_return_date = return_date if return_date else "ACTIVO"
            
            line = f"{loan_id:<5} | {title[:30]:<30} | {username:<15} | {loan_date:<15} | {display_return_date}"
            self.history_listbox.insert(tk.END, line)