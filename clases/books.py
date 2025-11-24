from datetime import datetime
from clases.database import Database

class Book:
    """Gestión de libros, incluyendo disponibilidad y operaciones de préstamo."""

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


    def lend(self, book_id: int, user_id: int) -> bool:
        """
        Registra un préstamo de un libro a un usuario.

        Args:
            book_id (int): ID del libro.
            user_id (int): ID del usuario.

        Returns:
            bool: True si se prestó correctamente, False si falla (no disponible/no existe).
        """
        book_data = self.get_by_id(book_id)
        # Verifica disponibilidad.
        if not book_data or book_data[5] == 0: 
            return False

        loan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insertar el préstamo.
        loan_id = self.db.insert(
            "INSERT INTO loans (book_id, user_id, loan_date) VALUES (?, ?, ?);",
            (book_id, user_id, loan_date)
        )
        if loan_id is None:
            return False

        # Marcar el libro como NO disponible.
        return self.db.update("UPDATE books SET available=0 WHERE id=?;", (book_id,))


    def return_book(self, book_id: int) -> bool:
        """
        Registrar la devolución de un libro prestado.

        Args:
            book_id (int): ID del libro.

        Returns:
            bool: True si se devolvió correctamente, False si falla.
        """
        return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Actualizar el registro de préstamo.
        ok1 = self.db.update(
            "UPDATE loans SET return_date=? WHERE book_id=? AND return_date IS NULL;",
            (return_date, book_id)
        )
        # Marcar el libro como disponible de nuevo.
        ok2 = self.db.update(
            "UPDATE books SET available=1 WHERE id=? AND available=0;",
            (book_id,)
        )
        # validar ambos updates
        return ok1 and ok2


    def find_active_loan_by_user_id(self, user_id: int) -> int | None:
        """
        Obtener el ID del libro prestado más recientemente por un usuario.

        Args:
            user_id (int): ID del usuario.

        Returns:
            int | None: ID del libro o None si no hay préstamo activo.
        """
        row = self.db.select_one(
            "SELECT book_id FROM loans WHERE user_id=? AND return_date IS NULL "
            "ORDER BY loan_date DESC LIMIT 1;", (user_id,)
        )
        return row[0] if row else None