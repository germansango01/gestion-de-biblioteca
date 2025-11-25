import customtkinter as ctk
from tkinter import ttk, messagebox
from clases.loan import Loan
from clases.book import Book
from clases.user import User
from views.forms.loan_form import LoanForm

class LoanView(ctk.CTkFrame):
    """
    Maneja el registro de nuevos préstamos y la gestión de devoluciones.
    """

    def __init__(self, master, db):
        super().__init__(master)
        self.loan_mgr = Loan(db)
        self.book_mgr = Book(db)
        self.user_mgr = User(db)

        # Layout responsivo
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Estilos encabezado ---
        style = ttk.Style()
        style.map("Treeview.Heading",
                background=[('active', '#D6D6D6')],
                foreground=[('active', 'black')])
        style.configure("Treeview.Heading",
                        font=('Arial', 10, 'bold'),
                        background='#EDEDED',
                        foreground='black')

        # Frame de botones
        frame_btn = ctk.CTkFrame(self)
        frame_btn.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        ctk.CTkButton(frame_btn, text="Nuevo Préstamo", command=self.open_form).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(frame_btn, text="🔄 Refrescar", command=self.refresh).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(frame_btn, text="Devolver Libro", command=self.return_book, fg_color="orange").pack(side="right", padx=5, pady=5)

        # --- Configuración del Treeview ---
        cols = ("ID", "Libro", "Usuario", "Fecha", "BookID")
        self.tree = ttk.Treeview(
            self,
            columns=cols,
            displaycolumns=("ID", "Libro", "Usuario", "Fecha"),  # ocultamos BookID
            show="headings"
        )

        # Columna oculta
        self.tree.column("BookID", width=0, minwidth=0, stretch=False)
        self.tree.heading("BookID", text="")

        # Columnas visibles con ancho y alineación
        self.tree.column("ID", width=60, anchor="center")
        self.tree.heading("ID", text="ID")

        self.tree.column("Libro", width=250, anchor="w")
        self.tree.heading("Libro", text="Libro")

        self.tree.column("Usuario", width=180, anchor="w")
        self.tree.heading("Usuario", text="Usuario")

        self.tree.column("Fecha", width=140, anchor="center")
        self.tree.heading("Fecha", text="Fecha Préstamo")

        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Cargar datos
        self.refresh()


    def refresh(self):
        """Carga y actualiza la tabla de préstamos activos."""
        self.tree.delete(*self.tree.get_children())
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
        book_id = vals[4]  # BookID oculto

        if messagebox.askyesno(
            "Devolución",
            f"¿Registrar la devolución del libro '{vals[1]}' prestado a '{vals[2]}'?"
        ):
            if self.loan_mgr.return_book(int(loan_id), int(book_id)):
                messagebox.showinfo("Éxito", "Devolución registrada correctamente.")
                self.refresh()
            else:
                messagebox.showerror("Error", "Fallo al registrar la devolución. Verifique si el préstamo ya fue cerrado.")
