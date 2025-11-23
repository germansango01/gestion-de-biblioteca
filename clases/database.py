import sqlite3
from datetime import datetime

class Database:
    """Clase para gestionar la conexión y operaciones con SQLite."""

    def __init__(self, db_name="library.db"):
        """Inicializa la base de datos y las tablas.

        Args:
            db_name (str): Nombre del archivo de base de datos SQLite.
        """
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
            print("[ERROR] Conexión a la base de datos:", e)
            self._connection = None


    def _execute_setup_query(self, query):
        """Ejecuta queries de creación de tablas.

        Args:
            query (str): Consulta SQL para creación de tabla.
        """
        if not self._connection:
            return
        try:
            cur = self._connection.cursor()
            cur.execute(query)
            self._connection.commit()
        except sqlite3.Error as e:
            print("Error creando tabla:", e)


    def _setup_tables(self):
        """Crea las tablas principales si no existen."""
        self._execute_setup_query("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                deleted_at TEXT NULL
            );
        """)
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
        self._execute_setup_query("""
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


    def insert(self, query, params=()):
        """Ejecuta un INSERT.

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


    def update(self, query, params=()):
        """Ejecuta un UPDATE.

        Returns:
            bool: True si se ejecutó correctamente, False si falla.
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


    def delete(self, query, params=()):
        """Ejecuta un DELETE.

        Returns:
            bool: True si se ejecutó correctamente, False si falla.
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


    def select_one(self, query, params=()):
        """Ejecuta un SELECT y devuelve la primera fila.

        Returns:
            tuple | None: Primera fila como tupla o None si no existe.
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


    def select_all(self, query, params=()):
        """Ejecuta un SELECT y devuelve todas las filas.

        Returns:
            list: Lista de tuplas con todas las filas.
        """
        if not self._connection:
            return []
        try:
            cur = self._connection.cursor()
            cur.execute(query, params)
            return [tuple(r) for r in cur.fetchall()]
        except sqlite3.Error:
            return []


    def close(self):
        """Cierra la conexión con la base de datos."""
        if self._connection:
            self._connection.close()
            self._connection = None
