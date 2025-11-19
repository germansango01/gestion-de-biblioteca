from database import DatabaseManager
from datetime import datetime

class Book:
    """
    Clase para manejar libros de la biblioteca.
    """


    def __init__(self, db: DatabaseManager):
        """
        Inicializa el gestor de libros y crea la tabla si no existen.

        Args:
            db (DatabaseManager): Instancia de DatabaseManager.
        """
        self.db = db
        self._setup_table()


    def _setup_table(self):
        """Crea la tabla books si no existe. Ahora guarda solo el nombre del autor."""
        if self.db is None:
            raise RuntimeError("DatabaseManager no está inicializado")
        self.db.execute_query("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                author TEXT,
                category TEXT,
                available INTEGER NOT NULL DEFAULT 1
            );
        """)


    def add_book(self, title: str, isbn: str, author: str | None = None, category: str | None = None) -> bool:
        """
        Agrega un libro a la biblioteca.

        Args:
            title (str): Título del libro.
            isbn (str): ISBN del libro.
            author (str | None, optional): Nombre del autor.
            category (str | None, optional): Categoría del libro.

        Returns:
            bool: True si se agregó correctamente, False si falla.
        """
        try:
            # Convertir None a cadena vacía para evitar errores de tipo
            author_val = author or ""
            category_val = category or ""

            self.db.execute_query(
                "INSERT INTO books (title, isbn, author, category) VALUES (?, ?, ?, ?);",
                (title, isbn, author_val, category_val)
            )
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo agregar el libro: {e}")
            return False


    def lend_book(self, book_id: int, user_id: int) -> bool:
        """
        Prestar un libro a un usuario.

        Args:
            book_id (int): ID del libro.
            user_id (int): ID del usuario.

        Returns:
            bool: True si se prestó correctamente, False si falla.
        """
        try:
            date = datetime.now().strftime("%Y-%m-%d")
            self.db.execute_query(
                "INSERT INTO loans (book_id, user_id, loan_date) VALUES (?, ?, ?);",
                (book_id, user_id, date)
            )
            self.db.execute_query(
                "UPDATE books SET available = 0 WHERE id = ?;",
                (book_id,)
            )
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo prestar el libro: {e}")
            return False


    def return_book(self, book_id: int) -> bool:
        """
        Devolver un libro prestado.

        Args:
            book_id (int): ID del libro.

        Returns:
            bool: True si se devolvió correctamente, False si falla.
        """
        try:
            date = datetime.now().strftime("%Y-%m-%d")
            self.db.execute_query(
                "UPDATE loans SET return_date = ? WHERE book_id = ? AND return_date IS NULL;",
                (date, book_id)
            )
            self.db.execute_query(
                "UPDATE books SET available = 1 WHERE id = ?;",
                (book_id,)
            )
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo devolver el libro: {e}")
            return False


    def list_books(self, available_only: bool = False) -> list[tuple]:
        """
        Lista los libros de la biblioteca.

        Args:
            available_only (bool): Si es True, solo lista los libros disponibles.

        Returns:
            list[tuple]: Lista de libros.
        """
        query = "SELECT id, title, isbn, author, category, available FROM books"
        if available_only:
            query += " WHERE available = 1"
        return self.db.execute_query(query)
