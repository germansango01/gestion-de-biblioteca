import sqlite3
from sqlite3 import Cursor

class DatabaseManager:
    """Clase para gestionar la conexión a SQLite y exponer métodos CRUD específicos."""

    def __init__(self, db_name: str = "library.db"):
        """
        Inicializar el DatabaseManager.

        Args:
            db_name (str): Nombre del archivo de base de datos.
        """
        self.db_name = db_name
        self._connection: sqlite3.Connection | None = None
        self._cursor: Cursor | None = None


    def connect(self) -> None:
        """Establecer la conexión a la base de datos e inicializa las tablas."""
        if self._connection is not None:
            return
        try:
            self._connection = sqlite3.connect(self.db_name)
            self._cursor = self._connection.cursor()
            self._cursor.execute("PRAGMA foreign_keys = ON;") 
            self._setup_tables()
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo conectar a la base de datos: {e}")
            self._connection = None


    def disconnect(self) -> None:
        """Cerrar la conexión y el cursor de la base de datos."""
        if self._cursor: self._cursor.close()
        if self._connection: self._connection.close()


    def _setup_tables(self) -> None:
        """Inicializar la estructura de las tablas."""
        if not self._connection: return
        
        self._execute_write_query("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL
            );
        """)
        self._execute_write_query("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                author TEXT,
                category TEXT DEFAULT '',
                available INTEGER NOT NULL DEFAULT 1
            );
        """)
        self._execute_write_query("""
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


    def _execute_write_query(self, query: str, params: tuple = ()) -> bool:
        """
        Ejecutar consultas de escritura (UPDATE/DELETE/CREATE). 
        Return: True o False.
        """
        if not self._cursor or not self._connection: return False
        try:
            self._cursor.execute(query, params)
            self._connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"[ERROR] Violación de unicidad (IntegrityError): {e}")
            return False
        except sqlite3.Error as e:
            print(f"[ERROR] Consulta de escritura falló: {e}")
            return False


    def select_one(self, query: str, params: tuple = ()) -> tuple | None:
        """
        Ejecutar SELECT para obtener un solo registro.

        Args:
            query (str): Consulta SQL SELECT.
            params (tuple): Parámetros de la consulta.

        Return:
            tuple | None: Tupla con la fila o None si no se encontró o falla.
        """
        if not self._cursor: return None
        try:
            self._cursor.execute(query, params)
            return self._cursor.fetchone() 
        except sqlite3.Error as e:
            print(f"[ERROR] Consulta SELECT_ONE falló: {e}")
            return None


    def select_all(self, query: str, params: tuple = ()) -> list:
        """
        Ejecutar SELECT para para obtener todos los registros.

        Args:
            query (str): Consulta SQL SELECT.
            params (tuple): Parámetros de la consulta.

        Return:
            list: Lista de tuplas o lista vacía si no hay resultados/falla.
        """
        if not self._cursor: return []
        try:
            self._cursor.execute(query, params)
            return self._cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[ERROR] Consulta SELECT_ALL falló: {e}")
            return []


    def insert(self, query: str, params: tuple = ()) -> int | bool:
        """
        Ejecutar INSERT.

        Args:
            query (str): Consulta SQL INSERT.
            params (tuple): Parámetros de la consulta.

        Return:
            int | bool: ID de la nueva fila (int) o False si falla.
        """
        if not self._cursor or not self._connection: return False
        try:
            self._cursor.execute(query, params)
            self._connection.commit()
            
            last_id: int | None = self._cursor.lastrowid
            
            if last_id is not None:
                return last_id
            else:
                print("[WARNING] Inserción exitosa, pero no se pudo obtener lastrowid.")
                return False 
        except sqlite3.IntegrityError as e:
            print(f"[ERROR] Violación de unicidad (IntegrityError) en INSERT: {e}")
            return False
        except sqlite3.Error as e:
            print(f"[ERROR] Consulta INSERT falló: {e}")
            return False


    def update(self, query: str, params: tuple = ()) -> bool:
        """
        Ejecutar UPDATE.

        Args:
            query (str): Consulta SQL UPDATE.
            params (tuple): Parámetros de la consulta.

        Return:
            bool: True si fue exitoso, False si falla.
        """
        return self._execute_write_query(query, params)


    def delete(self, query: str, params: tuple = ()) -> bool:
        """
        Ejecutar DELETE.

        Args:
            query (str): Consulta SQL DELETE.
            params (tuple): Parámetros de la consulta.

        Return:
            bool: True si fue exitoso, False si falla.
        """
        return self._execute_write_query(query, params)