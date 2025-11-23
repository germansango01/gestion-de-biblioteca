import bcrypt
from datetime import datetime
from database import Database

class User:
    """Gestión de usuarios: creación, listado, autenticación y borrado lógico."""

    def __init__(self, db: Database):
        self.db = db


    def create(self, username, password):
        """Crea un usuario.

        Returns:
            bool
        """
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        return self.db.insert(
            "INSERT INTO users (username, password) VALUES (?, ?);",
            (username, hashed)
        ) is not None


    def list(self):
        """Lista usuarios activos.

        Returns:
            list
        """
        return self.db.select_all("SELECT id, username FROM users WHERE deleted_at IS NULL ORDER BY username ASC;")


    def authenticate(self, username, password):
        """Autentica un usuario.

        Returns:
            int | None: ID del usuario si autenticado, None si falla.
        """
        row = self.db.select_one("SELECT id, password FROM users WHERE username=? AND deleted_at IS NULL;", (username,))
        if not row:
            return None
        user_id, hashed = row
        if bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8")):
            return user_id
        return None


    def soft_delete(self, user_id):
        """Borrado lógico de un usuario.

        Returns:
            bool
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.db.update("UPDATE users SET deleted_at=? WHERE id=? AND deleted_at IS NULL;", (ts, user_id))


    def get_by_id(self, user_id):
        """Obtiene un usuario activo por ID.

        Returns:
            tuple | None
        """
        return self.db.select_one("SELECT id, username, password FROM users WHERE id=? AND deleted_at IS NULL;", (user_id,))


    def find_id_by_username(self, username):
        """Obtiene el ID de un usuario activo por username.

        Returns:
            int | None
        """
        row = self.db.select_one("SELECT id FROM users WHERE username=? AND deleted_at IS NULL;", (username,))
        return row[0] if row else None
