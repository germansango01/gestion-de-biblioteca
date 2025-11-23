import bcrypt
from datetime import datetime
from clases.database import Database

class User:
    """Gestión de usuarios y autenticación en la biblioteca."""

    def __init__(self, db):
        """
        Inicializa la clase con la base de datos.

        Args:
            db (Database): instancia de la clase Database.
        """
        self.db = db


    def create(self, username, password):
        """
        Crea un nuevo usuario activo.

        Args:
            username (str): nombre de usuario.
            password (str): contraseña en texto plano.

        Returns:
            bool: True si se creó correctamente, False si falla.
        """
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        return self.db.insert(
            "INSERT INTO users (username, password) VALUES (?, ?);",
            (username, hashed)
        ) is not None


    def list(self):
        """
        Lista todos los usuarios activos.

        Returns:
            list: Lista de tuplas con (id, username).
        """
        return self.db.select_all(
            "SELECT id, username FROM users WHERE deleted_at IS NULL ORDER BY username ASC;"
        )


    def authenticate(self, username, password):
        """
        Autentica un usuario activo.

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
        if bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8")):
            return user_id
        return None


    def soft_delete(self, user_id):
        """
        Realiza un borrado lógico (soft delete) de un usuario.

        Args:
            user_id (int): ID del usuario.

        Returns:
            bool: True si se eliminó correctamente, False si falla.
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.db.update(
            "UPDATE users SET deleted_at=? WHERE id=? AND deleted_at IS NULL;",
            (ts, user_id)
        )


    def get_by_id(self, user_id):
        """
        Obtiene un usuario activo por ID.

        Args:
            user_id (int): ID del usuario.

        Returns:
            tuple | None: (id, username, password) o None si no existe.
        """
        return self.db.select_one(
            "SELECT id, username, password FROM users WHERE id=? AND deleted_at IS NULL;",
            (user_id,)
        )


    def find_id_by_username(self, username):
        """
        Busca el ID de un usuario activo por su username.

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
