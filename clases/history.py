from clases.database import DatabaseManager

class History:
    """Clase para gestionar el historial de préstamos de libros."""

    def __init__(self, db: DatabaseManager):
        """
        Inicializa el gestor de historial.

        Args:
            db (DatabaseManager): Instancia del gestor de base de datos.
        """
        self.db = db


    def get_loans(self, user_id: int | None = None) -> list:
        """
        Obtiene el historial completo de préstamos, opcionalmente filtrado por usuario.

        Args:
            user_id (int | None, optional): ID del usuario para filtrar préstamos.

        Returns:
            list: Lista de préstamos.
        """
        query = """
            SELECT l.id, b.title, u.username, l.loan_date, l.return_date
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN users u ON l.user_id = u.id
        """
        params = ()
        
        if user_id is not None:
            query += " WHERE l.user_id = ?"
            params = (user_id,)
            
        query += " ORDER BY l.loan_date DESC"

        return self.db.execute(query, params)


    def get_active_loans(self) -> list:
        """
        Obtiene una lista de todos los préstamos que aún no han sido devueltos.

        Returns:
            list: Lista de préstamos activos con (loan_id, book_title, username, loan_date).
        """
        query = """
            SELECT l.id, b.title, u.username, l.loan_date
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN users u ON l.user_id = u.id
            WHERE l.return_date IS NULL
            ORDER BY l.loan_date ASC
        """
        return self.db.execute(query)