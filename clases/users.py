import bcrypt
from clases.database import DatabaseManager 

class User:
    """Clase para gestionar usuarios (creación, autenticación y seguridad)."""

    def __init__(self, db: DatabaseManager):
        """
        Inicializar con el gestor de base de datos.

        Args:
            db (DatabaseManager): Instancia de DatabaseManager.
        """
        self.db = db


    def _hash_password(self, password: str) -> bytes:
        """
        Generar un hash seguro con bcrypt. 
        Return: Hash de bcrypt.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)


    def _verify_password(self, password: str, password_hash: bytes | str) -> bool:
        """
        Verificar si la contraseña coincide con el hash. 
        Return: True si coinciden, False en caso contrario.
        """
        try:
            if isinstance(password_hash, str):
                password_hash = password_hash.encode('latin-1') 
            return bcrypt.checkpw(password.encode('utf-8'), password_hash)
        except Exception:
            return False


    def create_user(self, username: str, password: str) -> bool:
        """
        Crear un nuevo usuario.

        Args:
            username (str): Nombre de usuario único.
            password (str): Contraseña.

        Return:
            bool: True si se creó, False si falla.
        """
        password_hash = self._hash_password(password)
        
        result: int | bool = self.db.insert(
            "INSERT INTO users (username, password_hash) VALUES (?, ?);",
            (username, password_hash)
        )
        return result is not False


    def authenticate(self, username: str, password: str) -> int | None:
        """
        Autenticar un usuario.

        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña.

        Return:
            int | None: ID del usuario si tiene éxito, None en caso contrario.
        """
        result: tuple | None = self.db.select_one(
            "SELECT id, password_hash FROM users WHERE username = ?;",
            (username,)
        )
        
        if result and isinstance(result, tuple):
            user_id = result[0]
            password_hash = result[1]
            
            if self._verify_password(password, password_hash):
                return user_id 
        
        return None


    def list_users(self) -> list:
        """
        Listar todos los usuarios.

        Return:
            list: Lista de tuplas con (id, username).
        """
        return self.db.select_all(
            "SELECT id, username FROM users ORDER BY id ASC;"
        )