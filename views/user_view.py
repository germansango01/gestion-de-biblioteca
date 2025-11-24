import customtkinter as ctk
from tkinter import ttk, messagebox
from clases.user import User
from views.forms.user_form import UserForm

class UserView(ctk.CTkFrame):

    def __init__(self, master, db):
        super().__init__(master)
        self.manager = User(db)

        # Botones
        frame_btn = ctk.CTkFrame(self)
        frame_btn.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(frame_btn, text="Nuevo Usuario", command=self.open_form).pack(side="left")
        ctk.CTkButton(frame_btn, text="Borrar Seleccionado", command=self.delete, fg_color="red").pack(side="right")

        # Tabla
        self.tree = ttk.Treeview(self, columns=("ID", "Username"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Username", text="Usuario")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh()


    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.manager.list():
            self.tree.insert("", "end", values=row)


    def open_form(self):
        UserForm(self, self.manager, self.refresh)


    def delete(self):
        sel = self.tree.selection()
        if sel:
            uid = self.tree.item(sel[0])['values'][0]
            if messagebox.askyesno("Confirmar", "¿Borrar usuario?"):
                self.manager.soft_delete(int(uid))
                self.refresh()