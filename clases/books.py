from datetime import datetime
from database import Database

class Book:
    """Gestión de libros: agregar, actualizar, borrar, listar y manejar préstamos."""

    def __init__(self, db: Database):
        self.db = db


    def add(self, title, isbn, author, category):
        """Agrega un libro.

        Returns:
            bool: True si se agregó correctamente, False si falla.
        """
        return self.db.insert(
            "INSERT INTO books (title, isbn, author, category) VALUES (?, ?, ?, ?);",
            (title, isbn, author, category)
        ) is not None


    def update(self, book_id, title, isbn, author, category):
        """Actualiza un libro existente.

        Returns:
            bool: True si se actualizó correctamente.
        """
        return self.db.update(
            "UPDATE books SET title=?, isbn=?, author=?, category=? WHERE id=? AND deleted_at IS NULL;",
            (title, isbn, author, category, book_id)
        )


    def soft_delete(self, book_id):
        """Realiza un borrado lógico de un libro.

        Returns:
            bool
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.db.update(
            "UPDATE books SET deleted_at=? WHERE id=? AND deleted_at IS NULL;",
            (ts, book_id)
        )


    def list_books(self, available_only=False):
        """Lista los libros activos.

        Returns:
            list: Lista de tuplas con libros.
        """
        query = "SELECT id, title, isbn, author, category, available FROM books WHERE deleted_at IS NULL"
        params = ()
        if available_only:
            query += " AND available = ?"
            params = (1,)
        query += " ORDER BY title ASC;"
        return self.db.select_all(query, params)


    def lend_book(self, book_id, user_id):
        """Presta un libro a un usuario.

        Returns:
            bool
        """
        row = self.db.select_one(
            "SELECT available FROM books WHERE id=? AND deleted_at IS NULL;", (book_id,)
        )
        if not row or row[0] == 0:
            return False
        loan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.db.insert(
            "INSERT INTO loans (book_id, user_id, loan_date) VALUES (?, ?, ?);",
            (book_id, user_id, loan_date)
        ) is None:
            return False
        return self.db.update("UPDATE books SET available = 0 WHERE id=?;", (book_id,))


    def return_book(self, book_id):
        """Devuelve un libro prestado.

        Returns:
            bool
        """
        return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ok1 = self.db.update(
            "UPDATE loans SET return_date=? WHERE book_id=? AND return_date IS NULL;",
            (return_date, book_id)
        )
        ok2 = self.db.update(
            "UPDATE books SET available=1 WHERE id=? AND available=0;",
            (book_id,)
        )
        return ok1 and ok2


    def find_active_loan_by_user_id(self, user_id):
        """Obtiene el libro activo prestado a un usuario.

        Returns:
            int | None: ID del libro o None si no hay préstamo activo.
        """
        row = self.db.select_one(
            "SELECT book_id FROM loans WHERE user_id=? AND return_date IS NULL ORDER BY loan_date DESC LIMIT 1;",
            (user_id,)
        )
        return row[0] if row else None
