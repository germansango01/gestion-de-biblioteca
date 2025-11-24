import customtkinter as ctk
import re

class BookForm(ctk.CTkToplevel):
    """
    Formulario modal para añadir nuevos libros.
    """
    
    @staticmethod
    def is_valid_isbn(isbn: str) -> bool:
        """
        Verifica que el ISBN tenga 10 o 13 caracteres, solo dígitos o 'X' al final.
        """
        isbn_clean = isbn.replace('-', '').replace(' ', '').upper()
        n = len(isbn_clean)

        if n == 10:
            # 10 caracteres: 9 dígitos + 1 dígito/X
            pattern = r"^\d{9}[\dX]$"
        elif n == 13:
            # 13 caracteres: 13 dígitos
            pattern = r"^\d{13}$"
        else:
            return False 

        return bool(re.match(pattern, isbn_clean))


    def __init__(self, master, book_manager, refresh_callback):
        super().__init__(master)
        self.title("Nuevo Libro")
        self.geometry("450x450") 
        self.manager = book_manager
        self.callback = refresh_callback
        self.grab_set()

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=3) 

        self.entries = {}
        self.errors = {}
        
        fields = ["title", "isbn", "author", "category"]
        
        row_counter = 0
        for f in fields:
            ctk.CTkLabel(self, text=f.capitalize() + ":").grid(
                row=row_counter, column=0, padx=(20, 5), pady=(15, 0), sticky="w"
            )
            self.entries[f] = ctk.CTkEntry(self, width=250)
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
        Realiza la validación de la interfaz (campos no vacíos y formato ISBN).
        """
        ui_errors = {}
        
        # 1. Validación de campos no vacíos
        for key, value in data.items():
            if not value.strip():
                ui_errors[key] = f"El campo '{key.capitalize()}' es obligatorio."

        # 2. Validación de ISBN simple
        isbn = data.get('isbn', '').strip()
        if 'isbn' not in ui_errors and isbn:
            if not self.is_valid_isbn(isbn):
                ui_errors['isbn'] = "ISBN inválido. Debe tener 10 (incl. X) o 13 dígitos."
        
        return ui_errors


    def save(self):
        # 1. Obtener datos y limpiar errores previos
        data = {k: v.get() for k, v in self.entries.items()}
        for lbl in self.errors.values(): 
            lbl.configure(text="")

        # 2. Realizar validación de la interfaz (UI)
        ui_errors = self._validate_ui(data)
        
        if ui_errors:
            for k, v in ui_errors.items():
                if k in self.errors: 
                    self.errors[k].configure(text=v)
            return

        # 3. Llamar a la capa de negocio (valida unicidad)
        # NOTA: En la clase Book, el método se llama 'create', pero aquí se llama 'add' en el form original
        res = self.manager.create(data['title'], data['isbn'], data['author'], data['category'])
        
        if res is True:
            self.callback()
            self.destroy()
        elif isinstance(res, dict):
            # Fallo en la capa de negocio (ej. ISBN duplicado)
            for k, v in res.items():
                if k in self.errors:
                    self.errors[k].configure(text=v)
                elif k == 'general':
                    self.errors['isbn'].configure(text=v) # Mostrar errores generales bajo ISBN