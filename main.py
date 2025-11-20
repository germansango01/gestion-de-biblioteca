import os
from database import DatabaseManager
from users import User
from books import Book
from history import History

# Nombre de la base de datos de la demo
DB_NAME = "library_demo.db"

def run_demo():
    """Ejecuta una demostración del flujo de trabajo del sistema de biblioteca."""
    
    # --- Preparación ---
    print("--- 1. CONFIGURACIÓN INICIAL ---")
    
    # Si el archivo DB existe de una ejecución anterior, lo eliminamos para empezar limpio
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Archivo '{DB_NAME}' anterior eliminado.")

    # Inicializar y Conectar la DB
    db = DatabaseManager(db_name=DB_NAME)
    db.connect()
    print(f"Conexión a '{DB_NAME}' establecida.")
    
    # Inicializar los gestores
    user_manager = User(db)
    book_manager = Book(db)
    history_manager = History(db)
    print("Gestores de clases inicializados y tablas creadas.")

    # --- 2. GESTIÓN DE USUARIOS ---
    print("\n--- 2. CREACIÓN Y AUTENTICACIÓN DE USUARIO ---")
    
    # Crear usuario
    print("Creando usuario 'admin'...")
    user_manager.create_user("admin", "securepass")
    
    # Autenticar usuario (debe devolver el ID)
    admin_id = user_manager.authenticate("admin", "securepass")
    if admin_id:
        print(f"Autenticación exitosa. ID del usuario: {admin_id}")
    else:
        print("ERROR: Fallo al autenticar. Terminando demo.")
        db.close()
        return

    # Listar usuarios
    users = user_manager.list_users()
    print(f"Usuarios en el sistema: {users}")

    # --- 3. GESTIÓN DE LIBROS ---
    print("\n--- 3. AGREGAR LIBROS ---")
    
    # Agregar libros
    book_manager.add_book("El Gran Gatsby", "978-3123456789", "F. Scott Fitzgerald", "Clásico")
    book_manager.add_book("Sapiens", "978-0062316097", "Yuval Noah Harari", "Historia")
    book_manager.add_book("1984", "978-0451524935", "George Orwell", "Distopía")

    all_books = book_manager.list_books()
    print(f"Libros totales agregados: {len(all_books)}")
    
    # Obtener IDs de libros
    gatsby_id = all_books[0][0]
    sapiens_id = all_books[1][0]
    
    # Listar disponibles antes del préstamo
    available_before = book_manager.list_books(available_only=True)
    print(f"Libros disponibles antes de prestar: {len(available_before)}")

    # --- 4. PRÉSTAMO Y DEVOLUCIÓN ---
    print("\n--- 4. EMULACIÓN DE PRÉSTAMO ---")
    
    # Prestar Gatsby
    print(f"Prestando 'El Gran Gatsby' (ID: {gatsby_id}) al usuario ID: {admin_id}")
    book_manager.lend_book(gatsby_id, admin_id)
    
    # Prestar Sapiens
    print(f"Prestando 'Sapiens' (ID: {sapiens_id}) al usuario ID: {admin_id}")
    book_manager.lend_book(sapiens_id, admin_id)

    # Listar préstamos activos
    active_loans = history_manager.get_active_loans()
    print(f"\n--- Préstamos Activos ({len(active_loans)}) ---")
    for loan in active_loans:
        print(f"  ID Préstamo: {loan[0]}, Libro: {loan[1]}, Fecha: {loan[3]}")
        
    # Listar disponibles después del préstamo
    available_after = book_manager.list_books(available_only=True)
    print(f"\nLibros disponibles después de prestar: {len(available_after)}")
    
    # Devolver Gatsby
    print(f"\nDevolviendo 'El Gran Gatsby' (ID: {gatsby_id})")
    book_manager.return_book(gatsby_id)
    
    # --- 5. VERIFICACIÓN FINAL ---
    print("\n--- 5. VERIFICACIÓN FINAL ---")
    
    # Listar préstamos activos (solo debe quedar Sapiens)
    active_loans_final = history_manager.get_active_loans()
    print(f"Préstamos Activos Finales ({len(active_loans_final)}):")
    for loan in active_loans_final:
        print(f"  ID Préstamo: {loan[0]}, Libro: {loan[1]}") # Solo debe mostrar Sapiens
        
    # Listar historial completo del usuario
    full_history = history_manager.get_loans(user_id=admin_id)
    print(f"\nHistorial completo del usuario ID {admin_id} ({len(full_history)} entradas):")
    for hist in full_history:
        # Formato: (loan_id, book_title, username, loan_date, return_date)
        status = "DEVUELTO" if hist[4] else "ACTIVO"
        print(f"  {hist[1]} - Estado: {status} (Devolución: {hist[4]})")

    # --- 6. CIERRE ---
    print("\n--- 6. CIERRE DE CONEXIÓN ---")
    db.close()
    print("Conexión a la base de datos cerrada.")

if __name__ == '__main__':
    run_demo()