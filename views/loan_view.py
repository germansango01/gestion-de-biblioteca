import customtkinter as ctk
from tkinter import ttk, messagebox
from clases.loan import Loan
from clases.book import Book
from clases.user import User
from views.forms.loan_form import LoanForm

class LoanView(ctk.CTkFrame):
    """Maneja el registro de nuevos préstamos y la gestión de devoluciones."""
    def __init__(self, master, db):
        super().__init__(master)
        # Se necesita Loan para transacciones y Book/User para llenar formularios de préstamo.
        self.loan_mgr = Loan(db)
        self.book_mgr = Book(db)
        self.user_mgr = User(db)

        frame_btn = ctk.CTkFrame(self)
        frame_btn.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(frame_btn, text="Nuevo Préstamo", command=self.open_form).pack(side="left")
        ctk.CTkButton(frame_btn, text="Devolver Libro", command=self.return_book, fg_color="orange").pack(side="right")

        # Configuración de la tabla de Préstamos Activos
        # Se añade BookID oculto para facilitar la devolución
        self.tree = ttk.Treeview(self, columns=("ID", "Libro", "Usuario", "Fecha", "BookID"), displaycolumns=("ID", "Libro", "Usuario", "Fecha"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Libro", text="Libro")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Fecha", text="Fecha Préstamo")
        self.tree.column("ID", width=60, anchor='center')
        self.tree.column("BookID", width=0, stretch=False)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh()

    def refresh(self):
        """Carga y actualiza la tabla de préstamos activos."""
        self.tree.delete(*self.tree.get_children())
        # Usa el método get_active_loans de la clase Loan
        for row in self.loan_mgr.get_active_loans():
            self.tree.insert("", "end", values=row)

    def open_form(self):
        """Abre el formulario para registrar un nuevo préstamo."""
        LoanForm(self, self.loan_mgr, self.user_mgr, self.book_mgr, self.refresh)

    def return_book(self):
        """Procesa la devolución del préstamo seleccionado."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Advertencia", "Seleccione un préstamo activo de la tabla.")
            return

        vals = self.tree.item(sel[0])['values']
        loan_id = vals[0]
        book_id = vals[4] # Se extrae el BookID de la columna oculta
        
        if messagebox.askyesno("Devolución", f"¿Registrar la devolución del libro '{vals[1]}' prestado a '{vals[2]}'?"):
            if self.loan_mgr.return_book(int(loan_id), int(book_id)):
                messagebox.showinfo("Éxito", "Devolución registrada correctamente.")
                self.refresh()
            else:
                messagebox.showerror("Error", "Fallo al registrar la devolución. Verifique si el préstamo ya fue cerrado.")