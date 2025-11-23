import customtkinter as ctk
from tkinter import messagebox

class LoanView(ctk.CTkFrame):
    """Vista para gestionar préstamos y devoluciones de libros."""

    def __init__(self, parent, book_class):
        """
        Inicializa la vista de préstamos.

        Args:
            parent: frame padre donde se incrusta.
            book_class: instancia de la clase Book.
        """
        super().__init__(parent)
        self.book_class = book_class

        # Variables
        self.loan_book_id_var = ctk.StringVar()
        self.loan_user_id_var = ctk.StringVar()

        # Entradas
        ctk.CTkLabel(self, text="ID Libro").grid(row=0, column=0, padx=5, pady=5)
        self.loan_book_entry = ctk.CTkEntry(self, textvariable=self.loan_book_id_var)
        self.loan_book_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(self, text="ID Usuario").grid(row=1, column=0, padx=5, pady=5)
        self.loan_user_entry = ctk.CTkEntry(self, textvariable=self.loan_user_id_var)
        self.loan_user_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botones
        self.lend_btn = ctk.CTkButton(self, text="Prestar Libro", command=self.lend_book)
        self.lend_btn.grid(row=2, column=0, padx=5, pady=5)
        self.return_btn = ctk.CTkButton(self, text="Devolver Libro", command=self.return_book)
        self.return_btn.grid(row=2, column=1, padx=5, pady=5)


    def lend_book(self):
        """Realiza préstamo de un libro a un usuario validando IDs."""
        try:
            book_id = int(self.loan_book_id_var.get())
            user_id = int(self.loan_user_id_var.get())
        except ValueError:
            messagebox.showerror("Error", "IDs inválidos")
            return
        if self.book_class.lend(book_id, user_id):
            messagebox.showinfo("Éxito", "Libro prestado")
        else:
            messagebox.showerror("Error", "No se pudo prestar")


    def return_book(self):
        """Registra la devolución de un libro validando ID."""
        try:
            book_id = int(self.loan_book_id_var.get())
        except ValueError:
            messagebox.showerror("Error", "ID inválido")
            return
        if self.book_class.return_book(book_id):
            messagebox.showinfo("Éxito", "Libro devuelto")
        else:
            messagebox.showerror("Error", "No se pudo devolver")
