import customtkinter as ctk
from tkinter import messagebox

class UserView(ctk.CTkFrame):
    """Vista para gestionar usuarios: crear, listar y eliminar."""

    def __init__(self, master, user_class):
        """
        Inicializa la vista de usuarios.

        Args:
            master: contenedor padre.
            user_class (User): instancia de la clase User.
        """
        super().__init__(master)
        self.user_class = user_class

        # Widgets
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.add_btn = ctk.CTkButton(self, text="Agregar Usuario", command=self.add_user)
        self.delete_btn = ctk.CTkButton(self, text="Eliminar Usuario", command=self.delete_user)
        self.refresh_btn = ctk.CTkButton(self, text="Actualizar Lista", command=self.refresh_users)
        self.listbox = ctk.CTkTextbox(self, width=600, height=300)

        # Layout
        self.username_entry.grid(row=0, column=0, padx=5, pady=5)
        self.password_entry.grid(row=0, column=1, padx=5, pady=5)
        self.add_btn.grid(row=1, column=0, padx=5, pady=5)
        self.delete_btn.grid(row=1, column=1, padx=5, pady=5)
        self.refresh_btn.grid(row=1, column=2, padx=5, pady=5)
        self.listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.refresh_users()


    def add_user(self):
        """Crea un usuario con los datos ingresados."""
        if self.user_class.create(self.username_entry.get(), self.password_entry.get()):
            messagebox.showinfo("Éxito", "Usuario creado")
            self.refresh_users()
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario")


    def delete_user(self):
        """Elimina un usuario por ID ingresado en el campo Usuario."""
        try:
            user_id = int(self.username_entry.get())
        except ValueError:
            messagebox.showerror("Error", "ID inválido")
            return

        if self.user_class.soft_delete(user_id):
            messagebox.showinfo("Éxito", "Usuario eliminado")
            self.refresh_users()
        else:
            messagebox.showerror("Error", "No se pudo eliminar")


    def refresh_users(self):
        """Actualiza la lista de usuarios en el textbox."""
        self.listbox.delete("1.0", "end")
        users = self.user_class.list()
        for u in users:
            self.listbox.insert("end", f"ID:{u[0]} Usuario:{u[1]}\n")
