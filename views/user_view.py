import customtkinter as ctk
from tkinter import messagebox

class UserView(ctk.CTkFrame):
    """Vista para gestionar usuarios: agregar, eliminar (soft delete) y listar."""

    def __init__(self, parent, user_class):
        """
        Inicializa la vista de usuarios.

        Args:
            parent: frame padre donde se incrusta.
            user_class: instancia de la clase User.
        """
        super().__init__(parent)
        self.user_class = user_class

        # Variables
        self.user_id_var = ctk.StringVar()
        self.user_name_var = ctk.StringVar()
        self.user_pass_var = ctk.StringVar()

        # Entradas
        ctk.CTkLabel(self, text="ID").grid(row=0, column=0, padx=5, pady=5)
        self.user_id_entry = ctk.CTkEntry(self, textvariable=self.user_id_var, state="readonly")
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(self, text="Usuario").grid(row=1, column=0, padx=5, pady=5)
        self.user_name_entry = ctk.CTkEntry(self, textvariable=self.user_name_var)
        self.user_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self, text="Contraseña").grid(row=2, column=0, padx=5, pady=5)
        self.user_pass_entry = ctk.CTkEntry(self, textvariable=self.user_pass_var)
        self.user_pass_entry.grid(row=2, column=1, padx=5, pady=5)

        # Botones
        self.add_btn = ctk.CTkButton(self, text="Agregar", command=self.add_user)
        self.add_btn.grid(row=3, column=0, padx=5, pady=5)
        self.delete_btn = ctk.CTkButton(self, text="Eliminar", command=self.delete_user)
        self.delete_btn.grid(row=3, column=1, padx=5, pady=5)
        self.refresh_btn = ctk.CTkButton(self, text="Actualizar Lista", command=self.refresh_users)
        self.refresh_btn.grid(row=3, column=2, padx=5, pady=5)

        # Lista de usuarios
        self.users_listbox = ctk.CTkTextbox(self, width=600, height=400)
        self.users_listbox.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.users_listbox.bind("<ButtonRelease-1>", self.select_user_from_list)

        self.refresh_users()


    def refresh_users(self):
        """Actualiza la lista de usuarios activos."""
        self.users_listbox.delete("1.0", "end")
        users = self.user_class.list()
        for u in users:
            self.users_listbox.insert("end", f"{u[0]} | {u[1]}\n")


    def select_user_from_list(self, event=None):
        """Llena los campos con el usuario seleccionado de la lista."""
        try:
            line = self.users_listbox.get("current linestart", "current lineend").strip()
            if not line:
                return
            user_data = line.split("|")
            self.user_id_var.set(user_data[0].strip())
            self.user_name_var.set(user_data[1].strip())
        except Exception:
            pass


    def add_user(self):
        """Agrega un usuario nuevo validando campos obligatorios."""
        username = self.user_name_var.get()
        password = self.user_pass_var.get()
        if not username or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        if self.user_class.create(username, password):
            messagebox.showinfo("Éxito", "Usuario agregado")
            self.refresh_users()
        else:
            messagebox.showerror("Error", "No se pudo agregar el usuario")


    def delete_user(self):
        """Realiza soft delete del usuario seleccionado."""
        try:
            user_id = int(self.user_id_var.get())
        except ValueError:
            messagebox.showerror("Error", "Seleccione un usuario válido")
            return
        if self.user_class.soft_delete(user_id):
            messagebox.showinfo("Éxito", "Usuario eliminado (soft delete)")
            self.refresh_users()
        else:
            messagebox.showerror("Error", "No se pudo eliminar")
