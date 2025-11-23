from clases.database import DatabaseManager

class History:
    """Clase para gestionar el historial de préstamos."""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_loans(self, user_id=None):
        """Obtiene el historial completo. Retorna list."""
        query = """
            SELECT 
                l.id, 
                b.title AS title, 
                u.username AS username, 
                l.loan_date, 
                l.return_date
            FROM loans l
            LEFT JOIN books b ON l.book_id = b.id
            LEFT JOIN users u ON l.user_id = u.id
        """
        params = ()
        
        if user_id is not None:
            query += " WHERE l.user_id = ?"
            params = (user_id,)
            
        query += " ORDER BY l.loan_date DESC"
        return self.db.select_all(query, params)


    def get_active_loans(self):
        """Obtiene una lista de todos los préstamos que aún no han sido devueltos. Retorna list."""
        query = """
            SELECT 
                l.id, 
                b.title AS title,
                u.username AS username,
                l.loan_date
            FROM loans l
            INNER JOIN books b ON l.book_id = b.id
            INNER JOIN users u ON l.user_id = u.id
            WHERE l.return_date IS NULL
            ORDER BY l.loan_date ASC
        """
        return self.db.select_all(query)