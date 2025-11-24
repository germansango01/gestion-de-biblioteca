import sqlite3
from datetime import datetime

class Database:
    """
    Gestión de conexión y operaciones básicas con SQLite.
    """
    
    def __init__(self, db_name="library.db"):
        """
        Inicializa la conexión a la base de datos y crea las tablas si no existen.
        
        Args:
            db_name (str): nombre del archivo de la base de datos.
        """
        self.db_name = db_name
        self._connection = None
        self._connect()
        self._setup_tables()


    def _connect(self):
        """Establece la conexión a la base de datos y configura sqlite3."""
        try:
            self._connection = sqlite3.connect(self.db_name)
            self._connection.row_factory = sqlite3.Row 
        except sqlite3.Error as e:
            print("[ERROR] Conexión a la base de datos:", e)
            self._connection = None


    def insert(self, query: str, params: tuple = ()) -> int | None:
        """
        Ejecuta un INSERT y retorna el ID de la fila insertada.

        Args:
            query (str): consulta SQL.
            params (tuple): parámetros para la consulta.

        Returns:
            int | None: ID de la fila insertada o None si falla.
        """
        if not self._connection:
            return None
        try:
            cur = self._connection.cursor()
            cur.execute(query, params)
            self._connection.commit()
            return cur.lastrowid
        except sqlite3.Error:
            return None


    def update(self, query: str, params: tuple = ()) -> bool:
        """
        Ejecuta una consulta UPDATE o cualquier consulta que modifique el estado de la DB (incluyendo CREATE TABLE).

        Args:
            query (str): consulta SQL.
            params (tuple): parámetros para la consulta.

        Returns:
            bool: True si la consulta se ejecutó correctamente, False si falla.
        """
        if not self._connection:
            return False
        try:
            cur = self._connection.cursor()
            cur.execute(query, params)
            self._connection.commit()
            return True
        except sqlite3.Error:
            return False


    def delete(self, query: str, params: tuple = ()) -> bool:
        """
        Ejecuta una consulta DELETE.

        Args:
            query (str): consulta SQL.
            params (tuple): parámetros para la consulta.

        Returns:
            bool: True si la consulta se ejecutó correctamente, False si falla.
        """
        return self.update(query, params)


    def select_one(self, query: str, params: tuple = ()) -> tuple | None:
        """
        Ejecuta un SELECT y retorna una fila como tupla.

        Args:
            query (str): consulta SQL.
            params (tuple): parámetros para la consulta.

        Returns:
            tuple | None: Una fila seleccionada o None si no hay resultados.
        """
        if not self._connection:
            return None
        try:
            cur = self._connection.cursor()
            cur.execute(query, params)
            row = cur.fetchone()
            return tuple(row) if row else None
        except sqlite3.Error:
            return None


    def select_all(self, query: str, params: tuple = ()) -> list[tuple]:
        """
        Ejecuta un SELECT y retorna varias filas como una lista de tuplas.

        Args:
            query (str): consulta SQL.
            params (tuple): parámetros para la consulta.

        Returns:
            list: Lista de tuplas con todos los resultados.
        """
        if not self._connection:
            return []
        try:
            cur = self._connection.cursor()
            cur.execute(query, params)
            return [tuple(r) for r in cur.fetchall()]
        except sqlite3.Error:
            return []


    def _setup_tables(self):
        """
        Crea las tablas 'users', 'books' y 'loans' si no existen.
        """
        self.update("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                deleted_at TEXT NULL
            );
        """)
        self.update("""
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
        self.update("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                user_id INTEGER,
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