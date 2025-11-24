import customtkinter as ctk
import re
from tkinter import messagebox

class UserForm(ctk.CTkToplevel):
    """
    Formulario modal para añadir nuevos usuarios.
    """
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def __init__(self, master, user_manager, refresh_callback):
        super().__init__(master)
        self.title("Nuevo Usuario")
        self.geometry("450x350")
        self.manager = user_manager
        self.callback = refresh_callback
        self.grab_set()

        # Grid responsivo
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        self.entries = {}
        self.errors = {}

        # Label para errores generales
        self.general_error = ctk.CTkLabel(self, text="", text_color="red")
        self.general_error.grid(row=0, column=0, columnspan=2, padx=20, pady=(10,5), sticky="w")

        fields = ["username", "email", "password"]
        row_counter = 1

        for f in fields:
            ctk.CTkLabel(self, text=f.capitalize() + ":").grid(
                row=row_counter, column=0, padx=(20,5), pady=(10,0), sticky="w"
            )
            show_char = '*' if f == "password" else None
            self.entries[f] = ctk.CTkEntry(self, width=250, show=show_char)
            self.entries[f].grid(
                row=row_counter, column=1, padx=(5,20), pady=(10,0), sticky="ew"
            )
            row_counter += 1

            self.errors[f] = ctk.CTkLabel(self, text="", text_color="red")
            self.errors[f].grid(
                row=row_counter, column=0, columnspan=2, padx=20, pady=(0,5), sticky="w"
            )
            row_counter += 1

        ctk.CTkButton(self, text="Guardar", command=self.save).grid(
            row=row_counter, column=0, columnspan=2, pady=20, padx=20, sticky="ew"
        )


    def _validate_ui(self, data: dict) -> dict:
        """
        Valida que los campos no estén vacíos, el email tenga formato correcto y la contraseña tenga al menos 6 caracteres.
        """
        ui_errors = {}
        for key, value in data.items():
            if not value.strip():
                ui_errors[key] = f"El campo '{key.capitalize()}' es obligatorio."

        email = data.get('email', '').strip()
        if 'email' not in ui_errors and email:
            if not re.match(self.EMAIL_REGEX, email):
                ui_errors['email'] = "Formato de email inválido."

        password = data.get('password', '').strip()
        if 'password' not in ui_errors and len(password) < 6:
            ui_errors['password'] = "La contraseña debe tener al menos 6 caracteres."

        return ui_errors


    def save(self):
        """
        Valida y crea el usuario a través de la capa de negocio.
        """
        data = {k: v.get() for k,v in self.entries.items()}
        self.general_error.configure(text="")
        for lbl in self.errors.values():
            lbl.configure(text="")

        # Validación de UI
        ui_errors = self._validate_ui(data)
        if ui_errors:
            for k,v in ui_errors.items():
                if k in self.errors:
                    self.errors[k].configure(text=v)
            return

        # Validación de negocio
        res = self.manager.create(data['username'], data['email'], data['password'])
        if res is True:
            self.callback()
            self.destroy()
        elif isinstance(res, dict):
            for k,v in res.items():
                if k in self.errors:
                    self.errors[k].configure(text=v)
                else:
                    self.general_error.configure(text=str(v))
