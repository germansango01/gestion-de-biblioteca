from clases.database import DatabaseManager
from datetime import datetime

class Book:
    """Clase para gestionar libros (CRUD, préstamos y devoluciones)."""

    def __init__(self, db: DatabaseManager):
        """
        Inicializar con el gestor de base de datos.

        Args:
            db (DatabaseManager): Instancia de DatabaseManager.
        """
        self.db = db


    def add_book(self, title: str, isbn: str, author: str | None, category: str | None) -> bool:
        """
        Agregar un libro. 
        Return: True si se agregó, False si falla.
        """
        category_val = category or ""
        author_val = author or ""
        
        result: int | bool = self.db.insert(
            "INSERT INTO books (title, isbn, author, category) VALUES (?, ?, ?, ?);",
            (title, isbn, author_val, category_val)
        )
        return result is not False


    def update_book(self, book_id: int, title: str, isbn: str, author: str | None, category: str | None) -> bool:
        """
        Actualizar un libro. 
        Return: True si se actualizó, False en caso contrario.
        """
        category_val = category or ""
        author_val = author or ""

        return self.db.update(
            "UPDATE books SET title = ?, isbn = ?, author = ?, category = ? WHERE id = ?;",
            (title, isbn, author_val, category_val, book_id)
        )


    def list_books(self, available_only: bool = False) -> list:
        """
        Listar los libros.

        Args:
            available_only (bool): Si es True, solo lista los disponibles.

        Return:
            list: Lista de tuplas con los detalles de los libros.
        """
        query = "SELECT id, title, isbn, author, category, available FROM books"
        params = ()
        
        if available_only:
            query += " WHERE available = ?"
            params = (1,)
        
        query += " ORDER BY title ASC" 
        
        # *** CAMBIO: Usamos self.db.select_all() -> list ***
        return self.db.select_all(query, params)


    def lend_book(self, book_id: int, user_id: int) -> bool:
        """
        Prestar un libro a un usuario.

        Args:
            book_id (int): ID del libro.
            user_id (int): ID del usuario.

        Return:
            bool: True si el préstamo fue exitoso, False si falla.
        """
        loan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Verificar disponibilidad y existencia
        # *** CAMBIO: Usamos self.db.select_one() -> tuple | None ***
        check_available: tuple | None = self.db.select_one(
            "SELECT available FROM books WHERE id = ?;", 
            (book_id,)
        )
        
        if not check_available or check_available[0] == 0:
            print(f"[ERROR] El libro con ID {book_id} no está disponible o no existe.")
            return False

        # Registrar el préstamo.
        if self.db.insert(
            "INSERT INTO loans (book_id, user_id, loan_date) VALUES (?, ?, ?);",
            (book_id, user_id, loan_date)
        ) is False:
            print(f"[ERROR] Falló el registro del préstamo para el libro ID {book_id}.")
            return False
        
        # Actualizar disponibilidad del libro.
        if self.db.update(
            "UPDATE books SET available = 0 WHERE id = ?;",
            (book_id,)
        ) is False:
            print(f"[ERROR] Falló la actualización de disponibilidad del libro ID {book_id}. Estado inconsistente.")
            return False
        
        return True


    def return_book(self, book_id: int) -> bool:
        """
        Devolver un libro prestado. 
        Return: True si la devolución fue exitosa, False si falla.
        """
        try:
            return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.db.update(
                "UPDATE loans SET return_date = ? WHERE book_id = ? AND return_date IS NULL;",
                (return_date, book_id)
            )
            
            update_result: bool = self.db.update(
                "UPDATE books SET available = 1 WHERE id = ? AND available = 0;",
                (book_id,)
            )
            
            return update_result
            
        except Exception as e:
            print(f"[ERROR] No se pudo devolver el libro: {e}")
            return False