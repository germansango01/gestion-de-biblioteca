import sqlite3
import bcrypt

class DatabaseManager:
    """
    Clase para manejar la conexión y consultas en la base de datos SQLite.
    """

    def __init__(self, db_name="library.db"):
        """
        Inicializa DatabaseManager.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None


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


    def execute_query(self, query, params=()):
        """
        Ejecuta una consulta SQL con parámetros opcionales.

        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple): Parámetros para consultas parametrizadas.

        Returns:
            list: Resultados de la consulta. Lista vacía si falla o no hay resultados.
        """
        if not self.cursor or not self.conn:
             print("[ERROR] La conexión a la base de datos no está establecida.")
             return []

        try:
            self.cursor.execute(query, params)
            
            if not query.strip().upper().startswith("SELECT"):
                 self.conn.commit()

            if query.strip().upper().startswith("SELECT"):
                return self.cursor.fetchall()
            
            return []
        except sqlite3.Error as e:
            print(f"[ERROR] Consulta fallida: {query}\nError: {e}")
            return []


    def hash_password(self, password):
        """
        Genera un hash seguro para una contraseña usando bcrypt.

        Args:
            password (str): Contraseña en texto plano.

        Returns:
            bytes: Contraseña hasheada.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)


    def verify_password(self, password, password_hash):
        """
        Verifica si una contraseña coincide con un hash.

        Args:
            password (str): Contraseña en texto plano.
            password_hash (bytes): Hash de la contraseña a verificar.

        Returns:
            bool: True si coincide, False en caso contrario.
        """
        return bcrypt.checkpw(password.encode('utf-8'), password_hash)