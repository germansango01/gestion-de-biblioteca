from clases.database import DatabaseManager

class History:
    """Clase para gestionar el historial de préstamos y las consultas de préstamos activos."""

    def __init__(self, db: DatabaseManager):
        """
        Inicializar con el gestor de base de datos.

        Args:
            db (DatabaseManager): Instancia del gestor de base de datos.
        """
        self.db = db


    def get_loans(self, user_id: int | None = None) -> list:
        """
        Obtener el historial completo de préstamos, opcionalmente filtrado por usuario.

        Args:
            user_id (int | None): ID del usuario para filtrar.

        Return:
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
        return self.db.select_all(query, params)


    def get_active_loans(self) -> list:
        """
        Obtener una lista de todos los préstamos que aún no han sido devueltos.

        Return:
            list: Lista de préstamos activos.
        """
        query = """
            SELECT l.id, b.title, u.username, l.loan_date
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN users u ON l.user_id = u.id
            WHERE l.return_date IS NULL
            ORDER BY l.loan_date ASC
        """
        return self.db.select_all(query)