from database import DatabaseManager
from datetime import datetime

class Book:
    """
    Clase para manejar libros de la biblioteca.
    """

    def __init__(self, db):
        """
        Inicializa el gestor de libros y crea las tablas si no existen.

        Args:
            db: Instancia de DatabaseManager.
        """
        self.db = db
        self._setup_tables()


    def _setup_tables(self):
        """Crea las tablas 'books' y 'loans' si no existen."""
        if self.db is None:
            raise RuntimeError("DatabaseManager no está inicializado.")
            
        self.db.execute_query("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                author TEXT DEFAULT '',
                category TEXT DEFAULT '',
                available INTEGER NOT NULL DEFAULT 1
            );
        """)
        
        self.db.execute_query("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                loan_date TEXT NOT NULL,
                return_date TEXT NULL,
                FOREIGN KEY(book_id) REFERENCES books(id)
            );
        """)


    def add_book(self, title, isbn, author=None, category=None):
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
        author_val = author or ""
        category_val = category or ""

        try:
            self.db.execute_query(
                "INSERT INTO books (title, isbn, author, category) VALUES (?, ?, ?, ?);",
                (title, isbn, author_val, category_val)
            )
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo agregar el libro: {e}")
            return False


    def lend_book(self, book_id, user_id):
        """
        Prestar un libro a un usuario.

        Args:
            book_id (int): ID del libro.
            user_id (int): ID del usuario.

        Returns:
            bool: True si se prestó correctamente, False si falla.
        """
        try:
            loan_date = datetime.now().strftime("%Y-%m-%d")

            self.db.execute_query(
                "INSERT INTO loans (book_id, user_id, loan_date) VALUES (?, ?, ?);",
                (book_id, user_id, loan_date)
            )
            
            self.db.execute_query(
                "UPDATE books SET available = 0 WHERE id = ? AND available = 1;",
                (book_id,)
            )
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo prestar el libro: {e}")
            return False


    def return_book(self, book_id):
        """
        Devolver un libro prestado.

        Args:
            book_id (int): ID del libro.

        Returns:
            bool: True si se devolvió correctamente, False si falla.
        """
        try:
            return_date = datetime.now().strftime("%Y-%m-%d")
            
            self.db.execute_query(
                "UPDATE loans SET return_date = ? WHERE book_id = ? AND return_date IS NULL;",
                (return_date, book_id)
            )
            
            self.db.execute_query(
                "UPDATE books SET available = 1 WHERE id = ? AND available = 0;",
                (book_id,)
            )
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo devolver el libro: {e}")
            return False


    def list_books(self, available_only=False):
        """
        Lista los libros de la biblioteca.

        Args:
            available_only (bool): Si es True, solo lista los libros disponibles.

        Returns:
            list: Lista de libros.
        """
        query = "SELECT id, title, isbn, author, category, available FROM books"
        params = ()
        
        if available_only:
            query += " WHERE available = ?"
            params = (1,)
            
        return self.db.execute_query(query, params)