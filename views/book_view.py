import customtkinter as ctk
from tkinter import ttk, messagebox
from clases.book import Book
from views.forms.book_form import BookForm

class BookView(ctk.CTkFrame):
    """
    Vista de libros que muestra un Treeview con operaciones básicas:
    crear, listar y borrar (soft delete), con columnas optimizadas.
    """

    def __init__(self, master, db):
        """
        Inicializa la vista de libros y construye la interfaz.

        Args:
            master: Widget padre donde se insertará este frame.
            db: Conexión o gestor de base de datos que usará Book.
        """
        super().__init__(master)
        self.manager = Book(db)

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Configuración de estilos para encabezado ---
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
        ctk.CTkButton(frame_btn, text="Nuevo Libro", command=self.open_form).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(frame_btn, text="🔄 Refrescar", command=self.refresh).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(frame_btn, text="Borrar Libro", command=self.delete, fg_color="red").pack(side="right", padx=5, pady=5)

        # --- Configuración del Treeview ---
        cols = ("ID", "Titulo", "ISBN", "Autor", "Categoría", "Disponible")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")

        self.tree.column("ID", width=50, anchor="center", stretch=False)
        self.tree.heading("ID", text="ID")

        self.tree.column("Titulo", width=220, anchor="w")
        self.tree.heading("Titulo", text="Titulo")

        self.tree.column("ISBN", width=150, anchor="center")
        self.tree.heading("ISBN", text="ISBN")

        self.tree.column("Autor", width=180, anchor="w")
        self.tree.heading("Autor", text="Autor")

        self.tree.column("Categoría", width=140, anchor="w")
        self.tree.heading("Categoría", text="Categoría")

        self.tree.column("Disponible", width=80, anchor="center", stretch=False)
        self.tree.heading("Disponible", text="Disponible")

        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Cargar datos
        self.refresh()


    def refresh(self):
        """
        Refresca la lista de libros en el Treeview.
        """
        self.tree.delete(*self.tree.get_children())
        for row in self.manager.list():
            vals = list(row)
            vals[5] = "Si" if vals[5] else "No"
            self.tree.insert("", "end", values=vals)


    def open_form(self):
        """
        Abre el formulario para crear/editar un libro.
        """
        BookForm(self, self.manager, self.refresh)


    def delete(self):
        """
        Elimina (soft delete) el libro actualmente seleccionado.
        """
        sel = self.tree.selection()
        if sel:
            bid = self.tree.item(sel[0])['values'][0]  # ID sigue accesible aunque oculto
            if messagebox.askyesno("Confirmar", "¿Borrar libro?"):
                self.manager.soft_delete(int(bid))
                self.refresh()
