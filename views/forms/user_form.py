import tkinter as tk
from tkinter import messagebox, ttk
# Asumo que la clase User está en la carpeta 'clases'
from clases.users import User

class UserFormScreen(tk.Toplevel):
    """Pantalla Toplevel dedicada para crear un usuario."""
    
    def __init__(self, master, db_manager, callback_on_success=None):
        super().__init__(master)
        self.title("👤 Crear Nuevo Usuario"); 
        
        # Configuración para que sea un modal
        self.transient(master); self.grab_set()
        
        self.user_manager = User(db_manager)
        self.callback_on_success = callback_on_success
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        self.create_widgets(); self.focus_set()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="15"); main_frame.pack(fill="both", expand=True)
        ttk.Label(main_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable=self.username_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(main_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=30).grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(main_frame, text="✅ Registrar Usuario", command=self.create_user_ui, style='Accent.TButton').grid(
            row=2, column=0, columnspan=2, pady=15, sticky="ew")

    def create_user_ui(self):
        username = self.username_var.get().strip(); password = self.password_var.get().strip()
        if not username or not password: return messagebox.showerror("Error", "Ambos campos son obligatorios.", parent=self)

        if self.user_manager.create_user(username, password):
            messagebox.showinfo("Éxito", f"Usuario '{username}' creado.", parent=self)
            self.username_var.set(""); self.password_var.set("")
            
            if self.callback_on_success: # ✅ CORRECCIÓN 1: Verificación de callback
                self.callback_on_success()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario (posiblemente ya existe).", parent=self)