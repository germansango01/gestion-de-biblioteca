import tkinter as tk
from tkinter import ttk
from clases.history import History
from clases.database import DatabaseManager 

class HistoryView(tk.Frame):
    """Interfaz principal para ver el historial de préstamos."""
    
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager
        self.history_manager = History(db_manager)
        
        self.user_search_var = tk.StringVar()
        self.is_active_only = tk.BooleanVar(value=True) # Mostrar solo activos por defecto
        
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

        username = self.user_search_var.get().strip()
        user_id = None
        
        if username:
            # Busca el ID del usuario (debe existir aunque esté soft-deleted)
            result = self.db_manager.select_one("SELECT id FROM users WHERE username = ?;", (username,))
            
            if result: 
                user_id = result[0]
            else: 
                self.history_tree.insert("", tk.END, values=("—", f"Usuario '{username}' no encontrado.", "—", "—", "—")); 
                return

        # Si el filtro es solo activo, usamos History.get_active_loans
        if self.is_active_only.get() and user_id is None:
            history_data = self.history_manager.get_active_loans()
        else:
            # Si hay filtro de usuario o se quieren todos los registros
            history_data = self.history_manager.get_loans(user_id=user_id)
        
        if not history_data: 
            self.history_tree.insert("", tk.END, values=("—", "No hay registros que coincidan con el filtro.", "—", "—", "—")); 
            return

        for row in history_data:
            # Formato esperado: (loan_id, title, username_loan, loan_date, return_date [o None])
            
            if len(row) >= 5:
                loan_id, title, username_loan, loan_date, return_date = row
            elif len(row) == 4:
                 # Desde get_active_loans
                loan_id, title, username_loan, loan_date = row
                return_date = None
            else:
                 continue
            
            is_active = return_date is None
            display_return_date = return_date if not is_active else "ACTIVO"
            tag = 'activo' if is_active else 'devuelto'
            
            self.history_tree.insert("", tk.END, values=(loan_id, title, username_loan, loan_date, display_return_date), tags=(tag,))