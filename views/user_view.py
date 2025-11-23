import tkinter as tk
from tkinter import messagebox, ttk
from clases.users import User
from clases.database import DatabaseManager # Importar para tipificación

# ==============================================================================
# Modal para Crear Usuario
# ==============================================================================
class AddUserModal(tk.Toplevel):
    """Ventana modal para el formulario de crear usuario."""
    
    def __init__(self, master, db_manager, callback_on_success=None):
        super().__init__(master)
        self.title("👤 Crear Nuevo Usuario"); self.transient(master); self.grab_set()
        self.user_manager = User(db_manager); self.callback_on_success = callback_on_success
        self.username_var = tk.StringVar(); self.password_var = tk.StringVar()
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
        if not username or not password: messagebox.showerror("Error", "Ambos campos son obligatorios.", parent=self); return

        if self.user_manager.create_user(username, password):
            messagebox.showinfo("Éxito", f"Usuario '{username}' creado.", parent=self)
            self.username_var.set(""); self.password_var.set("")
            if self.callback_on_success: self.callback_on_success()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario (posiblemente ya existe).", parent=self)


# ==============================================================================
# Vista Principal de Usuarios
# ==============================================================================
class UserView(tk.Frame):
    """Interfaz principal para gestionar usuarios."""
    
    def __init__(self, master, db_manager):
        super().__init__(master); self.db_manager = db_manager; self.user_manager = User(db_manager)
        self.auth_user_var = tk.StringVar(); self.auth_pass_var = tk.StringVar()
        self.create_widgets(); self.load_users()


    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10"); main_frame.pack(fill="both", expand=True)
        control_frame = ttk.Frame(main_frame); control_frame.pack(fill="x", pady=10)
        ttk.Button(control_frame, text="➕ Nuevo Usuario", command=self.open_add_user_modal).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🔄 Recargar Usuarios", command=self.load_users).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🗑️ Eliminar Usuario (Soft Delete)", command=self.delete_user_ui, style='Danger.TButton').pack(side=tk.LEFT, padx=5) # Botón añadido para Soft Delete

        auth_frame = ttk.LabelFrame(main_frame, text="Probar Autenticación", padding="10"); auth_frame.pack(fill="x", pady=10)
        ttk.Label(auth_frame, text="Username:").grid(row=0, column=0, padx=5, sticky="w")
        ttk.Entry(auth_frame, textvariable=self.auth_user_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(auth_frame, text="Password:").grid(row=1, column=0, padx=5, sticky="w")
        ttk.Entry(auth_frame, textvariable=self.auth_pass_var, show="*", width=20).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(auth_frame, text="🔑 Autenticar", command=self.authenticate_ui, style='Accent.TButton').grid(row=0, column=2, rowspan=2, padx=15, sticky="ns")
        
        self.users_tree = self._setup_treeview(main_frame); self.users_tree.pack(fill="both", expand=True, pady=5)


    def _setup_treeview(self, parent_frame):
        columns = ("ID", "Username"); tree = ttk.Treeview(parent_frame, columns=columns, show="headings", selectmode="browse")
        tree.heading("ID", text="ID", anchor=tk.CENTER); tree.column("ID", width=80, anchor=tk.CENTER)
        tree.heading("Username", text="Username"); tree.column("Username", width=250)
        return tree


    def open_add_user_modal(self): 
        AddUserModal(self.master, self.db_manager, self.load_users)


    def authenticate_ui(self):
        username = self.auth_user_var.get().strip(); password = self.auth_pass_var.get().strip()
        if not username or not password: messagebox.showerror("Error", "Ingrese usuario y contraseña para autenticar."); return
        
        user_id = self.user_manager.authenticate(username, password)
        
        if user_id:
            messagebox.showinfo("Autenticación Exitosa", f"¡Bienvenido, {username}! ID: {user_id}")
            self.auth_user_var.set(""); self.auth_pass_var.set("")
        else:
            messagebox.showerror("Autenticación Fallida", "Usuario o contraseña incorrectos.")


    def delete_user_ui(self):
        """Maneja el Soft Delete del usuario seleccionado."""
        selected_item = self.users_tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar.")
            return

        user_values = self.users_tree.item(selected_item, 'values')
        user_id = int(user_values[0])
        username = user_values[1]

        if messagebox.askyesno("Confirmar Eliminación (Soft Delete)", 
                            f"¿Está seguro de marcar como eliminado al usuario '{username}'?\n"
                            "El historial de préstamos se preservará."):
            
            if self.user_manager.delete_user(user_id):
                messagebox.showinfo("Éxito", f"Usuario '{username}' marcado como eliminado.")
                self.load_users()
            else:
                messagebox.showerror("Error", "No se pudo marcar el usuario como eliminado.")


    def load_users(self):
        for item in self.users_tree.get_children(): self.users_tree.delete(item)
        
        users = self.user_manager.list_users()
        
        if not users: self.users_tree.insert("", tk.END, values=("—", "No hay usuarios registrados.")); return
        for user in users: self.users_tree.insert("", tk.END, values=(user[0], user[1]))