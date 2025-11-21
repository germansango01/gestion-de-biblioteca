from clases.database import DatabaseManager

class User:
    """Clase para gestionar usuarios de la biblioteca, incluyendo la creación y autenticación."""

    def __init__(self, db: DatabaseManager):
        """
        Inicializa el gestor de usuarios.

        Args:
            db (DatabaseManager): Instancia del gestor de base de datos.
        """
        self.db = db


    def create_user(self, username: str, password: str) -> bool:
        """
        Crea un nuevo usuario con la contraseña hasheada.

        Args:
            username (str): Nombre de usuario único.
            password (str): Contraseña en texto plano.

        Returns:
            bool: True si se creó correctamente, False si falla (por duplicidad o error de DB).
        """
        password_hash = self.db.hash_password(password)
        
        result = self.db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?);",
            (username, password_hash)
        )
        return result is not False


    def authenticate(self, username: str, password: str) -> int | None:
        """
        Autentica un usuario.

        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña en texto plano.

        Returns:
            int | None: El ID del usuario si la autenticación es exitosa, None en caso contrario.
        """
        # (fetch_one=True)
        result = self.db.execute(
            "SELECT id, password_hash FROM users WHERE username = ?;",
            (username,),
            fetch_one=True
        )
        
        if result:
            user_id = result[0]
            password_hash = result[1]
            
            if self.db.verify_password(password, password_hash):
                return user_id
        
        return None


    def list_users(self) -> list:
        """
        Lista todos los usuarios.

        Returns:
            list: Lista de tuplas con (id, username).
        """
        return self.db.execute("SELECT id, username FROM users ORDER BY id ASC;")