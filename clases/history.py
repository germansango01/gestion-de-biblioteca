from clases.database import DatabaseManager

class History:
    """
    Clase para manejar el historial de préstamos de libros.
    """

    def __init__(self, db):
        """
        Inicializa el gestor de historial y asegura que la tabla 'loans' exista.

        Args:
            db: Instancia de DatabaseManager.
        """
        self.db = db
        self._setup_table()


    def _setup_table(self):
        """Crea la tabla loans si no existe, incluyendo las claves foráneas."""
        if self.db is None:
            raise RuntimeError("DatabaseManager no está inicializado.")
            
        self.db.execute_query("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                loan_date TEXT NOT NULL,
                return_date TEXT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)


    def get_loans(self, user_id=None):
        """
        Obtiene el historial completo de préstamos, opcionalmente filtrado por usuario.

        Args:
            user_id (int | None, optional): ID del usuario para filtrar préstamos.

        Returns:
            list: Lista de préstamos con (loan_id, book_title, username, loan_date, return_date).
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
            
        return self.db.execute_query(query, params)


    def get_active_loans(self):
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
        return self.db.execute_query(query)