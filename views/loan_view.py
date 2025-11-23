import customtkinter as ctk
from tkinter import messagebox

class LoanView(ctk.CTkFrame):
    """Vista para gestionar préstamos y devoluciones de libros."""

    def __init__(self, master, book_class):
        """
        Inicializa la vista de préstamos.

        Args:
            master: contenedor padre.
            book_class (Book): instancia de la clase Book.
        """
        super().__init__(master)
        self.book_class = book_class

        # Widgets
        self.book_id_entry = ctk.CTkEntry(self, placeholder_text="ID Libro")
        self.user_id_entry = ctk.CTkEntry(self, placeholder_text="ID Usuario")
        self.lend_btn = ctk.CTkButton(self, text="Prestar Libro", command=self.lend_book)
        self.return_btn = ctk.CTkButton(self, text="Devolver Libro", command=self.return_book)
        self.refresh_btn = ctk.CTkButton(self, text="Actualizar Lista", command=self.refresh_loans)
        self.listbox = ctk.CTkTextbox(self, width=600, height=300)

        # Layout
        self.book_id_entry.grid(row=0, column=0, padx=5, pady=5)
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.lend_btn.grid(row=1, column=0, padx=5, pady=5)
        self.return_btn.grid(row=1, column=1, padx=5, pady=5)
        self.refresh_btn.grid(row=1, column=2, padx=5, pady=5)
        self.listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.refresh_loans()


    def lend_book(self):
        """Realiza un préstamo con los IDs ingresados."""
        try:
            book_id = int(self.book_id_entry.get())
            user_id = int(self.user_id_entry.get())
        except ValueError:
            messagebox.showerror("Error", "IDs inválidos")
            return

        if self.book_class.lend(book_id, user_id):
            messagebox.showinfo("Éxito", "Libro prestado")
            self.refresh_loans()
        else:
            messagebox.showerror("Error", "No se pudo prestar el libro")


    def return_book(self):
        """Registra la devolución del libro ingresado por ID."""
        try:
            book_id = int(self.book_id_entry.get())
        except ValueError:
            messagebox.showerror("Error", "ID inválido")
            return

        if self.book_class.return_book(book_id):
            messagebox.showinfo("Éxito", "Libro devuelto")
            self.refresh_loans()
        else:
            messagebox.showerror("Error", "No se pudo devolver el libro")


    def refresh_loans(self):
        """Actualiza la lista de préstamos activos."""
        self.listbox.delete("1.0", "end")
        books = self.book_class.list(available_only=False)
        for b in books:
            status = "Disponible" if b[5] == 1 else "Prestado"
            self.listbox.insert("end", f"ID:{b[0]} Título:{b[1]} Estado:{status}\n")
