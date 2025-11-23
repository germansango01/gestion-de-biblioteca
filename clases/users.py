import bcrypt
from datetime import datetime
from clases.database import DatabaseManager

class User:
    """Clase para gestionar usuarios (CRUD y Autenticación)."""

    def __init__(self, db: DatabaseManager):
        self.db = db


    def create_user(self, username, password):
        """Crea un nuevo usuario (activo). Retorna bool."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # insert() devuelve ID (int) o False
        result = self.db.insert(
            "INSERT INTO users (username, password) VALUES (?, ?);",
            (username, hashed_password)
        )
        return result is not False


    def list_users(self):
        """Lista solo usuarios activos (deleted_at IS NULL). Retorna list."""
        return self.db.select_all("SELECT id, username FROM users WHERE deleted_at IS NULL ORDER BY username ASC")


    def authenticate(self, username, password):
        """Autentica solo usuarios activos. Retorna ID (int) o None."""
        # select_one() devuelve tuple o None
        user_data = self.db.select_one(
            "SELECT id, password FROM users WHERE username = ? AND deleted_at IS NULL;",
            (username,)
        )
        
        if user_data:
            user_id, hashed_password = user_data
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return user_id
        return None


    def delete_user(self, user_id):
        """Realiza un soft delete de un usuario. Retorna bool."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # update_delete() devuelve True o False
        return self.db.update_delete(
            "UPDATE users SET deleted_at = ? WHERE id = ? AND deleted_at IS NULL;",
            (timestamp, user_id)
        )