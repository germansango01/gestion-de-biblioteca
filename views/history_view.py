import tkinter as tk
from tkinter import ttk
# Asumo que las clases History y DatabaseManager están en la carpeta 'clases'
from clases.history import History
from clases.database import DatabaseManager

class HistoryView(tk.Frame):
    """Interfaz principal para ver el historial de préstamos."""
    
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager
        self.history_manager = History(db_manager)
        
        self.user_search_var = tk.StringVar()
        self.is_active_only = tk.BooleanVar(value=True)
        
        self.create_widgets()
        self.load_history()

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
        columns = ("ID", "Título", "Usuario", "Préstamo", "Devolución")
        tree = ttk.Treeview(parent_frame, columns=columns, show="headings")
        
        # ✅ CORRECCIÓN 3: Usar cadenas literales para 'anchor'
        config = [("ID", 50, 'center'), ("Título", 250, 'w'), ("Usuario", 120, 'w'), 
                ("Préstamo", 150, 'w'), ("Devolución", 150, 'center')]
        
        for name, width, anchor in config:
            tree.heading(name, text=name, anchor=anchor)
            tree.column(name, width=width, anchor=anchor)
            
        tree.tag_configure('activo', foreground='red')
        tree.tag_configure('devuelto', foreground='green')
        
        vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview); vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)
        
        return tree

    def load_history(self):
        self.history_tree.delete(*self.history_tree.get_children())

        username = self.user_search_var.get().strip()
        user_id = None
        
        if username:
            # Buscar el ID (usando db_manager, se asume que DatabaseManager está en clases/)
            result = self.db_manager.select_one("SELECT id FROM users WHERE username = ?;", (username,))
            if result: 
                user_id = result[0]
            else: 
                self.history_tree.insert("", tk.END, values=("—", f"Usuario '{username}' no encontrado.", "—", "—", "—"))
                return

        if self.is_active_only.get() and user_id is None:
            history_data = self.history_manager.get_active_loans()
        else:
            # Si se busca por user_id, se obtienen todos sus préstamos (activos e inactivos)
            # Si no se busca por user_id, y no es solo activo, se obtienen todos los préstamos.
            history_data = self.history_manager.get_loans(user_id=user_id)
        
        if not history_data: 
            self.history_tree.insert("", tk.END, values=("—", "No hay registros que coincidan con el filtro.", "—", "—", "—")); 
            return

        for row in history_data:
            # Row puede tener 4 o 5 elementos (dependiendo de si viene de get_active_loans o get_loans)
            if len(row) == 4:
                loan_id, title, username_loan, loan_date = row
                return_date = None
            else:
                loan_id, title, username_loan, loan_date, return_date = row
            
            is_active = return_date is None
            display_return_date = return_date if not is_active else "ACTIVO"
            tag = 'activo' if is_active else 'devuelto'
            
            self.history_tree.insert("", tk.END, 
                                    values=(loan_id, title, username_loan, loan_date, display_return_date), 
                                    tags=(tag,))