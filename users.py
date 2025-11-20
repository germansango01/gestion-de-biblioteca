from database import DatabaseManager

class User:
    """
    Clase para manejar usuarios de la biblioteca, incluyendo la creación y autenticación.
    """

    def __init__(self, db):
        """
        Inicializa el gestor de usuarios y crea la tabla si no existe.

        Args:
            db: Instancia de DatabaseManager.
        """
        self.db = db
        self._setup_table()


    def _setup_table(self):
        """Crea la tabla users si no existe."""
        if self.db is None:
            raise RuntimeError("DatabaseManager no está inicializado.")
            
        self.db.execute_query("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL 
            );
        """)


    def create_user(self, username, password):
        """
        Crea un nuevo usuario con la contraseña hasheada.

        Args:
            username (str): Nombre de usuario único.
            password (str): Contraseña en texto plano.

        Returns:
            bool: True si se creó correctamente, False si falla.
        """
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


    def authenticate(self, username, password):
        """
        Autentica un usuario.

        Args:
            username (str): Nombre de usuario.
            password (str): Contraseña en texto plano.

        Returns:
            int | None: El ID del usuario si la autenticación es exitosa, None en caso contrario.
        """
        result = self.db.execute_query(
            "SELECT id, password_hash FROM users WHERE username = ?;",
            (username,)
        )
        
        if result:
            user_id = result[0][0]
            password_hash = result[0][1]
            
            if isinstance(password_hash, str):
                 password_hash = password_hash.encode('latin-1') 
            
            if self.db.verify_password(password, password_hash):
                return user_id
        
        return None


    def list_users(self):
        """
        Lista todos los usuarios.

        Returns:
            list: Lista de tuplas con (id, username).
        """
        result = self.db.execute_query("SELECT id, username FROM users;")
        return result