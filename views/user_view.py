import tkinter as tk
from tkinter import messagebox, ttk
# Asumo que las clases User y Book están en la carpeta 'clases'
from clases.users import User
from clases.books import Book 
# ✅ Importamos las nuevas pantallas dedicadas
from views.forms.book_form import BookFormScreen 
from views.forms.user_form import UserFormScreen 

class UserView(tk.Frame):
    """Interfaz para gestionar usuarios y el CRUD de libros (Rol Administrador)."""
    
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager
        self.user_manager = User(db_manager)
        self.book_manager = Book(db_manager) 
        self.selected_book_data = None
        
        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10"); main_frame.pack(fill="both", expand=True)
        
        # --- Frame para Usuarios ---
        user_frame = ttk.LabelFrame(main_frame, text="👥 Gestión de Cuentas de Usuarios", padding=10); user_frame.pack(fill="x", pady=10)
        
        control_frame_user = ttk.Frame(user_frame); control_frame_user.pack(fill="x", pady=5)
        # ✅ Llama a la nueva pantalla dedicada
        ttk.Button(control_frame_user, text="➕ Nuevo Usuario", command=self.open_add_user_screen).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame_user, text="🔄 Recargar Usuarios", command=self.load_users).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame_user, text="🗑️ Eliminar Usuario (Soft Delete)", command=self.delete_user_ui, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        self.users_tree = self._setup_user_treeview(user_frame); self.users_tree.pack(fill="x", expand=False, pady=5)

        # --- Frame para Libros (CRUD de Admin) ---
        book_frame = ttk.LabelFrame(main_frame, text="📚 CRUD de Libros (Admin)", padding=10); book_frame.pack(fill="both", expand=True, pady=10)

        control_frame_book = ttk.Frame(book_frame); control_frame_book.pack(fill="x", pady=5)
        # ✅ Llama a la nueva pantalla dedicada
        ttk.Button(control_frame_book, text="➕ Nuevo Libro", command=self.open_add_book_screen, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        # ✅ Llama a la nueva pantalla dedicada
        ttk.Button(control_frame_book, text="✏️ Editar Libro", command=self.open_edit_book_screen).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame_book, text="🗑️ Eliminar Libro", command=self.delete_book_ui, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame_book, text="🔄 Recargar Libros", command=self.load_books_for_admin).pack(side=tk.LEFT, padx=5)

        self.books_tree = self._setup_book_treeview(book_frame); self.books_tree.pack(fill="both", expand=True, pady=5)
        self.books_tree.bind("<<TreeviewSelect>>", self.on_book_select)
        self.load_books_for_admin()

    def _setup_user_treeview(self, parent_frame):
        columns = ("ID", "Username"); 
        tree = ttk.Treeview(parent_frame, columns=columns, show="headings", selectmode="browse", height=5)
        # ✅ CORRECCIÓN 3: Usar cadenas literales para 'anchor'
        tree.heading("ID", text="ID", anchor='center'); tree.column("ID", width=80, anchor='center')
        tree.heading("Username", text="Username"); tree.column("Username", width=250, anchor='w')
        return tree
        
    def _setup_book_treeview(self, parent_frame):
        columns = ("ID", "Título", "ISBN", "Disp.")
        tree = ttk.Treeview(parent_frame, columns=columns, show="headings", selectmode="browse")
        # ✅ CORRECCIÓN 3: Usar cadenas literales para 'anchor'
        config = [("ID", 50, 'center'), ("Título", 250, 'w'), ("ISBN", 120, 'w'), ("Disp.", 60, 'center')]
        for name, width, anchor in config:
            tree.heading(name, text=name, anchor=anchor); tree.column(name, width=width, anchor=anchor)
        return tree

    # --- Lógica de Usuarios ---
    def load_users(self):
        self.users_tree.delete(*self.users_tree.get_children())
        users = self.user_manager.list_users()
        if not users: self.users_tree.insert("", tk.END, values=("—", "No hay usuarios registrados.")); return
        for user in users: self.users_tree.insert("", tk.END, values=(user[0], user[1]))

    # ✅ FUNCIÓN ACTUALIZADA: Llama a la pantalla dedicada UserFormScreen
    def open_add_user_screen(self): 
        UserFormScreen(self.master, self.db_manager, self.load_users)

    def delete_user_ui(self):
        selected_item = self.users_tree.focus()
        if not selected_item: return messagebox.showwarning("Advertencia", "Seleccione un usuario.")
        user_values = self.users_tree.item(selected_item, 'values')
        
        if user_values[0] == '—': return messagebox.showwarning("Advertencia", "Seleccione un usuario válido.")
        
        user_id = int(user_values[0]); username = user_values[1]
        
        if messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que desea eliminar (Soft Delete) a '{username}'?"):
            if self.user_manager.delete_user(user_id):
                messagebox.showinfo("Éxito", f"Usuario '{username}' marcado como eliminado.")
                self.load_users()
            else:
                messagebox.showerror("Error", "No se pudo marcar el usuario como eliminado.")

    # --- Lógica de Libros (CRUD) ---
    
    def on_book_select(self, event):
        selected_item = self.books_tree.selection()
        if selected_item:
            self.selected_book_data = self.books_tree.item(selected_item, 'values')
        else:
            self.selected_book_data = None
            
    def load_books_for_admin(self):
        self.books_tree.delete(*self.books_tree.get_children())
        
        books = self.book_manager.list_books()

        if not books: return
        for book in books:
            book_id, title, isbn, _, _, available = book
            status = "SÍ" if available == 1 else "NO"
            self.books_tree.insert("", tk.END, values=(book_id, title, isbn, status))

    # ✅ FUNCIÓN ACTUALIZADA: Llama a la pantalla dedicada BookFormScreen (Modo Agregar)
    def open_add_book_screen(self):
        BookFormScreen(self.master, self.db_manager, callback_on_success=self.load_books_for_admin) 
    
    # ✅ FUNCIÓN ACTUALIZADA: Llama a la pantalla dedicada BookFormScreen (Modo Editar)
    def open_edit_book_screen(self):
        if not self.selected_book_data: return messagebox.showwarning("Advertencia", "Seleccione un libro para editar.")
        
        if self.selected_book_data[0] == '—': return messagebox.showwarning("Advertencia", "Seleccione un libro válido.")

        book_id = int(self.selected_book_data[0])
        
        # Obtener los datos completos del libro para rellenar el formulario
        book_full_data = self.db_manager.select_one(
            "SELECT id, title, isbn, author, category FROM books WHERE id = ?;", 
            (book_id,)
        )

        if book_full_data:
            BookFormScreen(self.master, self.db_manager, book_data=book_full_data, callback_on_success=self.load_books_for_admin)
        else:
            messagebox.showerror("Error", "No se encontraron los datos completos del libro.")

    def delete_book_ui(self):
        if not self.selected_book_data: return messagebox.showwarning("Advertencia", "Seleccione un libro para eliminar.")
        
        if self.selected_book_data[0] == '—': return messagebox.showwarning("Advertencia", "Seleccione un libro válido.")
            
        book_id = int(self.selected_book_data[0]); title = self.selected_book_data[1]; available_status = self.selected_book_data[3]

        if available_status == "NO": return messagebox.showerror("Error", "No se puede eliminar un libro que está prestado.")
        
        if messagebox.askyesno("Confirmar Eliminación", 
                                f"¿Seguro de realizar el soft delete del libro '{title}' (ID: {book_id})?"):
            if self.book_manager.delete_book(book_id):
                messagebox.showinfo("Éxito", f"Libro '{title}' marcado como eliminado.")
                self.load_books_for_admin()
            else:
                messagebox.showerror("Error", "No se pudo marcar el libro como eliminado.")