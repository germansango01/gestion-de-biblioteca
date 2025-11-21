import sqlite3
import bcrypt

class DatabaseManager:
    """
    Clase para gestionar la conexión y las operaciones de la base de datos SQLite.
    """

    def __init__(self, db_name="library.db"):
        """
        Inicializa DatabaseManager.
        """
        self.db_name = db_name
        self._conn = None
        self._cursor = None


    def connect_db(self):
        """Establece la conexión con la base de datos SQLite y configura las tablas."""
        if self._conn is not None:
            return

        try:
            self._conn = sqlite3.connect(self.db_name)
            self._cursor = self._conn.cursor()
            self._cursor.execute("PRAGMA foreign_keys = ON;") 
            self._setup_db()
        except sqlite3.Error as e:
            print(f"[ERROR] Could not connect to the database: {e}")
            self._conn = None


    def close_db(self):
        """Cierra la conexión y el cursor de la base de datos."""
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._conn:
            self._conn.close()
            self._conn = None


    def _setup_db(self):
        """Inicializa y verifica la estructura de todas las tablas requeridas."""
        if not self._conn: return

        # Tabla de Usuarios
        self.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL
            );
        """)

        # 🛑 Tabla de Autores ELIMINADA 🛑
        
        # Tabla de Libros (Campo 'author' añadido, 'author_id' y FOREIGN KEY eliminados)
        self.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                author TEXT,                     -- ⬅️ Nuevo campo de texto para el nombre del autor
                category TEXT DEFAULT '',
                available INTEGER NOT NULL DEFAULT 1
                -- 🛑 FOREIGN KEY (author_id) REFERENCES authors(id) ELIMINADA 🛑
            );
        """)

        # Tabla de Préstamos
        self.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                loan_date TEXT NOT NULL,
                return_date TEXT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)


    def execute(self, query, params=(), commit=True, fetch_one=False):
        """
        Ejecuta una consulta SQL con parámetros opcionales.

        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple): Parámetros para consultas parametrizadas.
            commit (bool): True si es una operación de escritura (INSERT, UPDATE, DELETE).
            fetch_one (bool): Si es True y es un SELECT, retorna solo el primer resultado.

        Returns:
            list | tuple | bool: Resultados de la consulta (list/tuple) o False si falla por IntegrityError.
        """
        if not self._cursor or not self._conn:
            print("[ERROR] Database connection is not established.")
            return []

        try:
            self._cursor.execute(query, params)
            
            if commit:
                self._conn.commit()

            if query.strip().upper().startswith("SELECT"):
                return self._cursor.fetchone() if fetch_one else self._cursor.fetchall()
            
            # Retorna el ID de la última fila insertada para operaciones INSERT
            if query.strip().upper().startswith("INSERT"):
                return self._cursor.lastrowid
            
            return True # Éxito en operaciones que no son SELECT/INSERT
            
        except sqlite3.IntegrityError as e:
            # Error común por duplicidad (p. ej., ISBN o username repetido)
            print(f"[ERROR] Uniqueness violation (IntegrityError) in query. Error: {e}")
            return False
        except sqlite3.Error as e:
            print(f"[ERROR] Query failed: {query}\nError: {e}")
            return False


    def hash_password(self, password: str) -> bytes:
        """
        Genera un hash seguro para una contraseña usando bcrypt.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)


    def verify_password(self, password: str, password_hash) -> bool:
        """
        Verifica si una contraseña coincide con un hash.
        """
        try:
            # Asegura que el hash sea bytes para bcrypt
            if isinstance(password_hash, str):
                password_hash = password_hash.encode('latin-1') 
            
            return bcrypt.checkpw(password.encode('utf-8'), password_hash)
        except Exception:
            # Falla si el hash es inválido o el formato es incorrecto
            return False