import tkinter as tk
from tkinter import messagebox
from clases.books import Book
from clases.users import User # Necesario para buscar ID
from clases.history import History # Necesario para actualizar listas

class BookView(tk.Frame):
    """Interfaz para Agregar, Listar, Prestar y Devolver Libros."""
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.book_manager = Book(db_manager)
        self.user_manager = User(db_manager)
        self.history_manager = History(db_manager)
        
        # Variables de entrada
        self.title_var = tk.StringVar()
        self.isbn_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.loan_user_var = tk.StringVar()
        
        self.selected_book_id = None # Almacena el ID del libro seleccionado en la Listbox
        
        self.create_widgets()
        self.load_books()

    def create_widgets(self):
        # Frame principal dividido
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # --- Columna 1: Agregar Libro ---
        add_frame = tk.LabelFrame(main_frame, text="Agregar Libro", padx=10, pady=10)
        add_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")

        fields = [("Título:", self.title_var), ("ISBN:", self.isbn_var), ("Autor:", self.author_var)]
        for i, (text, var) in enumerate(fields):
            tk.Label(add_frame, text=text).grid(row=i, column=0, sticky="w", pady=2)
            tk.Entry(add_frame, textvariable=var, width=25).grid(row=i, column=1, padx=5, pady=2)
            
        tk.Button(add_frame, text="✅ Agregar Libro", command=self.add_book_ui, 
                  bg="green", fg="white").grid(row=len(fields), column=0, columnspan=2, pady=10)

        # --- Columna 2: Préstamo/Devolución ---
        loan_frame = tk.LabelFrame(main_frame, text="Gestión de Préstamo", padx=10, pady=10)
        loan_frame.grid(row=0, column=1, padx=5, pady=5, sticky="n")

        tk.Label(loan_frame, text="Username del Prestatario:").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(loan_frame, textvariable=self.loan_user_var, width=25).grid(row=0, column=1, padx=5, pady=5)

        self.selected_label = tk.Label(loan_frame, text="Libro Seleccionado: Ninguno", fg="blue", wraplength=200)
        self.selected_label.grid(row=1, column=0, columnspan=2, pady=5)

        tk.Button(loan_frame, text="➡️ Prestar", command=self.lend_book_ui, 
                  bg="#2196F3", fg="white").grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        tk.Button(loan_frame, text="⬅️ Devolver", command=self.return_book_ui, 
                  bg="#FF5722", fg="white").grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # --- Fila 1: Listado de Libros ---
        list_frame = tk.LabelFrame(main_frame, text="Libros en Stock (ID | Título | Autor | ISBN | Disp.)", padx=10, pady=5)
        list_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        
        self.books_listbox = tk.Listbox(list_frame, height=15)
        self.books_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        self.books_listbox.bind("<<ListboxSelect>>", self.on_book_select)
        
        scrollbar = tk.Scrollbar(list_frame, command=self.books_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.books_listbox.config(yscrollcommand=scrollbar.set)
        
    def on_book_select(self, event):
        """Captura la selección de la Listbox y actualiza el ID seleccionado."""
        try:
            selection = self.books_listbox.curselection()
            if selection:
                # Obtener el texto completo de la línea seleccionada
                line = self.books_listbox.get(selection[0])
                # El ID es el primer elemento (asumimos que siempre está)
                self.selected_book_id = int(line.split('|')[0].strip())
                title = line.split('|')[1].strip()
                self.selected_label.config(text=f"Libro Seleccionado: {title} (ID: {self.selected_book_id})")
        except Exception:
            self.selected_book_id = None
            self.selected_label.config(text="Libro Seleccionado: Ninguno")

    def add_book_ui(self):
        title = self.title_var.get()
        isbn = self.isbn_var.get()
        author = self.author_var.get() or None
        
        if self.book_manager.add_book(title, isbn, author):
            self.load_books()
        else:
            messagebox.showerror("Error", "No se pudo agregar el libro.")

    def lend_book_ui(self):
        if not self.selected_book_id:
            messagebox.showwarning("Advertencia", "Seleccione un libro para prestar.")
            return
        username = self.loan_user_var.get()
        if not username:
            messagebox.showwarning("Advertencia", "Ingrese el Username del prestatario.")
            return

        # Buscar ID del usuario (usamos SELECT directo ya que authenticate pide pass)
        user_check = self.book_manager.db.execute_query("SELECT id FROM users WHERE username = ?", (username,))
        
        if not user_check:
            messagebox.showerror("Error", f"El usuario '{username}' no existe.")
            return
            
        user_id = user_check[0][0]

        if self.book_manager.lend_book(self.selected_book_id, user_id):
            messagebox.showinfo("Éxito", f"Libro ID {self.selected_book_id} prestado a {username}.")
            self.loan_user_var.set("")
            self.selected_book_id = None
            self.selected_label.config(text="Libro Seleccionado: Ninguno")
            self.load_books()
        else:
            messagebox.showerror("Error", "El libro ya está prestado o error de DB.")

    def return_book_ui(self):
        if not self.selected_book_id:
            messagebox.showwarning("Advertencia", "Seleccione un libro para devolver.")
            return

        if self.book_manager.return_book(self.selected_book_id):
            messagebox.showinfo("Éxito", f"Libro ID {self.selected_book_id} devuelto y disponible.")
            self.selected_book_id = None
            self.selected_label.config(text="Libro Seleccionado: Ninguno")
            self.load_books()
        else:
            messagebox.showerror("Error", "El libro no estaba prestado o error de DB.")

    def load_books(self):
        self.books_listbox.delete(0, tk.END)
        books = self.book_manager.list_books()
        
        if not books:
             self.books_listbox.insert(tk.END, "No hay libros registrados.")
             return

        for book in books:
            book_id, title, isbn, author, category, available = book
            status = "SÍ" if available == 1 else "NO"
            
            line = f"{book_id:<5} | {title[:30]:<30} | {author[:20]:<20} | {isbn:<15} | Disp.: {status}"
            self.books_listbox.insert(tk.END, line)