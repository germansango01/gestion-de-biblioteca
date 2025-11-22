import tkinter as tk
from tkinter import messagebox, ttk
from clases.books import Book
from clases.users import User
from clases.history import History
# from clases.author import Author  <-- Eliminado, ya no es necesario
import re

class AddBookModal(tk.Toplevel):
    """Ventana modal para el formulario de agregar/editar libro."""
    def __init__(self, master, db_manager, book_data=None, callback_on_success=None):
        super().__init__(master)
        
        self.book_manager = Book(db_manager)
        self.callback_on_success = callback_on_success
        self.book_data = book_data

        is_editing = book_data is not None
        title_text = "✏️ Editar Libro" if is_editing else "➕ Agregar Nuevo Libro"
        self.title(title_text)
        self.transient(master); self.grab_set(); self.focus_set()
        
        # Variables de control
        self.title_var = tk.StringVar(value=book_data[1] if is_editing else "")
        self.isbn_var = tk.StringVar(value=book_data[2] if is_editing else "")
        self.author_name_var = tk.StringVar(value=book_data[3] if is_editing else "")
        self.category_var = tk.StringVar(value=book_data[4] if is_editing else "")
        
        self.create_widgets(is_editing)


    def _is_valid_isbn(self, isbn: str) -> bool:
        """Simple validación de formato ISBN (10 o 13 dígitos numéricos)."""
        isbn_clean = re.sub(r'[-\s]', '', isbn) # Remueve guiones y espacios
        return bool(re.fullmatch(r'(\d{10}|\d{13})', isbn_clean))


    def create_widgets(self, is_editing: bool):
        main_frame = ttk.Frame(self, padding="15"); main_frame.pack(fill="both", expand=True)
        
        fields = [
            ("Título:", self.title_var), 
            ("ISBN:", self.isbn_var), 
            ("Autor:", self.author_name_var),
            ("Categoría:", self.category_var)
        ]
        
        for i, (text, var) in enumerate(fields):
            ttk.Label(main_frame, text=text).grid(row=i, column=0, sticky="w", pady=5)
            # Deshabilitar ISBN en edición para evitar romper la unicidad
            state = "readonly" if is_editing and text == "ISBN:" else "normal"
            ttk.Entry(main_frame, textvariable=var, width=40, state=state).grid(row=i, column=1, padx=10, pady=5)
            
        button_text = "Guardar Cambios" if is_editing else "✅ Registrar Libro"
        action_command = self.edit_book_ui if is_editing else self.add_book_ui
        
        ttk.Button(main_frame, text=button_text, command=action_command, style='Accent.TButton').grid(
            row=len(fields), column=0, columnspan=2, pady=15, sticky="ew")


    def add_book_ui(self):
        title = self.title_var.get().strip(); isbn = self.isbn_var.get().strip()
        category = self.category_var.get().strip() or None
        author_name = self.author_name_var.get().strip() or None 
        
        if not title or not isbn:
            messagebox.showerror("Error de Entrada", "El Título y el ISBN son obligatorios.", parent=self); return

        if not self._is_valid_isbn(isbn):
            messagebox.showerror("Error de Validación", "El ISBN debe tener 10 o 13 dígitos (solo números).", parent=self); return
        
        if self.book_manager.add_book(title, isbn, author_name, category):
            messagebox.showinfo("Éxito", f"Libro '{title}' agregado correctamente.", parent=self)
            if self.callback_on_success: self.callback_on_success()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo agregar el libro. (ISBN duplicado o error de DB).", parent=self)


    def edit_book_ui(self):
        book_id = self.book_data[0]
        title = self.title_var.get().strip(); isbn = self.isbn_var.get().strip() # ISBN no cambia
        category = self.category_var.get().strip() or None
        author_name = self.author_name_var.get().strip() or None
        
        if not title or not isbn:
            messagebox.showerror("Error de Entrada", "El Título y el ISBN son obligatorios.", parent=self); return
        
        if self.book_manager.update_book(book_id, title, isbn, author_name, category):
            messagebox.showinfo("Éxito", f"Libro ID {book_id} actualizado correctamente.", parent=self)
            if self.callback_on_success: self.callback_on_success()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el libro.", parent=self)


class BookView(tk.Frame):
    """Interfaz principal para Listar, Prestar y Devolver Libros."""
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager; self.book_manager = Book(db_manager)
        self.loan_user_var = tk.StringVar(); self.selected_book_data = None
        self.create_widgets(); self.load_books()


    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10"); main_frame.pack(fill="both", expand=True)
        control_frame = ttk.Frame(main_frame); control_frame.pack(fill="x", pady=10)
        
        ttk.Button(control_frame, text="➕ Nuevo Libro", command=self.open_add_book_modal).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="✏️ Editar Libro", command=self.open_edit_book_modal).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🗑️ Eliminar Libro", command=self.delete_book_ui, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🔄 Recargar Libros", command=self.load_books).pack(side=tk.LEFT, padx=5)
        
        # Configurar estilo Danger (asumiendo que está definido en el MainApp, si no, descomentar lo siguiente)
        style = ttk.Style(self)
        style.configure('Danger.TButton', background='#D32F2F', foreground='white', borderwidth=0)
        style.map('Danger.TButton', background=[('active', '#B71C1C')], foreground=[('active', 'white')])

        loan_frame = ttk.LabelFrame(control_frame, text="Gestión de Préstamo", padding=5)
        loan_frame.pack(side=tk.RIGHT, padx=5)

        ttk.Label(loan_frame, text="Username:").pack(side=tk.LEFT, padx=(5, 5))
        ttk.Entry(loan_frame, textvariable=self.loan_user_var, width=15).pack(side=tk.LEFT, padx=5)

        ttk.Button(loan_frame, text="➡️ Prestar", command=self.lend_book_ui, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(loan_frame, text="⬅️ Devolver", command=self.return_book_ui).pack(side=tk.LEFT, padx=5)
        
        self.selected_label = ttk.Label(main_frame, text="Libro Seleccionado: Ninguno", foreground="blue")
        self.selected_label.pack(fill="x", pady=(0, 5))

        self.books_tree = self._setup_treeview(main_frame); self.books_tree.pack(fill="both", expand=True, pady=5)
        self.books_tree.bind("<<TreeviewSelect>>", self.on_book_select)


    def _setup_treeview(self, parent_frame):
        # Columnas actualizadas
        columns = ("ID", "Título", "ISBN", "Autor", "Categoría", "Disp."); tree = ttk.Treeview(parent_frame, columns=columns, show="headings", selectmode="browse")
        tree.heading("ID", text="ID", anchor=tk.CENTER); tree.column("ID", width=40, anchor=tk.CENTER)
        tree.heading("Título", text="Título"); tree.column("Título", width=200)
        tree.heading("ISBN", text="ISBN"); tree.column("ISBN", width=100)
        tree.heading("Autor", text="Autor"); tree.column("Autor", width=150)
        tree.heading("Categoría", text="Categoría"); tree.column("Categoría", width=100)
        tree.heading("Disp.", text="Disp."); tree.column("Disp.", width=50, anchor=tk.CENTER)
        tree.tag_configure('disponible', background='#e6ffe6', foreground='green'); tree.tag_configure('prestado', background='#ffeeee', foreground='red')
        
        # Scrollbar vertical
        vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview)
        vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)
        
        return tree


    def open_add_book_modal(self):
        AddBookModal(self.master, self.db_manager, callback_on_success=self.load_books) 
    
    
    def open_edit_book_modal(self):
        if not self.selected_book_data: 
            messagebox.showwarning("Advertencia", "Seleccione un libro para editar."); return

        # book_data contiene (id, title, isbn, author, category, available)
        AddBookModal(self.master, self.db_manager, book_data=self.selected_book_data, callback_on_success=self.load_books)
        
    
    def delete_book_ui(self):
        if not self.selected_book_data: 
            messagebox.showwarning("Advertencia", "Seleccione un libro para eliminar."); return
            
        book_id, title, _, _, _, available = self.selected_book_data

        if available == 0:
            messagebox.showerror("Error", "No se puede eliminar un libro que está prestado actualmente."); return
        
        if messagebox.askyesno("Confirmar Eliminación", 
                            f"¿Está seguro de eliminar el libro '{title}' (ID: {book_id})?\n\nEsta acción es irreversible.",
                            parent=self):
            # Asumiendo que has añadido un método delete_book en Book Manager
            if self.book_manager.delete_book(book_id):
                messagebox.showinfo("Éxito", f"Libro '{title}' eliminado correctamente.")
                self.selected_book_data = None
                self.selected_label.config(text="Libro Seleccionado: Ninguno")
                self.load_books()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el libro.")


    def on_book_select(self, event):
        selected_item = self.books_tree.selection()
        if selected_item:
            values = self.books_tree.item(selected_item, 'values')
            # Almacenar todos los datos del libro seleccionado: (id, title, isbn, author, category, status_display)
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
            # book es (id, title, isbn, author, category, available)
            book_id, title, isbn, author_name, category, available = book 
            
            author_display = author_name if author_name else "N/A"
            category_display = category if category else "N/A"
            
            status = "SÍ" if available == 1 else "NO"
            tag = 'disponible' if available == 1 else 'prestado'
            
            # Los valores insertados deben coincidir con las columnas del Treeview
            self.books_tree.insert("", tk.END, 
                                values=(book_id, title, isbn, author_display, category_display, status), 
                                tags=(tag,))


    def lend_book_ui(self):
        if not self.selected_book_data: messagebox.showwarning("Advertencia", "Seleccione un libro para prestar."); return
        book_id = int(self.selected_book_data[0]); available = self.selected_book_data[5]
        
        if available == "NO": messagebox.showwarning("Advertencia", "El libro ya está prestado."); return
        
        username = self.loan_user_var.get().strip()
        if not username: messagebox.showwarning("Advertencia", "Ingrese el Username del prestatario."); return

        # Buscar usuario
        user_check = self.db_manager.execute("SELECT id FROM users WHERE username = ?", (username,), fetch_one=True)
        if not user_check: messagebox.showerror("Error", f"El usuario '{username}' no existe."); return
        user_id = user_check[0]

        if self.book_manager.lend_book(book_id, user_id):
            messagebox.showinfo("Préstamo Exitoso", f"Libro ID {book_id} prestado a {username}.")
            self.loan_user_var.set(""); self.selected_book_data = None
            self.selected_label.config(text="Libro Seleccionado: Ninguno"); self.load_books()
        else:
            messagebox.showerror("Error", "Error de DB al prestar el libro.")


    def return_book_ui(self):
        if not self.selected_book_data: messagebox.showwarning("Advertencia", "Seleccione un libro para devolver."); return
        book_id = int(self.selected_book_data[0]); available = self.selected_book_data[5]

        if available == "SÍ": messagebox.showwarning("Advertencia", "El libro ya está disponible (no estaba prestado)."); return

        if self.book_manager.return_book(book_id):
            messagebox.showinfo("Devolución Exitosa", f"Libro ID {book_id} devuelto y disponible.")
            self.selected_book_data = None
            self.selected_label.config(text="Libro Seleccionado: Ninguno"); self.load_books()
        else:
            messagebox.showerror("Error", "Error de DB al devolver el libro.")