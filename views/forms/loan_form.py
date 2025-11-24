import customtkinter as ctk
from tkinter import messagebox

class LoanForm(ctk.CTkToplevel):
    """
    Formulario modal para seleccionar un usuario y un libro disponible
    y registrar un nuevo préstamo.
    """

    def __init__(self, master, loan_manager, user_manager, book_manager, refresh_callback):
        super().__init__(master)
        self.title("Nuevo Préstamo")
        self.geometry("350x250")
        
        # Managers de negocio
        self.loan_mgr = loan_manager
        self.user_mgr = user_manager
        self.book_mgr = book_manager
        
        self.callback = refresh_callback
        self.grab_set() # Hace que el formulario sea modal

        # --- Obtener y mapear datos ---
        # Listamos usuarios activos
        users = self.user_mgr.list() 
        # Listamos solo libros disponibles (available_only=True)
        books = self.book_mgr.list(available_only=True) 

        # Mapeo de nombres a IDs (necesario para la lógica de negocio)
        self.user_map = {u[1]: u[0] for u in users} # {username: id}
        self.book_map = {b[1]: b[0] for b in books} # {title: id}

        # --- Interfaz ---
        
        # Selector de Usuario
        user_names = list(self.user_map.keys()) or ["No hay usuarios"]
        ctk.CTkLabel(self, text="Usuario:").pack(pady=5)
        self.om_user = ctk.CTkOptionMenu(self, values=user_names)
        self.om_user.pack(pady=5)
        
        # Selector de Libro Disponible
        book_titles = list(self.book_map.keys()) or ["No hay libros disponibles"]
        ctk.CTkLabel(self, text="Libro Disponible:").pack(pady=5)
        self.om_book = ctk.CTkOptionMenu(self, values=book_titles)
        self.om_book.pack(pady=5)

        ctk.CTkButton(self, text="Prestar", command=self.save).pack(pady=20)


    def save(self):
        """Procesa el registro del préstamo."""
        u_name = self.om_user.get()
        b_name = self.om_book.get()

        # Validar si se seleccionaron opciones válidas
        if u_name not in self.user_map or b_name not in self.book_map:
            messagebox.showerror("Error", "Seleccione un usuario y un libro válidos.")
            return

        # Obtener los IDs para el manager de negocio
        user_id = self.user_map[u_name]
        book_id = self.book_map[b_name]
        
        # Llamar a la lógica de préstamo
        res = self.loan_mgr.lend_book(user_id, book_id)
        
        if res is True:
            messagebox.showinfo("Éxito", f"Libro '{b_name}' prestado a '{u_name}'.")
            self.callback() # Refresca la tabla en LoanView
            self.destroy()
        else:
            # res contiene el mensaje de error de la clase Loan (e.g., "El libro no está disponible")
            messagebox.showerror("Error", f"Fallo al prestar: {str(res)}")