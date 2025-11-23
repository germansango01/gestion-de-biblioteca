import tkinter as tk
from tkinter import messagebox, ttk
from clases.books import Book
from clases.users import User

class LoanView(tk.Frame):
    """
    Vista optimizada para que un usuario logueado (NO Admin) 
    preste y devuelva libros.
    """
    
    def __init__(self, master, db_manager, user_manager: User, logged_in_user_id):
        super().__init__(master)
        self.db_manager = db_manager
        self.book_manager = Book(db_manager)
        self.user_manager = user_manager
        self.logged_in_user_id = logged_in_user_id
        
        self.loan_user_var = tk.StringVar()
        self.selected_book_data = None
        
        self._set_initial_username()
        self.create_widgets()
        self.load_available_books()

    def _set_initial_username(self):
        """Establece el nombre del usuario logueado en el campo de solo lectura."""
        if self.logged_in_user_id:
            user_data = self.user_manager.get_user_by_id(self.logged_in_user_id)
            if user_data:
                self.loan_user_var.set(user_data[1])
            else:
                self.loan_user_var.set("Error: Usuario no encontrado")
        else:
            self.loan_user_var.set("NO LOGUEADO")


    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="15"); main_frame.pack(fill="both", expand=True)

        # Sección de Control Superior
        control_frame = ttk.LabelFrame(main_frame, text="Operación de Préstamo", padding=10)
        control_frame.pack(fill="x", pady=10)

        # Muestra el usuario actual
        ttk.Label(control_frame, text="Usuario Logueado:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(control_frame, textvariable=self.loan_user_var, width=20, state="readonly").grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(control_frame, text="➡️ Prestar Libro", command=self.lend_book_ui, style='Accent.TButton').grid(row=0, column=2, padx=15, pady=5)
        ttk.Button(control_frame, text="⬅️ Devolver Libro", command=self.return_book_ui).grid(row=0, column=3, padx=15, pady=5)
        ttk.Button(control_frame, text="🔄 Recargar Disponibles", command=self.load_available_books).grid(row=0, column=4, padx=15, pady=5)

        # Treeview de Libros Disponibles
        ttk.Label(main_frame, text="Seleccione un libro para prestar:", font=("Arial", 12)).pack(fill="x", pady=(15, 5))
        self.books_tree = self._setup_treeview(main_frame); self.books_tree.pack(fill="both", expand=True, pady=5)
        self.books_tree.bind("<<TreeviewSelect>>", self.on_book_select)
        
        self.selected_label = ttk.Label(main_frame, text="Libro Seleccionado: Ninguno", foreground="blue")
        self.selected_label.pack(fill="x", pady=(0, 5))


    def _setup_treeview(self, parent_frame):
        columns = ("ID", "Título", "ISBN", "Autor", "Categoría")
        tree = ttk.Treeview(parent_frame, columns=columns, show="headings", selectmode="browse")
        
        # ✅ CORRECCIÓN 3: Usar cadenas literales para 'anchor'
        config = [("ID", 40, 'center'), ("Título", 200, 'w'), ("ISBN", 100, 'w'), 
                ("Autor", 150, 'w'), ("Categoría", 100, 'w')]
        
        for name, width, anchor in config:
            tree.heading(name, text=name, anchor=anchor)
            tree.column(name, width=width, anchor=anchor)
        
        vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview); vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)
        
        return tree

    # ... (El resto de la lógica de LoanView se mantiene igual) ...
    def on_book_select(self, event):
        selected_item = self.books_tree.selection()
        if selected_item:
            values = self.books_tree.item(selected_item, 'values')
            self.selected_book_data = values 
            self.selected_label.config(text=f"Libro Seleccionado: {values[1]} (ISBN: {values[2]})")
        else:
            self.selected_book_data = None
            self.selected_label.config(text="Libro Seleccionado: Ninguno")

    def load_available_books(self):
        """Carga solo los libros que están disponibles."""
        self.books_tree.delete(*self.books_tree.get_children())
        books = self.book_manager.list_books(available_only=True) 
        
        if not books: 
            self.books_tree.insert("", tk.END, values=("—", "No hay libros disponibles para préstamo.", "—", "—", "—")); return

        for book in books:
            self.books_tree.insert("", tk.END, values=book[:5])

    def lend_book_ui(self):
        if not self.logged_in_user_id: 
            return messagebox.showerror("Error", "Debe iniciar sesión para realizar préstamos.")
        if not self.selected_book_data or self.selected_book_data[0] == '—': 
            return messagebox.showwarning("Advertencia", "Seleccione un libro válido para prestar.")
        
        try:
            book_id = int(self.selected_book_data[0])
        except ValueError:
            return messagebox.showerror("Error", "ID de libro no válido.")
            
        user_id = self.logged_in_user_id

        if self.book_manager.lend_book(book_id, user_id):
            messagebox.showinfo("Préstamo Exitoso", f"Libro {self.selected_book_data[1]} prestado a {self.loan_user_var.get()}.")
            self.selected_book_data = None
            self.selected_label.config(text="Libro Seleccionado: Ninguno")
            self.load_available_books()
        else:
            messagebox.showerror("Error", "Error al prestar el libro. Verifique disponibilidad.")

    def return_book_ui(self):
        if not self.logged_in_user_id: 
            return messagebox.showerror("Error", "Debe iniciar sesión para realizar devoluciones.")
        
        book_id_to_return = self.book_manager.find_active_loan_by_user_id(self.logged_in_user_id)
        
        if book_id_to_return is None: 
            return messagebox.showwarning("Advertencia", f"El usuario {self.loan_user_var.get()} no tiene préstamos activos para devolver.")

        if self.book_manager.return_book(book_id_to_return):
            messagebox.showinfo("Devolución Exitosa", "Devolución del libro completada y actualizado el historial.")
            self.load_available_books()
        else:
            messagebox.showerror("Error", "Error al devolver el libro.")