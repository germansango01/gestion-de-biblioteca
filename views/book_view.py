import tkinter as tk
from tkinter import messagebox, ttk
from clases.books import Book
from clases.database import DatabaseManager
import re

# ==============================================================================
# Modal para Agregar/Editar Libro
# ==============================================================================
class AddBookModal(tk.Toplevel):
    """Ventana modal para el formulario de agregar/editar libro."""
    
    def __init__(self, master, db_manager, book_data=None, callback_on_success=None):
        self.book_manager = Book(db_manager)
        self.callback_on_success = callback_on_success
        self.book_data = book_data
        
        super().__init__(master)
        
        is_editing = book_data is not None
        title_text = "✏️ Editar Libro" if is_editing else "➕ Agregar Nuevo Libro"
        self.title(title_text)
        self.transient(master); self.grab_set(); self.focus_set()
        
        # Variables de control (Tipado Básico)
        self.title_var = tk.StringVar(value=book_data[1] if is_editing else "")
        self.isbn_var = tk.StringVar(value=book_data[2] if is_editing else "")
        self.author_var = tk.StringVar(value=book_data[3] if is_editing else "")
        self.category_var = tk.StringVar(value=book_data[4] if is_editing else "")
        
        self.create_widgets(is_editing)


    def _is_valid_isbn(self, isbn):
        """Simple validación de formato ISBN (10 o 13 dígitos numéricos)."""
        isbn_clean = re.sub(r'[-\s]', '', isbn)
        return bool(re.fullmatch(r'(\d{10}|\d{13})', isbn_clean))


    def create_widgets(self, is_editing):
        main_frame = ttk.Frame(self, padding="15"); main_frame.pack(fill="both", expand=True)
        
        fields = [
            ("Título: *", self.title_var), 
            ("ISBN: *", self.isbn_var), 
            ("Autor: *", self.author_var),
            ("Categoría: *", self.category_var)
        ]
        
        for i, (text, var) in enumerate(fields):
            ttk.Label(main_frame, text=text).grid(row=i, column=0, sticky="w", pady=5)
            state = "readonly" if is_editing and text == "ISBN: *" else "normal"
            ttk.Entry(main_frame, textvariable=var, width=40, state=state).grid(row=i, column=1, padx=10, pady=5)
            
        button_text = "Guardar Cambios" if is_editing else "✅ Registrar Libro"
        action_command = self.edit_book_ui if is_editing else self.add_book_ui
        
        ttk.Button(main_frame, text=button_text, command=action_command, style='Accent.TButton').grid(
            row=len(fields), column=0, columnspan=2, pady=15, sticky="ew")


    def _validate_input(self, isbn_check=True):
        """Valida la entrada del usuario. Retorna tuple o None."""
        title = self.title_var.get().strip()
        isbn = self.isbn_var.get().strip()
        author_name = self.author_var.get().strip()
        category = self.category_var.get().strip()
        
        if not title or not isbn or not author_name or not category:
            messagebox.showerror("Error de Entrada", "Todos los campos marcados con '*' son obligatorios.", parent=self)
            return None

        if isbn_check and not self._is_valid_isbn(isbn):
            messagebox.showerror("Error de Validación", "El ISBN debe tener 10 o 13 dígitos (solo números).", parent=self)
            return None
        
        return (title, isbn, author_name, category)


    def add_book_ui(self):
        validated_data = self._validate_input(isbn_check=True)
        if validated_data is None: return
        
        title, isbn, author_name, category = validated_data
        
        if self.book_manager.add_book(title, isbn, author_name, category):
            messagebox.showinfo("Éxito", f"Libro '{title}' agregado correctamente.", parent=self)
            if self.callback_on_success: self.callback_on_success()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo agregar el libro. (ISBN duplicado o error de DB).", parent=self)


    def edit_book_ui(self):
        validated_data = self._validate_input(isbn_check=False) # No revalidamos el ISBN, ya existe
        if validated_data is None: return
        
        title, isbn, author_name, category = validated_data
        book_id = self.book_data[0]
        
        if self.book_manager.update_book(book_id, title, isbn, author_name, category):
            messagebox.showinfo("Éxito", f"Libro ID {book_id} actualizado correctamente.", parent=self)
            if self.callback_on_success: self.callback_on_success()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el libro.", parent=self)


# ==============================================================================
# Vista Principal de Libros y Préstamos
# ==============================================================================
class BookView(tk.Frame):
    """Interfaz principal para Listar, Prestar y Devolver Libros."""
    
    def __init__(self, master, db_manager, logged_in_user_id):
        super().__init__(master)
        self.db_manager = db_manager
        self.book_manager = Book(db_manager)
        self.logged_in_user_id = logged_in_user_id
        
        self.loan_user_var = tk.StringVar()
        self.selected_book_data = None # tuple o None
        
        self.create_widgets()
        self.load_books()


    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10"); main_frame.pack(fill="both", expand=True)
        control_frame = ttk.Frame(main_frame); control_frame.pack(fill="x", pady=10)
        
        # Botones de CRUD (sin cambios)
        ttk.Button(control_frame, text="➕ Nuevo Libro", command=self.open_add_book_modal).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="✏️ Editar Libro", command=self.open_edit_book_modal).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🗑️ Eliminar Libro (Soft Delete)", command=self.delete_book_ui, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🔄 Recargar Libros", command=self.load_books).pack(side=tk.LEFT, padx=5)
        
        # Sección de Préstamos 
        loan_frame = ttk.LabelFrame(control_frame, text="Gestión de Préstamo", padding=5)
        loan_frame.pack(side=tk.RIGHT, padx=5)
        
        # Si no hay sesión, se deshabilita
        if not self.logged_in_user_id:
            ttk.Label(loan_frame, text="⛔ Inicie sesión para prestar/devolver.", foreground="red").pack(padx=10, pady=5)
            state = tk.DISABLED
        else:
            state = tk.NORMAL
        
        ttk.Label(loan_frame, text="Username:").pack(side=tk.LEFT, padx=(5, 5))
        ttk.Entry(loan_frame, textvariable=self.loan_user_var, width=15, state=state).pack(side=tk.LEFT, padx=5)

        ttk.Button(loan_frame, text="➡️ Prestar", command=self.lend_book_ui, style='Accent.TButton', state=state).pack(side=tk.LEFT, padx=5)
        ttk.Button(loan_frame, text="⬅️ Devolver", command=self.return_book_ui, state=state).pack(side=tk.LEFT, padx=5)
        
        self.selected_label = ttk.Label(main_frame, text="Libro Seleccionado: Ninguno", foreground="blue")
        self.selected_label.pack(fill="x", pady=(0, 5))

        self.books_tree = self._setup_treeview(main_frame); self.books_tree.pack(fill="both", expand=True, pady=5)
        self.books_tree.bind("<<TreeviewSelect>>", self.on_book_select)


    def _setup_treeview(self, parent_frame):
        columns = ("ID", "Título", "ISBN", "Autor", "Categoría", "Disp."); tree = ttk.Treeview(parent_frame, columns=columns, show="headings", selectmode="browse")
        tree.heading("ID", text="ID", anchor=tk.CENTER); tree.column("ID", width=40, anchor=tk.CENTER)
        tree.heading("Título", text="Título"); tree.column("Título", width=200)
        tree.heading("ISBN", text="ISBN"); tree.column("ISBN", width=100)
        tree.heading("Autor", text="Autor"); tree.column("Autor", width=150)
        tree.heading("Categoría", text="Categoría"); tree.column("Categoría", width=100)
        tree.heading("Disp.", text="Disp."); tree.column("Disp.", width=50, anchor=tk.CENTER)
        tree.tag_configure('disponible', background='#e6ffe6', foreground='green'); tree.tag_configure('prestado', background='#ffeeee', foreground='red')
        
        vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview); vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)
        
        return tree


    def open_add_book_modal(self):
        AddBookModal(self.master, self.db_manager, callback_on_success=self.load_books) 
    
    
    def open_edit_book_modal(self):
        if not self.selected_book_data: 
            messagebox.showwarning("Advertencia", "Seleccione un libro para editar."); return

        # Pasamos solo los datos necesarios para la edición (ID, Title, ISBN, Author, Category)
        book_data_for_edit = self.selected_book_data[:5]
        AddBookModal(self.master, self.db_manager, book_data=book_data_for_edit, callback_on_success=self.load_books)
        
        
    def delete_book_ui(self):
        if not self.selected_book_data: 
            messagebox.showwarning("Advertencia", "Seleccione un libro para eliminar."); return
            
        book_id = int(self.selected_book_data[0]); title = self.selected_book_data[1]; available_status = self.selected_book_data[5]

        if available_status == "NO":
            messagebox.showerror("Error", "No se puede eliminar un libro que está prestado actualmente."); return
        
        if messagebox.askyesno("Confirmar Eliminación (Soft Delete)", 
                            f"¿Está seguro de realizar el soft delete del libro '{title}' (ID: {book_id})?",
                            parent=self):
            
            if self.book_manager.delete_book(book_id):
                messagebox.showinfo("Éxito", f"Libro '{title}' marcado como eliminado.")
                self.selected_book_data = None
                self.selected_label.config(text="Libro Seleccionado: Ninguno")
                self.load_books()
            else:
                messagebox.showerror("Error", "No se pudo marcar el libro como eliminado.")


    def on_book_select(self, event):
        selected_item = self.books_tree.selection()
        if selected_item:
            values = self.books_tree.item(selected_item, 'values')
            self.selected_book_data = values 
            title = values[1]; status = values[5]
            self.selected_label.config(text=f"Libro Seleccionado: {title} (Disp: {status})")
        else:
            self.selected_book_data = None; self.selected_label.config(text="Libro Seleccionado: Ninguno")


    def load_books(self):
        for item in self.books_tree.get_children(): self.books_tree.delete(item)
        books = self.book_manager.list_books()
        
        if not books: 
            self.books_tree.insert("", tk.END, values=("—", "No hay libros registrados.", "—", "—", "—", "—")); return

        for book in books:
            # book es (id, title, isbn, author, category, available) - 'available' es 1 o 0
            book_id, title, isbn, author_name, category, available = book 
            
            status = "SÍ" if available == 1 else "NO"
            tag = 'disponible' if available == 1 else 'prestado'
            
            self.books_tree.insert("", tk.END, 
                                values=(book_id, title, isbn, author_name, category, status), 
                                tags=(tag,))


    def _find_user_id(self, username):
        """Busca el ID de un usuario por su nombre usando select_one(). Retorna int o None."""
        result = self.db_manager.select_one(
            "SELECT id FROM users WHERE username = ? AND deleted_at IS NULL;", 
            (username,)
        )
        # Se asegura que el usuario esté activo para prestarle
        return result[0] if result else None


    def lend_book_ui(self):
        if not self.logged_in_user_id: return
            
        if not self.selected_book_data: messagebox.showwarning("Advertencia", "Seleccione un libro para prestar."); return
        
        book_id = int(self.selected_book_data[0])
        available_status = self.selected_book_data[5] # "SÍ" o "NO"
        
        if available_status == "NO": messagebox.showwarning("Advertencia", "El libro ya está prestado."); return
        
        username = self.loan_user_var.get().strip()
        if not username: messagebox.showwarning("Advertencia", "Ingrese el Username del prestatario."); return

        user_id = self._find_user_id(username)
        if user_id is None: messagebox.showerror("Error", f"El usuario '{username}' no existe o está eliminado."); return

        # Se usa el método simplificado lend_book del modelo
        if self.book_manager.lend_book(book_id, user_id):
            messagebox.showinfo("Préstamo Exitoso", f"Libro ID {book_id} prestado a {username}.")
            self.loan_user_var.set(""); self.selected_book_data = None
            self.selected_label.config(text="Libro Seleccionado: Ninguno"); self.load_books()
        else:
            messagebox.showerror("Error", "Error al prestar el libro (DB o lógica interna).")


    def return_book_ui(self):
        if not self.logged_in_user_id: return

        if not self.selected_book_data: messagebox.showwarning("Advertencia", "Seleccione un libro para devolver."); return
        
        book_id = int(self.selected_book_data[0])
        available_status = self.selected_book_data[5] # "SÍ" o "NO"

        if available_status == "SÍ": messagebox.showwarning("Advertencia", "El libro ya está disponible (no estaba prestado)."); return

        # Se usa el método simplificado return_book del modelo
        if self.book_manager.return_book(book_id):
            messagebox.showinfo("Devolución Exitosa", f"Libro ID {book_id} devuelto y disponible.")
            self.selected_book_data = None
            self.selected_label.config(text="Libro Seleccionado: Ninguno"); self.load_books()
        else:
            messagebox.showerror("Error", "Error al devolver el libro (DB o lógica interna).")