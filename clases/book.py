from datetime import datetime
from clases.database import Database

class Book:
    """
    Gestión de libros, incluyendo validación de unicidad y estado de préstamo.
    """
    def __init__(self, db: Database):
        self.db = db


    def _validate_uniqueness(self, isbn: str, current_id: int | None = None) -> dict:
        """
        Verifica si el ISBN ya está registrado para otro libro.

        Args:
            isbn (str): ISBN a verificar.
            current_id (int | None): ID del libro actual (para exclusión en UPDATE).

        Returns:
            dict: Diccionario de errores ('isbn' si falla).
        """
        isbn_clean = isbn.replace('-', '').replace(' ', '').upper()
        
        query = "SELECT id FROM books WHERE isbn=? AND deleted_at IS NULL"
        params = (isbn_clean,)
        
        if current_id is not None:
            query += " AND id!=?"
            params = (isbn_clean, current_id)
            
        if self.db.select_one(query, params):
            return {'isbn': "Este ISBN ya está registrado en la biblioteca."}
        
        return {}


    def get_by_id(self, book_id: int) -> tuple | None:
        """
        Obtener un libro activo por ID.
        """
        return self.db.select_one(
            "SELECT id, title, isbn, author, category, available FROM books WHERE id=? AND deleted_at IS NULL;", 
            (book_id,)
        )


    @staticmethod
    def validate(title: str, isbn: str, author: str, category: str) -> dict:
        """
        Valida campos de libro.
        """
        errors = {}
        if not title: errors['title'] = "Requerido."
        if not author: errors['author'] = "Requerido."
        if not category: errors['category'] = "Requerido."
        if len(isbn.replace('-', '').replace(' ', '')) < 10: 
            errors['isbn'] = "El ISBN debe tener al menos 10 caracteres."
        return errors


    def create(self, title: str, isbn: str, author: str, category: str) -> bool | dict:
        """
        Agregar un libro a la biblioteca, verificando unicidad del ISBN.

        Returns:
            bool | dict: True si se agregó, o dict de errores de unicidad si falla.
        """
        isbn_clean = isbn.replace('-', '').replace(' ', '').upper()

        # Validación de unicidad
        errors = self._validate_uniqueness(isbn_clean)
        if errors:
            return errors
        
        # Inserción
        result = self.db.insert(
            "INSERT INTO books (title, isbn, author, category) VALUES (?, ?, ?, ?);",
            (title, isbn_clean, author, category)
        )
        
        if result is None:
            # Error genérico de DB (ej. conexión)
            return {'general': 'Fallo al insertar el registro en la base de datos.'}
        
        return True


    def update(self, book_id: int, title: str, isbn: str, author: str, category: str) -> bool | dict:
        """
        Actualizar los datos de un libro existente, verificando unicidad del nuevo ISBN.

        Returns:
            bool | dict: True si se actualizó, o dict de errores de unicidad si falla.
        """
        isbn_clean = isbn.replace('-', '').replace(' ', '').upper()
        
        # Validación de unicidad (excluyendo el libro actual)
        errors = self._validate_uniqueness(isbn_clean, book_id)
        if errors:
            return errors
        
        # Actualización
        result = self.db.update(
            "UPDATE books SET title=?, isbn=?, author=?, category=? "
            "WHERE id=? AND deleted_at IS NULL;",
            (title, isbn_clean, author, category, book_id)
        )
        
        return result


    def soft_delete(self, book_id: int) -> bool | dict:
        """
        Realiza un borrado lógico (soft delete) de un libro, verificando 
        que no esté prestado (available = 0).

        Returns:
            bool | dict: True si se eliminó, o dict de error si está prestado.
        """
        # Verificar estado (disponible)
        book = self.db.select_one("SELECT available FROM books WHERE id=?", (book_id,))
        if book and book[0] == 0:
            return {'general': "El libro está actualmente prestado y no puede ser eliminado."}
        
        # Borrado lógico
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = self.db.update(
            "UPDATE books SET deleted_at=? WHERE id=? AND deleted_at IS NULL;",
            (ts, book_id)
        )
        
        if not result:
            return {'general': 'Error desconocido al intentar eliminar el libro.'}
            
        return True


    def list(self, available_only: bool = False) -> list[tuple]:
        """
        Lista los libros disponibles o todos los activos.
        """
        query = "SELECT id, title, isbn, author, category, available FROM books WHERE deleted_at IS NULL"
        params = ()
        if available_only:
            query += " AND available = ?"
            params = (1,)
        query += " ORDER BY id ASC;"
        return self.db.select_all(query, params)