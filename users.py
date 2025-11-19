from database import DatabaseManager

class User:
    """
    Clase para manejar usuarios de la biblioteca.
    """


    def __init__(self, db: DatabaseManager):
        """
        Inicializa el gestor de usuarios y crea la tabla si no existe.

        Args:
            db (DatabaseManager): Instancia de DatabaseManager.
        """
        self.db = db
        self._setup_table()


    def _setup_table(self):
        """Crea la tabla users si no existe."""
        if self.db is None:
            raise RuntimeError("DatabaseManager no está inicializado")
        self.db.execute_query("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
        """)


    def create_user(self, username: str, password: str) -> bool:
        """Crea un usuario con contraseña hasheada."""
        try:
            password_hash = self.db.hash_password(password)
            self.db.execute_query(
                "INSERT INTO users (username, password_hash) VALUES (?, ?);",
                (username, password_hash)
            )
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo crear el usuario: {e}")
            return False


    def authenticate(self, username: str, password: str) -> bool:
        """Autentica un usuario."""
        result = self.db.execute_query(
            "SELECT password_hash FROM users WHERE username = ?;",
            (username,)
        )
        if result:
            return self.db.verify_password(password, result[0][0])
        return False


    def list_users(self) -> list[tuple]:
        """Lista todos los usuarios."""
        result = self.db.execute_query("SELECT id, username FROM users;")
        return result
