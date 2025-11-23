from clases.database import Database

class History:
    """Gestión del historial de préstamos en la biblioteca."""

    def __init__(self, db):
        """
        Inicializa la clase con la base de datos.

        Args:
            db (Database): instancia de la clase Database.
        """
        self.db = db


    def get_loans(self, user_id=None):
        """
        Obtiene el historial completo de préstamos.

        Args:
            user_id (int, opcional): filtra por ID de usuario.

        Returns:
            list: Lista de tuplas con (id, title, username, loan_date, return_date).
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


    def get_active_loans(self):
        """
        Obtiene todos los préstamos activos (no devueltos).

        Returns:
            list: Lista de tuplas con (id, title, username, loan_date).
        """
        query = """
        SELECT l.id, b.title, u.username, l.loan_date
        FROM loans l
        INNER JOIN books b ON l.book_id = b.id
        INNER JOIN users u ON l.user_id = u.id
        WHERE l.return_date IS NULL
        ORDER BY l.loan_date ASC;
        """
        return self.db.select_all(query)
