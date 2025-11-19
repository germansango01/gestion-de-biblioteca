from database import DatabaseManager

class History:
    """
    Clase para manejar el historial de préstamos de libros.
    """


    def __init__(self, db: DatabaseManager):
        """
        Inicializa el gestor de historial y crea la tabla si no existe.

        Args:
            db (DatabaseManager): Instancia de DatabaseManager.
        """
        self.db = db
        self._setup_table()


    def _setup_table(self):
        """Crea la tabla loans si no existe."""
        if self.db is None:
            raise RuntimeError("DatabaseManager no está inicializado")
        self.db.execute_query("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                loan_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)


    def get_loans(self, user_id: int | None = None) -> list[tuple]:
        """
        Obtiene el historial de préstamos, opcionalmente filtrado por usuario.

        Args:
            user_id (int | None, optional): ID del usuario para filtrar préstamos.

        Returns:
            list[tuple]: Lista de préstamos (loan_id, book_title, username, loan_date, return_date).
        """
        query = """
            SELECT l.id, b.title, u.username, l.loan_date, l.return_date
            FROM loans l
            JOIN books b ON l.book_id = b.id
            JOIN users u ON l.user_id = u.id
        """
        params: tuple = ()
        if user_id is not None:
            query += " WHERE u.id = ?"
            params = (user_id,)
        return self.db.execute_query(query, params)
