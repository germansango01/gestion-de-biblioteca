from clases.database import DatabaseManager
from datetime import datetime

class Book:
    """Clase para gestionar libros (CRUD, préstamos y devoluciones) con Soft Delete."""

    def __init__(self, db: DatabaseManager):
        self.db = db


    def add_book(self, title, isbn, author, category):
        """Agrega un libro activo. Retorna bool."""
        result = self.db.insert(
            "INSERT INTO books (title, isbn, author, category) VALUES (?, ?, ?, ?);",
            (title, isbn, author, category)
        )
        return result is not False


    def update_book(self, book_id, title, isbn, author, category):
        """Actualiza un libro activo. Retorna bool."""
        return self.db.update_delete(
            "UPDATE books SET title = ?, isbn = ?, author = ?, category = ? WHERE id = ? AND deleted_at IS NULL;",
            (title, isbn, author, category, book_id)
        )


    def delete_book(self, book_id):
        """Realiza un soft delete de un libro. Retorna bool."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.db.update_delete(
            "UPDATE books SET deleted_at = ? WHERE id = ? AND deleted_at IS NULL;",
            (timestamp, book_id)
        )


    def list_books(self, available_only=False):
        """Lista los libros activos. Retorna list."""
        query = "SELECT id, title, isbn, author, category, available FROM books WHERE deleted_at IS NULL"
        params = ()
        
        if available_only:
            query += " AND available = ?"
            params = (1,)
        
        query += " ORDER BY title ASC" 
        
        return self.db.select_all(query, params)


    def lend_book(self, book_id, user_id):
        """Presta un libro. Retorna bool."""
        loan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Verificar disponibilidad, existencia.
        check_available = self.db.select_one(
            "SELECT available FROM books WHERE id = ? AND deleted_at IS NULL;", 
            (book_id,)
        )
        
        if not check_available or check_available[0] == 0:
            return False

        # Registrar el préstamo.
        if self.db.insert(
            "INSERT INTO loans (book_id, user_id, loan_date) VALUES (?, ?, ?);",
            (book_id, user_id, loan_date)
        ) is False:
            return False
        
        # Actualizar disponibilidad del libro (Update)
        if self.db.update_delete(
            "UPDATE books SET available = 0 WHERE id = ?;",
            (book_id,)
        ) is False:
            return False
        
        return True

    def return_book(self, book_id):
        """Devuelve un libro prestado. Retorna bool."""
        try:
            return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Marcar el préstamo como devuelto
            self.db.update_delete(
                "UPDATE loans SET return_date = ? WHERE book_id = ? AND return_date IS NULL;",
                (return_date, book_id)
            )
            
            # Marcar el libro como disponible
            update_result = self.db.update_delete(
                "UPDATE books SET available = 1 WHERE id = ? AND available = 0;",
                (book_id,)
            )
            
            return update_result
            
        except Exception:
            return False