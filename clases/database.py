import sqlite3
from datetime import datetime

class Database:
    """
    Gestión de conexión y operaciones básicas con SQLite.
    """
    
    def __init__(self, db_name="library.db"):
        """
        Inicializa la conexión a la base de datos y crea las tablas si no existen.
        
        Args:
            db_name (str): nombre del archivo de la base de datos.
        """
        self.db_name = db_name
        self._connection = None
        self._connect()
        self._setup_tables()


    def _connect(self):
        """Establece la conexión a la base de datos y configura sqlite3."""
        try:
            self._connection = sqlite3.connect(self.db_name)
            self._connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print("[ERROR] Conexión a la base de datos:", e)
            self._connection = None


    def insert(self, query: str, params: tuple = ()) -> int | None:
        """Ejecuta un INSERT y retorna el ID de la fila insertada."""
        if not self._connection:
            return None
        try:
            with self._connection as conn:
                cur = conn.cursor()
                cur.execute(query, params)
                return cur.lastrowid
        except sqlite3.Error as e:
            print("[ERROR] insert:", e)
            return None


    def update(self, query: str, params: tuple = ()) -> bool:
        """Ejecuta un UPDATE o cualquier consulta que modifique la DB."""
        if not self._connection:
            return False
        try:
            with self._connection as conn:
                cur = conn.cursor()
                cur.execute(query, params)
                return True
        except sqlite3.Error as e:
            print("[ERROR] update:", e)
            return False


    def delete(self, query: str, params: tuple = ()) -> bool:
        """Ejecuta un DELETE."""
        return self.update(query, params)


    def select_one(self, query: str, params: tuple = ()) -> tuple | None:
        """Ejecuta un SELECT y retorna una fila como tupla."""
        if not self._connection:
            return None
        try:
            with self._connection as conn:
                cur = conn.cursor()
                cur.execute(query, params)
                row = cur.fetchone()
                return tuple(row) if row else None
        except sqlite3.Error as e:
            print("[ERROR] select_one:", e)
            return None


    def select_all(self, query: str, params: tuple = ()) -> list[tuple]:
        """Ejecuta un SELECT y retorna varias filas como lista de tuplas."""
        if not self._connection:
            return []
        try:
            with self._connection as conn:
                cur = conn.cursor()
                cur.execute(query, params)
                return [tuple(r) for r in cur.fetchall()]
        except sqlite3.Error as e:
            print("[ERROR] select_all:", e)
            return []


    def _setup_tables(self):
        """Crea las tablas 'users', 'books' y 'loans' si no existen."""
        self.update("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                deleted_at TEXT NULL
            );
        """)
        self.update("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                isbn TEXT NOT NULL UNIQUE,
                author TEXT NOT NULL,
                category TEXT NOT NULL,
                available INTEGER NOT NULL DEFAULT 1,
                deleted_at TEXT NULL
            );
        """)
        self.update("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                user_id INTEGER,
                loan_date TEXT NOT NULL,
                return_date TEXT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE SET NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            );
        """)


    def seed_data(self):
        """
        Inserta 5 usuarios y 20 libros si la BD está vacía.
        """

        # Usuarios
        existing_users = self.select_all("SELECT id FROM users")
        if not existing_users:
            users = [
                ("german", "german@example.com", "pass123"),
                ("manuel", "manuel@example.com", "pass123"),
                ("carol", "carol@example.com", "pass123"),
                ("dave", "dave@example.com", "pass123"),
                ("eve", "eve@example.com", "pass123")
            ]
            for u in users:
                self.insert("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", u)

        # Libros
        existing_books = self.select_all("SELECT id FROM books")
        if not existing_books:
            books = [
                ("Cien Años de Soledad", "9783161484100", "Gabriel García Márquez", "Novela"),
                ("Don Quijote de la Mancha", "9780142437230", "Miguel de Cervantes", "Novela"),
                ("1984", "9780452284234", "George Orwell", "Distopía"),
                ("El Principito", "9780156012195", "Antoine de Saint-Exupéry", "Infantil"),
                ("Orgullo y Prejuicio", "9780199535569", "Jane Austen", "Romántico"),
                ("La Odisea", "9780140268867", "Homero", "Épica"),
                ("Hamlet", "9780141015866", "William Shakespeare", "Drama"),
                ("Crimen y Castigo", "9780140449136", "Fiódor Dostoyevski", "Novela"),
                ("El Hobbit", "9780618002213", "J.R.R. Tolkien", "Fantasía"),
                ("Moby Dick", "9780142437247", "Herman Melville", "Aventura"),
                ("Guerra y Paz", "9780143039990", "León Tolstói", "Novela"),
                ("El Nombre de la Rosa", "9780140178453", "Umberto Eco", "Misterio"),
                ("La Divina Comedia", "9780140448955", "Dante Alighieri", "Épica"),
                ("Frankenstein", "9780141439471", "Mary Shelley", "Terror"),
                ("Drácula", "9780141439846", "Bram Stoker", "Terror"),
                ("Alicia en el País de las Maravillas", "9780141439761", "Lewis Carroll", "Infantil"),
                ("Veinte mil leguas de viaje submarino", "9780140444308", "Julio Verne", "Aventura"),
                ("El Conde de Montecristo", "9780140449266", "Alexandre Dumas", "Aventura"),
                ("Rayuela", "9780143039952", "Julio Cortázar", "Novela"),
                ("Cumbres Borrascosas", "9780141439556", "Emily Brontë", "Novela")
            ]
            for b in books:
                self.insert(
                    "INSERT INTO books (title, isbn, author, category) VALUES (?, ?, ?, ?)", b
                )


    def close(self):
        """Cierra la conexión a la base de datos."""
        if self._connection:
            self._connection.close()
            self._connection = None
