import tkinter as tk
from tkinter import messagebox
from clases.users import User

class UserView(tk.Frame):
    """Interfaz para Crear y Listar Usuarios."""
    def __init__(self, master, db_manager):
        super().__init__(master)
        self.user_manager = User(db_manager)
        
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        self.create_widgets()
        self.load_users()

    def create_widgets(self):
        # Frame para el formulario de creación
        form_frame = tk.LabelFrame(self, text="Crear Usuario", padx=10, pady=10)
        form_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.username_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.password_var, show="*", width=30).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(form_frame, text="Crear y Listar", command=self.create_user_ui, 
                  bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

        # Frame para el listado
        list_frame = tk.LabelFrame(self, text="Usuarios Registrados (ID | Username)", padx=10, pady=5)
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.users_listbox = tk.Listbox(list_frame, height=15, width=50)
        self.users_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, command=self.users_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.users_listbox.config(yscrollcommand=scrollbar.set)
    
    def create_user_ui(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Ambos campos son obligatorios.")
            return

        if self.user_manager.create_user(username, password):
            messagebox.showinfo("Éxito", f"Usuario '{username}' creado.")
            self.username_var.set("")
            self.password_var.set("")
            self.load_users()
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario (posiblemente ya existe).")

    def load_users(self):
        self.users_listbox.delete(0, tk.END)
        users = self.user_manager.list_users()
        
        if not users:
             self.users_listbox.insert(tk.END, "No hay usuarios registrados.")
             return

        for user in users:
            self.users_listbox.insert(tk.END, f"{user[0]:<5} | {user[1]}")