from datetime import datetime
from clases.database import Database

class Book:
    """Gestión de libros"""

    def __init__(self, db: Database):
        """
        Inicializar la clase con la base de datos.

        Args:
            db (Database): instancia de la clase Database.
        """
        self.db = db


    def get_by_id(self, book_id: int) -> tuple | None:
        """
        Obtener un libro activo por ID.

        Args:
            book_id (int): ID del libro.

        Returns:
            tuple | None: (id, title, isbn, author, category, available) o None.
        """
        return self.db.select_one(
            "SELECT id, title, isbn, author, category, available FROM books WHERE id=? AND deleted_at IS NULL;", 
            (book_id,)
        )

    @staticmethod
    def validate(title: str, isbn: str, author: str, category: str) -> dict:
        """Valida campos de libro."""
        errors = {}
        if not title: errors['title'] = "Requerido."
        if not author: errors['author'] = "Requerido."
        if not category: errors['category'] = "Requerido."
        if len(isbn) < 3: errors['isbn'] = "ISBN inválido."
        return errors

    def add(self, title: str, isbn: str, author: str, category: str) -> bool:
        """
        Agregar un libro a la biblioteca.

        Args:
            title (str): Título del libro.
            isbn (str): ISBN del libro.
            author (str): Autor del libro.
            category (str): Categoría del libro.

        Returns:
            bool: True si se agregó correctamente, False si falla (ej. ISBN duplicado).
        """
        return self.db.insert(
            "INSERT INTO books (title, isbn, author, category) VALUES (?, ?, ?, ?);",
            (title, isbn, author, category)
        ) is not None


    def update(self, book_id: int, title: str, isbn: str, author: str, category: str) -> bool:
        """
        Actualizar los datos de un libro existente.

        Args:
            book_id (int): ID del libro.
            title (str): Nuevo Título.
            isbn (str): Nuevo ISBN.
            author (str): Nuevo Autor.
            category (str): Nueva Categoría.

        Returns:
            bool: True si se actualizó correctamente, False si falla.
        """
        return self.db.update(
            "UPDATE books SET title=?, isbn=?, author=?, category=? "
            "WHERE id=? AND deleted_at IS NULL;",
            (title, isbn, author, category, book_id)
        )


    def soft_delete(self, book_id: int) -> bool:
        """
        Realiza un borrado lógico (soft delete) de un libro.

        Args:
            book_id (int): ID del libro.

        Returns:
            bool: True si se eliminó correctamente, False si falla.
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.db.delete(
            "UPDATE books SET deleted_at=? WHERE id=? AND deleted_at IS NULL;",
            (ts, book_id)
        )


    def list(self, available_only: bool = False) -> list[tuple]:
        """
        Lista los libros disponibles o todos los activos.

        Args:
            available_only (bool): True solo libros disponibles, False todos.

        Returns:
            list: Lista de tuplas con los libros.
        """
        query = "SELECT id, title, isbn, author, category, available FROM books WHERE deleted_at IS NULL"
        params = ()
        if available_only:
            query += " AND available = ?"
            params = (1,)
        query += " ORDER BY title ASC;"
        return self.db.select_all(query, params)
