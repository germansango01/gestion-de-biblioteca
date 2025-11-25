import customtkinter as ctk
from tkinter import ttk, messagebox
from clases.user import User
from views.forms.user_form import UserForm

class UserView(ctk.CTkFrame):
    """
    Vista de usuarios que permite crear, listar y borrar (soft delete) usuarios.
    """
    def __init__(self, master, db):
        super().__init__(master)
        self.manager = User(db)

        # Configuración del layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Estilos encabezado.
        style = ttk.Style()
        style.map("Treeview.Heading",
                background=[('active', '#D6D6D6')],
                foreground=[('active', 'black')])
        style.configure("Treeview.Heading",
                        font=('Arial', 10, 'bold'),
                        background='#EDEDED',
                        foreground='black')

        # Frame de botones.
        frame_btn = ctk.CTkFrame(self)
        frame_btn.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        ctk.CTkButton(frame_btn, text="Nuevo Usuario", command=self.open_form).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(frame_btn, text="🔄 Refrescar", command=self.refresh).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(frame_btn, text="Borrar Seleccionado", command=self.delete, fg_color="red", hover_color="#A00116", text_color="white").pack(side="right", padx=5, pady=5)

        # Configuración del Treeview.
        cols = ("ID", "Username", "Email")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")

        self.tree.column("ID", width=0, minwidth=0, stretch=False)
        self.tree.heading("ID", text="")

        self.tree.column("Username", width=200, anchor="w")
        self.tree.heading("Username", text="Usuario")

        self.tree.column("Email", width=250, anchor="w")
        self.tree.heading("Email", text="Correo Electrónico")

        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Cargar datos
        self.refresh()


    def refresh(self):
        """
        Carga y actualiza la tabla de usuarios.
        """
        self.tree.delete(*self.tree.get_children())
        for row in self.manager.list():
            self.tree.insert("", "end", values=row)


    def open_form(self):
        """
        Abre el formulario para crear/editar un usuario.
        """
        UserForm(self, self.manager, self.refresh)


    def delete(self):
        """
        Elimina (soft delete) el usuario seleccionado.
        """
        sel = self.tree.selection()
        if sel:
            uid = self.tree.item(sel[0])['values'][0]
            if messagebox.askyesno("Confirmar", "¿Borrar usuario?"):
                self.manager.soft_delete(int(uid))
                self.refresh()
