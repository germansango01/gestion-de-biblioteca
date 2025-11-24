import bcrypt
from datetime import datetime
from clases.database import Database # Asumiendo la ruta correcta

class User:
    """Gestión de usuarios, incluyendo autenticación y borrado lógico."""

    def __init__(self, db: Database):
        """
        Inicializar la clase con la base de datos.

        Args:
            db (Database): instancia de la clase Database.
        """
        self.db = db
        
    def get_by_id(self, user_id: int) -> tuple | None:
        """
        Obtener un usuario activo por ID.

        Args:
            user_id (int): ID del usuario.

        Returns:
            tuple | None: (id, username, password) o None si no existe o está borrado.
        """
        return self.db.select_one(
            "SELECT id, username, password FROM users WHERE id=? AND deleted_at IS NULL;",
            (user_id,)
        )

    def create(self, username: str, password: str) -> bool:
        """
        Crear un nuevo usuario activo con la contraseña hasheada.

        Args:
            username (str): nombre de usuario (debe ser único).
            password (str): contraseña en texto plano.

        Returns:
            bool: True si se creó correctamente, False si falla (ej. username duplicado).
        """
        # Hashing de la contraseña.
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        return self.db.insert(
            "INSERT INTO users (username, password) VALUES (?, ?);",
            (username, hashed)
        ) is not None


    def list(self) -> list[tuple]:
        """
        Lista todos los usuarios activos.

        Returns:
            list: Lista de tuplas con (id, username).
        """
        return self.db.select_all(
            "SELECT id, username FROM users WHERE deleted_at IS NULL ORDER BY username ASC;"
        )


    def authenticate(self, username: str, password: str) -> int | None:
        """
        Autenticar un usuario activo.

        Args:
            username (str): nombre de usuario.
            password (str): contraseña en texto plano.

        Returns:
            int | None: ID del usuario si autenticación correcta, None si falla.
        """
        row = self.db.select_one(
            "SELECT id, password FROM users WHERE username=? AND deleted_at IS NULL;",
            (username,)
        )
        if not row:
            return None

        user_id, hashed = row
        # Validación de la contraseña.
        if bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8")):
            return user_id
        return None


    def soft_delete(self, user_id: int) -> bool:
        """
        Realizar un borrado lógico (soft delete) de un usuario.

        Args:
            user_id (int): ID del usuario.

        Returns:
            bool: True si se eliminó (actualizó) correctamente, False si falla.
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Uso del método delete() de Database (que internamente llama a update)
        return self.db.delete(
            "UPDATE users SET deleted_at=? WHERE id=? AND deleted_at IS NULL;",
            (ts, user_id)
        )


    def find_id_by_username(self, username: str) -> int | None:
        """
        Buscar el ID de un usuario activo por su username.

        Args:
            username (str): nombre de usuario.

        Returns:
            int | None: ID del usuario o None si no existe.
        """
        row = self.db.select_one(
            "SELECT id FROM users WHERE username=? AND deleted_at IS NULL;",
            (username,)
        )
        return row[0] if row else None