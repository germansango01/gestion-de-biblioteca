import re
import bcrypt
from datetime import datetime
from clases.database import Database

class User:
    """
    Gestión de usuarios, incluyendo autenticación.
    """

    def __init__(self, db: Database):
        self.db = db


    def get_by_id(self, user_id: int) -> tuple | None:
        """
        Obtener un usuario activo por ID.

        Returns:
            tuple | None: (id, username, email) o None.
        """
        return self.db.select_one(
            "SELECT id, username, email FROM users WHERE id=? AND deleted_at IS NULL;",
            (user_id,)
        )


    @staticmethod
    def validate(username: str, password: str, email: str | None = None) -> dict:
        """
        Valida campos de usuario (validación básica de longitud).
        
        Args:
            email (str | None): Campo opcional. Si se proporciona, también se valida.
        """
        errors = {}
        if not username or len(username.strip()) < 4:
            errors['username'] = "Mínimo 4 caracteres."
        if not password or len(password.strip()) < 6:
            errors['password'] = "Mínimo 6 caracteres."
        
        if email is not None and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors['email'] = "Formato de email inválido."

        return errors


    def _validate_uniqueness(self, username: str, email: str, current_id: int | None = None) -> dict:
        """
        Verifica la unicidad de username y email en la base de datos.
        """
        errors = {}
        
        # Verificar unicidad de username
        query_u = "SELECT id FROM users WHERE username=? AND deleted_at IS NULL"
        params_u = (username,)
        
        # Verificar unicidad de email
        query_e = "SELECT id FROM users WHERE email=? AND deleted_at IS NULL"
        params_e = (email,)

        # Excluir el ID actual si estamos actualizando un usuario
        if current_id is not None:
            query_u += " AND id!=?"
            params_u = (username, current_id)
            query_e += " AND id!=?"
            params_e = (email, current_id)

        if self.db.select_one(query_u, params_u):
            errors['username'] = "Este nombre de usuario ya está registrado."
            
        if self.db.select_one(query_e, params_e):
            errors['email'] = "Este email ya está registrado."
            
        return errors


    def create(self, username: str, email: str, password: str) -> bool | dict:
        """
        Crear un nuevo usuario activo con email y contraseña hasheada.

        Args:
            username (str): nombre de usuario (debe ser único).
            email (str): correo electrónico (debe ser único).
            password (str): contraseña en texto plano.

        Returns:
            bool | dict: True si se creó, dict de errores de unicidad si falla.
        """
        username = username.strip()
        email = email.strip()
        
        # Validar unicidad en la base de datos
        errors = self._validate_uniqueness(username, email)
        if errors:
            return errors

        # Hashing de la contraseña.
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        result = self.db.insert(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?);",
            (username, email, hashed)
        )
        return result is not None


    def list(self) -> list[tuple]:
        """
        Lista todos los usuarios activos.

        Returns:
            list: Lista de tuplas con (id, username, email).
        """
        return self.db.select_all(
            "SELECT id, username, email FROM users WHERE deleted_at IS NULL ORDER BY username ASC;"
        )


    def authenticate(self, username: str, password: str) -> int | None:
        """
        Autenticar un usuario activo por username.

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


    def soft_delete(self, user_id: int) -> dict | bool:
        """
        Realizar un borrado lógico (soft delete) de un usuario, 
        verificando que no tenga préstamos activos.
        
        Returns:
            dict | bool: True si éxito, o dict de error si tiene préstamos.
        """
        # Verificar préstamos activos
        active_loans = self.db.select_one("SELECT COUNT(*) FROM loans WHERE user_id=? AND return_date IS NULL", (user_id,))
        if active_loans and active_loans[0] > 0:
            return {'general': f'El usuario tiene {active_loans[0]} préstamos activos y no puede ser eliminado.'}
        
        # Proceder con el borrado suave
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.db.update(
            "UPDATE users SET deleted_at=? WHERE id=? AND deleted_at IS NULL;",
            (ts, user_id)
        )


    def find_id_by_username(self, username: str) -> int | None:
        """
        Buscar el ID de un usuario activo por su username.
        """
        row = self.db.select_one(
            "SELECT id FROM users WHERE username=? AND deleted_at IS NULL;",
            (username,)
        )
        return row[0] if row else None