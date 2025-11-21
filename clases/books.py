from clases.database import DatabaseManager
from datetime import datetime

class Book:
    """Clase para gestionar libros de la biblioteca."""

    def __init__(self, db: DatabaseManager):
        """
        Inicializa el gestor de libros.

        Args:
            db (DatabaseManager): Instancia del gestor de base de datos.
        """
        self.db = db

    def add_book(self, title: str, isbn: str, author: str | None, category: str | None) -> bool:
        """
        Agrega un libro a la biblioteca.

        Args:
            title (str): Título del libro.
            isbn (str): ISBN del libro.
            author (str | None): Nombre del autor (texto)
            category (str | None): Categoría del libro.

        Returns:
            bool: True si se agregó correctamente, False si falla.
        """
        category_val = category or ""
        author_val = author or ""
        
        result = self.db.execute(
            "INSERT INTO books (title, isbn, author, category) VALUES (?, ?, ?, ?);",
            (title, isbn, author_val, category_val)
        )
        # Retorna False si falla por IntegrityError
        return result is not False

    def update_book(self, book_id: int, title: str, isbn: str, author: str | None, category: str | None) -> bool:
        """
        Actualiza los detalles de un libro existente.
        """
        category_val = category or ""
        author_val = author or ""

        return self.db.execute(
            "UPDATE books SET title = ?, isbn = ?, author = ?, category = ? WHERE id = ?;",
            (title, isbn, author_val, category_val, book_id)
        )

    def lend_book(self, book_id: int, user_id: int) -> bool:
        """
        Prestar un libro a un usuario. (Lógica sin cambios)
        """
        try:
            loan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Verificar disponibilidad
            check_available = self.db.execute("SELECT available FROM books WHERE id = ?;", (book_id,), fetch_one=True)
            if not check_available or check_available[0] == 0:
                print(f"[ERROR] Book ID {book_id} not available or does not exist.")
                return False

            # Registrar el préstamo
            self.db.execute(
                "INSERT INTO loans (book_id, user_id, loan_date) VALUES (?, ?, ?);",
                (book_id, user_id, loan_date)
            )
            
            # Actualizar disponibilidad
            self.db.execute(
                "UPDATE books SET available = 0 WHERE id = ?;",
                (book_id,)
            )
            return True
        except Exception as e:
            print(f"[ERROR] Could not lend the book: {e}")
            return False


    def return_book(self, book_id: int) -> bool:
        """
        Devolver un libro prestado. (Lógica sin cambios)
        """
        try:
            return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Actualizar el registro de préstamo activo
            self.db.execute(
                "UPDATE loans SET return_date = ? WHERE book_id = ? AND return_date IS NULL;",
                (return_date, book_id)
            )
            
            # Actualizar disponibilidad
            update_result = self.db.execute(
                "UPDATE books SET available = 1 WHERE id = ? AND available = 0;",
                (book_id,)
            )
            return update_result is True
        except Exception as e:
            print(f"[ERROR] Could not return the book: {e}")
            return False


    def list_books(self, available_only: bool = False) -> list:
        """
        Lista los libros de la biblioteca. (Consulta SQL simplificada)

        Args:
            available_only (bool): Si es True, solo lista los libros disponibles.

        Returns:
            list: Lista de libros.
        """
        query = """
            SELECT b.id, b.title, b.isbn, b.author, b.category, b.available
            FROM books b
            -- 🛑 LEFT JOIN authors a ON b.author_id = a.id ELIMINADO 🛑
        """
        params = ()
        
        if available_only:
            query += " WHERE b.available = ?"
            params = (1,)
        
        query += " ORDER BY b.title ASC" 
        return self.db.execute(query, params)