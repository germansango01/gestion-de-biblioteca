import tkinter as tk
from tkinter import messagebox, ttk
# Asumo que la clase Book está en la carpeta 'clases'
from clases.books import Book 
# NOTA: La lógica de AddBookModal se movió a views.forms.book_form.BookFormScreen

class BookView(tk.Frame):
    """Interfaz principal para listar el catálogo de libros (Solo Lectura)."""
    
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.db_manager = db_manager
        self.book_manager = Book(db_manager)
        self.create_widgets()
        self.load_books()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10"); main_frame.pack(fill="both", expand=True)
        control_frame = ttk.Frame(main_frame); control_frame.pack(fill="x", pady=5)
        
        ttk.Label(control_frame, text="Catálogo Completo de Libros", font=("Arial", 14, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🔄 Recargar Catálogo", command=self.load_books).pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.books_tree = self._setup_treeview(main_frame); self.books_tree.pack(fill="both", expand=True, pady=5)
        
    def _setup_treeview(self, parent_frame):
        columns = ("ID", "Título", "ISBN", "Autor", "Categoría", "Disp.")
        tree = ttk.Treeview(parent_frame, columns=columns, show="headings", selectmode="browse")
        
        # ✅ CORRECCIÓN 3: Usar cadenas literales para 'anchor'
        config = [("ID", 40, 'center'), ("Título", 200, 'w'), ("ISBN", 100, 'w'), 
                ("Autor", 150, 'w'), ("Categoría", 100, 'w'), ("Disp.", 50, 'center')]
        
        for name, width, anchor in config:
            tree.heading(name, text=name.replace('.', '').replace('Disp', 'Disp.'), anchor=anchor)
            tree.column(name, width=width, anchor=anchor)
        
        tree.tag_configure('disponible', background='#e6ffe6', foreground='green')
        tree.tag_configure('prestado', background='#ffeeee', foreground='red')
        
        vsb = ttk.Scrollbar(parent_frame, orient="vertical", command=tree.yview); vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)
        
        return tree

    def load_books(self):
        self.books_tree.delete(*self.books_tree.get_children())
        books = self.book_manager.list_books()
        
        if not books: 
            self.books_tree.insert("", tk.END, values=("—", "No hay libros registrados.", "—", "—", "—", "—")); return

        for book in books:
            book_id, title, isbn, author_name, category, available = book 
            status = "SÍ" if available == 1 else "NO"
            tag = 'disponible' if available == 1 else 'prestado'
            
            self.books_tree.insert("", tk.END, 
                                values=(book_id, title, isbn, author_name, category, status), 
                                tags=(tag,))