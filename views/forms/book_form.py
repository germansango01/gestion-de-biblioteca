import tkinter as tk
from tkinter import messagebox, ttk
# Asumo que las clases Book y DatabaseManager están en la carpeta 'clases'
from clases.books import Book 
import re

class BookFormScreen(tk.Toplevel):
    """Pantalla Toplevel dedicada para gestionar un libro (Agregar/Editar)."""
    
    def __init__(self, master, db_manager, book_data=None, callback_on_success=None):
        """
        Inicializa la pantalla.
        :param master: Ventana padre (root de Tkinter).
        :param db_manager: Instancia del DatabaseManager.
        :param book_data: Tupla con los datos del libro si está en modo edición (ID, título, etc.).
        :param callback_on_success: Función a ejecutar en la vista padre al completar la acción.
        """
        self.book_manager = Book(db_manager)
        self.callback_on_success = callback_on_success
        self.book_data = book_data
        
        super().__init__(master)
        
        is_editing = book_data is not None
        title_text = "✏️ Editar Libro" if is_editing else "➕ Agregar Nuevo Libro"
        self.title(title_text)
        
        # Configuración para que sea un modal
        self.transient(master); self.grab_set(); self.focus_set()
        
        # Inicialización de variables de Tkinter
        # book_data es (id, title, isbn, author, category)
        self.title_var = tk.StringVar(value=book_data[1] if is_editing else "")
        self.isbn_var = tk.StringVar(value=book_data[2] if is_editing else "")
        self.author_var = tk.StringVar(value=book_data[3] if is_editing else "")
        self.category_var = tk.StringVar(value=book_data[4] if is_editing else "")
        
        self.create_widgets(is_editing)

    def _is_valid_isbn(self, isbn):
        """Simple validación de formato de ISBN-10 o ISBN-13."""
        isbn_clean = re.sub(r'[-\s]', '', isbn)
        return bool(re.fullmatch(r'(\d{10}|\d{13})', isbn_clean))
    
    def create_widgets(self, is_editing):
        main_frame = ttk.Frame(self, padding="15"); main_frame.pack(fill="both", expand=True)
        
        fields = [
            ("Título: *", self.title_var), ("ISBN: *", self.isbn_var), 
            ("Autor: *", self.author_var), ("Categoría: *", self.category_var)
        ]
        
        for i, (text, var) in enumerate(fields):
            ttk.Label(main_frame, text=text).grid(row=i, column=0, sticky="w", pady=5)
            # El ISBN se desactiva si está en modo edición
            state = "readonly" if is_editing and text == "ISBN: *" else "normal"
            ttk.Entry(main_frame, textvariable=var, width=40, state=state).grid(row=i, column=1, padx=10, pady=5)
            
        button_text = "Guardar Cambios" if is_editing else "✅ Registrar Libro"
        action_command = self.edit_book_ui if is_editing else self.add_book_ui
        
        ttk.Button(main_frame, text=button_text, command=action_command, style='Accent.TButton').grid(
            row=len(fields), column=0, columnspan=2, pady=15, sticky="ew")

    def _validate_input(self):
        """Valida que todos los campos obligatorios estén llenos."""
        title, isbn, author_name, category = (self.title_var.get().strip(), self.isbn_var.get().strip(), 
                                            self.author_var.get().strip(), self.category_var.get().strip())
        if not all([title, isbn, author_name, category]):
            messagebox.showerror("Error de Validación", "Todos los campos marcados con * son obligatorios.", parent=self)
            return False
        return (title, isbn, author_name, category)

    def add_book_ui(self):
        """Lógica para registrar un nuevo libro."""
        validated = self._validate_input()
        if not validated: return
        title, isbn, author_name, category = validated
        
        if self.book_manager.add_book(title, isbn, author_name, category):
            messagebox.showinfo("Éxito", f"Libro '{title}' registrado.", parent=self)
            
            if self.callback_on_success: # ✅ CORRECCIÓN 1: Verificación de callback
                self.callback_on_success()
            self.destroy() 
        else:
            messagebox.showerror("Error", "No se pudo crear el libro (posiblemente el ISBN ya existe).", parent=self)

    def edit_book_ui(self):
        """Lógica para editar un libro existente (con protección de ID)."""
        validated = self._validate_input()
        if not validated: return
        title, isbn, author_name, category = validated
        
        # ✅ CORRECCIÓN 2: Protección robusta para self.book_data
        if not self.book_data or len(self.book_data) == 0:
            messagebox.showerror("Error de Edición", "No se encontró la información del libro (ID) para editar.", parent=self)
            return
            
        try:
            book_id = int(self.book_data[0]) 
        except (TypeError, ValueError):
            messagebox.showerror("Error de Edición", "El ID del libro no es un número válido.", parent=self)
            return

        if self.book_manager.update_book(book_id, title, isbn, author_name, category):
            messagebox.showinfo("Éxito", f"Libro '{title}' actualizado.", parent=self)
            
            if self.callback_on_success: # ✅ CORRECCIÓN 1: Verificación de callback
                self.callback_on_success()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudieron guardar los cambios.", parent=self)