import customtkinter as ctk
from tkinter import messagebox

class LoanForm(ctk.CTkToplevel):
    """
    Formulario modal para seleccionar un usuario y un libro disponible.
    """

    def __init__(self, master, loan_manager, user_manager, book_manager, refresh_callback):
        super().__init__(master)
        self.title("Nuevo Préstamo")
        self.geometry("400x280")
        self.grab_set()

        self.loan_mgr = loan_manager
        self.user_mgr = user_manager
        self.book_mgr = book_manager
        self.callback = refresh_callback

        # Grid responsivo
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        # --- Obtener datos ---
        users = self.user_mgr.list()
        books = self.book_mgr.list(available_only=True)
        self.user_map = {u[1]: u[0] for u in users}
        self.book_map = {b[1]: b[0] for b in books}

        self.user_names = ["--- Seleccione Usuario ---"] + list(self.user_map.keys()) if users else ["--- Seleccione Usuario ---"]
        self.book_titles = ["--- Seleccione Libro ---"] + list(self.book_map.keys()) if books else ["--- Seleccione Libro ---"]

        self.user_placeholder = self.user_names[0]
        self.book_placeholder = self.book_titles[0]

        # --- Error general ---
        self.general_error = ctk.CTkLabel(self, text="", text_color="red")
        self.general_error.grid(row=0, column=0, columnspan=2, padx=20, pady=(10,5), sticky="w")

        # Selector Usuario
        ctk.CTkLabel(self, text="Usuario:").grid(row=1, column=0, padx=10, pady=(10,0), sticky="w")
        self.om_user = ctk.CTkOptionMenu(self, values=self.user_names, width=220)
        self.om_user.set(self.user_placeholder)
        self.om_user.grid(row=1, column=1, padx=10, pady=(10,0), sticky="ew")
        self.error_user = ctk.CTkLabel(self, text="", text_color="red")
        self.error_user.grid(row=2, column=0, columnspan=2, padx=10, sticky="w")

        # Selector Libro
        ctk.CTkLabel(self, text="Libro:").grid(row=3, column=0, padx=10, pady=(10,0), sticky="w")
        self.om_book = ctk.CTkOptionMenu(self, values=self.book_titles, width=220)
        self.om_book.set(self.book_placeholder)
        self.om_book.grid(row=3, column=1, padx=10, pady=(10,0), sticky="ew")
        self.error_book = ctk.CTkLabel(self, text="", text_color="red")
        self.error_book.grid(row=4, column=0, columnspan=2, padx=10, sticky="w")

        # Botón Prestar
        ctk.CTkButton(self, text="Prestar", command=self.save).grid(row=5, column=0, columnspan=2, pady=20, padx=20, sticky="ew")


    def _validate_ui(self, u_name: str, b_name: str) -> bool:
        """
        Valida que se hayan seleccionado opciones válidas.
        """
        is_valid = True
        self.general_error.configure(text="")
        self.error_user.configure(text="")
        self.error_book.configure(text="")

        if u_name == self.user_placeholder or u_name not in self.user_map:
            self.error_user.configure(text="Debe seleccionar un usuario válido.")
            is_valid = False

        if b_name == self.book_placeholder or b_name not in self.book_map:
            self.error_book.configure(text="Debe seleccionar un libro disponible.")
            is_valid = False

        return is_valid


    def save(self):
        """
        Valida y registra el préstamo a través de la capa de negocio.
        """
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
            self.general_error.configure(text=str(res))
