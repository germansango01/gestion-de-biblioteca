import customtkinter as ctk
from tkinter import messagebox

class BookView(ctk.CTkFrame):
    """Vista para gestionar libros: crear, actualizar, eliminar y listar."""

    def __init__(self, master, book_class, user_class):
        """
        Inicializa la vista de libros.

        Args:
            master: contenedor padre.
            book_class (Book): instancia de la clase Book.
            user_class (User): instancia de la clase User (para préstamos).
        """
        super().__init__(master)
        self.book_class = book_class
        self.user_class = user_class

        # Widgets
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Título")
        self.isbn_entry = ctk.CTkEntry(self, placeholder_text="ISBN")
        self.author_entry = ctk.CTkEntry(self, placeholder_text="Autor")
        self.category_entry = ctk.CTkEntry(self, placeholder_text="Categoría")

        self.add_btn = ctk.CTkButton(self, text="Agregar Libro", command=self.add_book)
        self.update_btn = ctk.CTkButton(self, text="Actualizar Libro", command=self.update_book)
        self.delete_btn = ctk.CTkButton(self, text="Eliminar Libro", command=self.delete_book)
        self.lend_btn = ctk.CTkButton(self, text="Prestar Libro", command=self.lend_book)
        self.return_btn = ctk.CTkButton(self, text="Devolver Libro", command=self.return_book)
        self.refresh_btn = ctk.CTkButton(self, text="Actualizar Lista", command=self.refresh_books)

        self.listbox = ctk.CTkTextbox(self, width=600, height=300)

        # Layout
        self.title_entry.grid(row=0, column=0, padx=5, pady=5)
        self.isbn_entry.grid(row=0, column=1, padx=5, pady=5)
        self.author_entry.grid(row=1, column=0, padx=5, pady=5)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_btn.grid(row=2, column=0, padx=5, pady=5)
        self.update_btn.grid(row=2, column=1, padx=5, pady=5)
        self.delete_btn.grid(row=2, column=2, padx=5, pady=5)
        self.lend_btn.grid(row=3, column=0, padx=5, pady=5)
        self.return_btn.grid(row=3, column=1, padx=5, pady=5)
        self.refresh_btn.grid(row=3, column=2, padx=5, pady=5)

        self.listbox.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        self.refresh_books()


    def add_book(self):
        """Agrega un libro con los datos ingresados en los campos."""
        if self.book_class.add(
            self.title_entry.get(),
            self.isbn_entry.get(),
            self.author_entry.get(),
            self.category_entry.get()
        ):
            messagebox.showinfo("Éxito", "Libro agregado correctamente")
            self.refresh_books()
        else:
            messagebox.showerror("Error", "No se pudo agregar el libro")


    def update_book(self):
        """Actualiza un libro seleccionado por ID en el primer campo (Título)."""
        try:
            book_id = int(self.title_entry.get())
        except ValueError:
            messagebox.showerror("Error", "ID inválido")
            return

        if self.book_class.update(
            book_id,
            self.title_entry.get(),
            self.isbn_entry.get(),
            self.author_entry.get(),
            self.category_entry.get()
        ):
            messagebox.showinfo("Éxito", "Libro actualizado")
            self.refresh_books()
        else:
            messagebox.showerror("Error", "No se pudo actualizar")


    def delete_book(self):
        """Elimina un libro por ID ingresado en el campo Título."""
        try:
            book_id = int(self.title_entry.get())
        except ValueError:
            messagebox.showerror("Error", "ID inválido")
            return

        if self.book_class.soft_delete(book_id):
            messagebox.showinfo("Éxito", "Libro eliminado")
            self.refresh_books()
        else:
            messagebox.showerror("Error", "No se pudo eliminar")


    def lend_book(self):
        """Presta un libro a un usuario: IDs ingresados en Título y Autor (Libro y Usuario)."""
        try:
            book_id = int(self.title_entry.get())
            user_id = int(self.author_entry.get())
        except ValueError:
            messagebox.showerror("Error", "IDs inválidos")
            return

        if self.book_class.lend(book_id, user_id):
            messagebox.showinfo("Éxito", "Libro prestado")
            self.refresh_books()
        else:
            messagebox.showerror("Error", "No se pudo prestar")


    def return_book(self):
        """Devuelve un libro por ID ingresado en el campo Título."""
        try:
            book_id = int(self.title_entry.get())
        except ValueError:
            messagebox.showerror("Error", "ID inválido")
            return

        if self.book_class.return_book(book_id):
            messagebox.showinfo("Éxito", "Libro devuelto")
            self.refresh_books()
        else:
            messagebox.showerror("Error", "No se pudo devolver")


    def refresh_books(self):
        """Actualiza la lista de libros en el textbox."""
        self.listbox.delete("1.0", "end")
        books = self.book_class.list()
        for b in books:
            self.listbox.insert("end", f"ID:{b[0]} Título:{b[1]} ISBN:{b[2]} Autor:{b[3]} Categoría:{b[4]} Disponible:{b[5]}\n")
