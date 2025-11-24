# clases/loan.py
from datetime import datetime
from clases.database import Database

class Loan:
    """
    Gestión completa de préstamos, devoluciones y reportes de historial.
    """

    def __init__(self, db: Database):
        """
        Inicializa con la base de datos.

        Args:
            db (Database): Instancia de base de datos.
        """
        self.db = db


    def lend_book(self, user_id: int, book_id: int) -> bool | str:
        """
        Registra un préstamo y actualiza la disponibilidad del libro a 0 (no disponible).

        Args:
            user_id (int): ID del usuario que toma prestado el libro.
            book_id (int): ID del libro prestado.

        Returns:
            bool | str: True si el préstamo fue exitoso, mensaje de error (str) si falla.
        """
        # Verificar disponibilidad real y existencia del libro
        book = self.db.select_one("SELECT available FROM books WHERE id=? AND deleted_at IS NULL", (book_id,))
        if not book:
            return "El libro no existe o fue eliminado."
        if book[0] == 0:
            return "El libro no está disponible actualmente."

        # Registrar préstamo
        loan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not self.db.insert("INSERT INTO loans (book_id, user_id, loan_date) VALUES (?, ?, ?)", 
                            (book_id, user_id, loan_date)):
            return "Error al registrar el préstamo en la base de datos."

        # Actualizar estado libro (available = 0)
        self.db.update("UPDATE books SET available=0 WHERE id=?", (book_id,))
        return True


    def return_book(self, loan_id: int, book_id: int) -> bool:
        """
        Registra la fecha de devolución en el préstamo y actualiza la disponibilidad
        del libro a 1 (disponible).

        Args:
            loan_id (int): ID del registro de préstamo activo.
            book_id (int): ID del libro a liberar.

        Returns:
            bool: True si la devolución fue exitosa, False si falla.
        """
        ret_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Cerrar préstamo (solo si return_date es NULL)
        ok_loan = self.db.update(
            "UPDATE loans SET return_date=? WHERE id=? AND return_date IS NULL", 
            (ret_date, loan_id)
        )
        
        # Liberar libro (available = 1)
        ok_book = self.db.update("UPDATE books SET available=1 WHERE id=?", (book_id,))
        
        # Debe ser exitoso si el préstamo existía y se pudo actualizar el libro.
        return ok_loan and ok_book


    def get_active_loans(self) -> list[tuple]:
        """
        Obtener todos los préstamos activos (no devueltos).

        Returns:
            list: Lista de tuplas con (loan_id, title, username, loan_date, book_id).
        """
        query = """
            SELECT l.id, b.title, u.username, l.loan_date, l.book_id
            FROM loans l
            INNER JOIN books b ON l.book_id = b.id
            INNER JOIN users u ON l.user_id = u.id
            WHERE l.return_date IS NULL
            ORDER BY l.loan_date ASC;
        """
        return self.db.select_all(query)


    def get_history(self, user_id: int | None = None) -> list[tuple]:
        """
        Obtener el historial completo de préstamos (activos y devueltos), 
        opcionalmente filtrado por usuario.

        Args:
            user_id (int | None): ID de usuario para filtrar, None para todos.

        Returns:
            list: Lista de tuplas con (loan_id, title, username, loan_date, return_date).
        """
        query = """
            SELECT l.id, b.title, u.username, l.loan_date, l.return_date
            FROM loans l
            LEFT JOIN books b ON l.book_id = b.id
            LEFT JOIN users u ON l.user_id = u.id
        """
        params = ()
        if user_id is not None:
            query += " WHERE l.user_id=?"
            params = (user_id,)
        
        query += " ORDER BY l.loan_date DESC;"
        return self.db.select_all(query, params)