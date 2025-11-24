import customtkinter as ctk
import re
from tkinter import messagebox

class UserForm(ctk.CTkToplevel):
    """
    Formulario modal para añadir nuevos usuarios con validación de email y password en la interfaz.
    """
    
    # Patrón básico para validar email
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def __init__(self, master, user_manager, refresh_callback):
        super().__init__(master)
        self.title("Nuevo Usuario")
        self.geometry("450x350")
        self.manager = user_manager
        self.callback = refresh_callback
        self.grab_set()

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=3) 

        self.entries = {}
        self.errors = {}
        
        fields = ["username", "email", "password"]
        
        row_counter = 0
        for f in fields:
            ctk.CTkLabel(self, text=f.capitalize() + ":").grid(
                row=row_counter, column=0, padx=(20, 5), pady=(15, 0), sticky="w"
            )
            
            show_char = '*' if f == "password" else None
            self.entries[f] = ctk.CTkEntry(self, width=250, show=show_char)
            self.entries[f].grid(
                row=row_counter, column=1, padx=(5, 20), pady=(15, 0), sticky="ew"
            )
            row_counter += 1
            
            self.errors[f] = ctk.CTkLabel(self, text="", text_color="red")
            self.errors[f].grid(
                row=row_counter, column=0, columnspan=2, padx=20, pady=(0, 5), sticky="w"
            )
            row_counter += 1

        ctk.CTkButton(self, text="Guardar", command=self.save).grid(
            row=row_counter, column=0, columnspan=2, pady=20
        )


    def _validate_ui(self, data: dict) -> dict:
        """
        Realiza la validación de la interfaz (no vacíos, email y password).
        """
        ui_errors = {}
        
        # 1. Validación de campos no vacíos
        for key, value in data.items():
            if not value.strip():
                ui_errors[key] = f"El campo '{key.capitalize()}' es obligatorio."

        # 2. Validación de formato de Email
        email = data.get('email', '').strip()
        if 'email' not in ui_errors and email:
            if not re.match(self.EMAIL_REGEX, email):
                ui_errors['email'] = "Formato de email inválido."

        # 3. Validación de Password (Mínimo de caracteres)
        password = data.get('password', '').strip()
        if 'password' not in ui_errors and len(password) < 6:
            ui_errors['password'] = "La contraseña debe tener al menos 6 caracteres."
        
        return ui_errors


    def save(self):
        data = {k: v.get() for k, v in self.entries.items()}
        for lbl in self.errors.values(): 
            lbl.configure(text="")

        ui_errors = self._validate_ui(data)
        
        if ui_errors:
            for k, v in ui_errors.items():
                if k in self.errors: 
                    self.errors[k].configure(text=v)
            return

        # Llama a la capa de negocio
        res = self.manager.create(data['username'], data['email'], data['password'])
        
        if res is True:
            self.callback()
            self.destroy()
        elif isinstance(res, dict):
            # Fallo en la capa de negocio (ej. Username o Email duplicado)
            for k, v in res.items():
                if k in self.errors:
                    self.errors[k].configure(text=v)
                else:
                    messagebox.showerror("Error de Negocio", f"Error desconocido: {v}")