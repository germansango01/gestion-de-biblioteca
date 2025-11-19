import sqlite3
from sqlite3 import Connection, Cursor
from datetime import datetime
import bcrypt

class DatabaseManager:
    """
    Clase genérica para manejar la conexión y consultas en la base de datos SQLite.
    """

    def __init__(self, db_name: str = "library.db"):
        """
        Inicializa DatabaseManager y conecta a la base de datos SQLite.

        Args:
            db_name (str): Nombre del archivo de la base de datos. Por defecto "library.db".
        """
        self.db_name: str = db_name
        self.conn: Connection | None = None
        self.cursor: Cursor | None = None
        self.connect()


    def connect(self):
        """Establece la conexión con la base de datos SQLite."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"[ERROR] No se pudo conectar a la base de datos: {e}")


    def close(self):
        """Cierra la conexión y el cursor de la base de datos."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


    def execute_query(self, query: str, params: tuple = ()) -> list[tuple]:
        """
        Ejecuta una consulta SQL con parámetros opcionales.

        Siempre retorna una lista (vacía si falla o no hay resultados).

        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple): Parámetros para consultas parametrizadas.

        Returns:
            list[tuple]: Resultados de la consulta. Lista vacía si falla o no hay resultados.
        """
        # Asegura al tipador que la conexión y cursor no son None
        if self.cursor is None or self.conn is None:
            raise RuntimeError("La conexión a la base de datos no está establecida.")

        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            if query.strip().upper().startswith("SELECT"):
                return self.cursor.fetchall() or []  # Asegura lista vacía si fetchall devuelve None
            return []
        except sqlite3.Error as e:
            print(f"[ERROR] Consulta fallida: {query}\nParametros: {params}\nError: {e}")
            return []  # Nunca retorna None


    def hash_password(self, password: str) -> bytes:
        """
        Genera un hash seguro para una contraseña usando bcrypt.

        Args:
            password (str): Contraseña en texto plano.

        Returns:
            bytes: Contraseña hasheada.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)


    def verify_password(self, password: str, password_hash: bytes) -> bool:
        """
        Verifica si una contraseña coincide con un hash.

        Args:
            password (str): Contraseña en texto plano.
            password_hash (bytes): Hash de la contraseña a verificar.

        Returns:
            bool: True si coincide, False en caso contrario.
        """
        return bcrypt.checkpw(password.encode(), password_hash)
