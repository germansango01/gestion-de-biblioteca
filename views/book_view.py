import customtkinter as ctk
from tkinter import messagebox

class BookView(ctk.CTkFrame):
    """Vista para gestionar libros: agregar, actualizar, eliminar, soft delete."""

    def __init__(self, parent, book_class, user_class):
        """
        Inicializa la vista de libros.

        Args:
            parent: frame padre donde se incrusta.
            book_class: instancia de la clase Book.
            user_class: instancia de la clase User.
        """
        super().__init__(parent)
        self.book_class = book_class
        self.user_class = user_class

        # Variables
        self.book_id_var = ctk.StringVar()
        self.book_title_var = ctk.StringVar()
        self.book_isbn_var = ctk.StringVar()
        self.book_author_var = ctk.StringVar()
        self.book_category_var = ctk.StringVar()

        # Entradas
        ctk.CTkLabel(self, text="ID").grid(row=0, column=0, padx=5, pady=5)
        self.book_id_entry = ctk.CTkEntry(self, textvariable=self.book_id_var, state="readonly")
        self.book_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(self, text="Título").grid(row=1, column=0, padx=5, pady=5)
        self.book_title_entry = ctk.CTkEntry(self, textvariable=self.book_title_var)
        self.book_title_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self, text="ISBN").grid(row=2, column=0, padx=5, pady=5)
        self.book_isbn_entry = ctk.CTkEntry(self, textvariable=self.book_isbn_var)
        self.book_isbn_entry.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(self, text="Autor").grid(row=3, column=0, padx=5, pady=5)
        self.book_author_entry = ctk.CTkEntry(self, textvariable=self.book_author_var)
        self.book_author_entry.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkLabel(self, text="Categoría").grid(row=4, column=0, padx=5, pady=5)
        self.book_category_entry = ctk.CTkEntry(self, textvariable=self.book_category_var)
        self.book_category_entry.grid(row=4, column=1, padx=5, pady=5)

        # Botones
        self.add_btn = ctk.CTkButton(self, text="Agregar", command=self.add_book)
        self.add_btn.grid(row=5, column=0, padx=5, pady=5)
        self.update_btn = ctk.CTkButton(self, text="Actualizar", command=self.update_book)
        self.update_btn.grid(row=5, column=1, padx=5, pady=5)
        self.delete_btn = ctk.CTkButton(self, text="Eliminar", command=self.delete_book)
        self.delete_btn.grid(row=5, column=2, padx=5, pady=5)

        # Lista de libros
        self.books_listbox = ctk.CTkTextbox(self, width=700, height=300)
        self.books_listbox.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
        self.books_listbox.bind("<ButtonRelease-1>", self.select_book_from_list)

        self.refresh_books()

    def refresh_books(self):
        """Actualiza la lista de libros activos."""
        self.books_listbox.delete("1.0", "end")
        books = self.book_class.list()
        for b in books:
            self.books_listbox.insert("end", f"{b[0]} | {b[1]} | {b[2]} | {b[3]} | {b[4]} | {'Disponible' if b[5] else 'Prestado'}\n")


    def select_book_from_list(self, event=None):
        """Llena los campos con el libro seleccionado de la lista."""
        try:
            line = self.books_listbox.get("current linestart", "current lineend").strip()
            if not line:
                return
            book_data = line.split("|")
            self.book_id_var.set(book_data[0].strip())
            self.book_title_var.set(book_data[1].strip())
            self.book_isbn_var.set(book_data[2].strip())
            self.book_author_var.set(book_data[3].strip())
            self.book_category_var.set(book_data[4].strip())
        except Exception:
            pass


    def add_book(self):
        """Agrega un libro validando los campos obligatorios."""
        title = self.book_title_var.get()
        isbn = self.book_isbn_var.get()
        author = self.book_author_var.get()
        category = self.book_category_var.get()
        if not title or not isbn or not author or not category:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        if self.book_class.add(title, isbn, author, category):
            messagebox.showinfo("Éxito", "Libro agregado")
            self.refresh_books()
        else:
            messagebox.showerror("Error", "No se pudo agregar el libro")


    def update_book(self):
        """Actualiza el libro seleccionado validando los campos."""
        try:
            book_id = int(self.book_id_var.get())
        except ValueError:
            messagebox.showerror("Error", "Seleccione un libro válido")
            return
        title = self.book_title_var.get()
        isbn = self.book_isbn_var.get()
        author = self.book_author_var.get()
        category = self.book_category_var.get()
        if not title or not isbn or not author or not category:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        if self.book_class.update(book_id, title, isbn, author, category):
            messagebox.showinfo("Éxito", "Libro actualizado")
            self.refresh_books()
        else:
            messagebox.showerror("Error", "No se pudo actualizar")


    def delete_book(self):
        """Realiza soft delete del libro seleccionado."""
        try:
            book_id = int(self.book_id_var.get())
        except ValueError:
            messagebox.showerror("Error", "Seleccione un libro válido")
            return
        if self.book_class.soft_delete(book_id):
            messagebox.showinfo("Éxito", "Libro eliminado (soft delete)")
            self.refresh_books()
        else:
            messagebox.showerror("Error", "No se pudo eliminar")
