import sqlite3

class DatabaseManager:
    """Clase para gestionar la conexión y operaciones con SQLite."""

    def __init__(self, db_name='library.db'):
        self.db_name = db_name
        self._connection = None
        self._connect()
        self._setup_tables()


    def _connect(self):
        """Establece la conexión a la base de datos."""
        try:
            self._connection = sqlite3.connect(self.db_name)
            self._connection.row_factory = sqlite3.Row 
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo conectar a la base de datos: {e}")
            self._connection = None


    def insert(self, query, params=()):
        """
        Ejecuta una consulta INSERT. Retorna el ID de la fila insertada (int) o False si falla.
        """
        if not self._connection: return False
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            self._connection.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error:
            return False


    def update_delete(self, query, params=()):
        """
        Ejecuta consultas UPDATE o DELETE. Retorna True si tiene éxito, False si falla.
        """
        if not self._connection: return False
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            self._connection.commit()
            return True # Retorna un booleano (True)
        except sqlite3.Error:
            return False


    def select_one(self, query, params=()):
        """Ejecuta un SELECT y retorna una única fila como tupla o None."""
        if not self._connection: return None
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchone()
            return tuple(results) if results else None
        except sqlite3.Error:
            return None


    def select_all(self, query, params=()):
        """Ejecuta un SELECT y retorna todas las filas como una lista de tuplas."""
        if not self._connection: return []
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            # Retorna list
            return [tuple(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []


    def _execute_setup_query(self, query):
        """Método simple para CREATE TABLE."""
        if not self._connection: return
        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            self._connection.commit()
        except sqlite3.Error as e:
            print(f"Error al configurar tabla: {e}")


    def _setup_tables(self):
        """Inicializa la estructura de las tablas."""

        if not self._connection: return
        
        # Tabla USERS
        self._execute_setup_query("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                deleted_at TEXT NULL
            );
        """)
        # Tabla BOOKS
        self._execute_setup_query("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                isbn TEXT NOT NULL UNIQUE,
                author TEXT NOT NULL,
                category TEXT NOT NULL,
                available INTEGER NOT NULL DEFAULT 1,
                deleted_at TEXT NULL
            );
        """)
        # Tabla LOANS
        self._execute_setup_query("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NULL,
                user_id INTEGER NULL,
                loan_date TEXT NOT NULL,
                return_date TEXT NULL,
                
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE SET NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            );
        """)

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self._connection:
            self._connection.close()
            self._connection = None