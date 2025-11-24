import customtkinter as ctk
from tkinter import messagebox

class LoanForm(ctk.CTkToplevel):
    """
    Formulario modal para seleccionar un usuario y un libro disponible.
    """
    def __init__(self, master, loan_manager, user_manager, book_manager, refresh_callback):
        super().__init__(master)
        self.title("Nuevo Préstamo")
        self.geometry("350x300")
        
        self.loan_mgr = loan_manager
        self.user_mgr = user_manager
        self.book_mgr = book_manager
        self.callback = refresh_callback
        self.grab_set() 

        # --- Obtener y mapear datos ---
        users = self.user_mgr.list() 
        books = self.book_mgr.list(available_only=True) 

        self.user_map = {u[1]: u[0] for u in users} 
        self.book_map = {b[1]: b[0] for b in books} 

        self.user_names = list(self.user_map.keys())
        self.book_titles = list(self.book_map.keys())

        self.user_placeholder = "--- Seleccione Usuario ---"
        self.book_placeholder = "--- Seleccione Libro ---"

        # Asegurar que el placeholder sea la primera opción si hay elementos, o la única si no los hay
        if self.user_names: self.user_names.insert(0, self.user_placeholder)
        if self.book_titles: self.book_titles.insert(0, self.book_placeholder)
        
        if not self.user_names: self.user_names = [self.user_placeholder]
        if not self.book_titles: self.book_titles = [self.book_placeholder]


        # --- Interfaz ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        # Selector de Usuario
        ctk.CTkLabel(self, text="Usuario:").grid(row=0, column=0, padx=10, pady=(15, 0), sticky="w")
        self.om_user = ctk.CTkOptionMenu(self, values=self.user_names, width=200)
        self.om_user.set(self.user_placeholder)
        self.om_user.grid(row=0, column=1, padx=10, pady=(15, 0), sticky="ew")
        self.error_user = ctk.CTkLabel(self, text="", text_color="red")
        self.error_user.grid(row=1, column=0, columnspan=2, padx=10, sticky="w")
        
        # Selector de Libro Disponible
        ctk.CTkLabel(self, text="Libro:").grid(row=2, column=0, padx=10, pady=(15, 0), sticky="w")
        self.om_book = ctk.CTkOptionMenu(self, values=self.book_titles, width=200)
        self.om_book.set(self.book_placeholder)
        self.om_book.grid(row=2, column=1, padx=10, pady=(15, 0), sticky="ew")
        self.error_book = ctk.CTkLabel(self, text="", text_color="red")
        self.error_book.grid(row=3, column=0, columnspan=2, padx=10, sticky="w")

        ctk.CTkButton(self, text="Prestar", command=self.save).grid(row=4, column=0, columnspan=2, pady=20)


    def _validate_ui(self, u_name: str, b_name: str) -> bool:
        """
        Verifica que se hayan seleccionado opciones válidas.
        """
        is_valid = True
        
        self.error_user.configure(text="")
        self.error_book.configure(text="")
        
        # 1. Validar selección de usuario
        if u_name == self.user_placeholder or u_name not in self.user_map:
            self.error_user.configure(text="Debe seleccionar un usuario válido.")
            is_valid = False

        # 2. Validar selección de libro
        if b_name == self.book_placeholder or b_name not in self.book_map:
            self.error_book.configure(text="Debe seleccionar un libro disponible.")
            is_valid = False
            
        return is_valid


    def save(self):
        u_name = self.om_user.get()
        b_name = self.om_book.get()

        if not self._validate_ui(u_name, b_name):
            return

        user_id = self.user_map[u_name]
        book_id = self.book_map[b_name]
        
        res = self.loan_mgr.lend_book(user_id, book_id)
        
        if res is True:
            messagebox.showinfo("Éxito", f"Préstamo registrado: {b_name} a {u_name}.")
            self.callback() 
            self.destroy()
        else:
            messagebox.showerror("Error", f"Fallo al prestar: {str(res)}")