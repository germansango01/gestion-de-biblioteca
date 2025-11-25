# Sistema de Gestión de Biblioteca con Tkinter, SQLite y Estadísticas

## Descripción
Este proyecto es un sistema de gestión de biblioteca desarrollado en Python con interfaz gráfica usando Tkinter y CustomTkinter. Permite gestionar libros, usuarios, préstamos y visualizar estadísticas avanzadas.  
Incluye funcionalidades de:

- Gestión de libros (añadir, borrar, listar).
- Gestión de usuarios (añadir, borrar, listar).
- Registro de préstamos y devoluciones.
- Historial completo de préstamos.
- Estadísticas con gráficos interactivos usando Matplotlib y Pandas:
  - Top 10 libros más prestados.
  - Autores con más préstamos.
  - Préstamos por mes (últimos 6 meses).
  - Últimos 10 préstamos.
  - Préstamos por categoría.

## Versión
`v1.0.0`

## Requisitos

- Python 3.8 o superior
- Librerías de Python:
  - `customtkinter`
  - `pandas`
  - `numpy`
  - `matplotlib`
  
Instalación de dependencias usando `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Uso

Ejecutar el archivo principal:

```bash
python main.py
```

La ventana principal mostrará varias pestañas:

- **Libros:** Gestiona la información de los libros (crear, borrar, listar).  
- **Usuarios:** Gestiona la información de los usuarios (crear, borrar, listar).  
- **Préstamos y Devoluciones:** Registrar nuevos préstamos y devoluciones de libros.  
- **Historial:** Muestra todos los préstamos, activos y devueltos.  
- **Estadísticas:** Botones para abrir ventanas modales con diferentes gráficas estadísticas.

### Funcionalidades principales

#### Libros
- **Añadir libro:** Abre un formulario modal para crear un libro con título, ISBN, autor y categoría.  
- **Borrar libro:** Elimina (soft delete) el libro seleccionado en el Treeview.  

#### Usuarios
- **Añadir usuario:** Abre un formulario modal para registrar usuario con username, email y password.  
- **Borrar usuario:** Elimina (soft delete) el usuario seleccionado en el Treeview.  

#### Préstamos
- **Nuevo préstamo:** Selecciona un usuario y un libro disponible mediante formulario modal.  
- **Devolver libro:** Registra la devolución de un libro seleccionado.

#### Historial
- Visualiza todos los préstamos con estado (activo o devuelto).

#### Estadísticas
- Botones para abrir gráficas en ventanas separadas:
  - Top 10 libros más prestados.
  - Autores con más préstamos.
  - Préstamos por mes (últimos 6 meses).
  - Últimos 10 préstamos.
  - Préstamos por categoría.

## Estructura de la Base de Datos

SQLite crea un archivo `library.db` con las tablas:

### users
| Campo       | Tipo    | Detalles                |
|------------|---------|------------------------|
| id         | INTEGER | Clave primaria autoincremental |
| username   | TEXT    | Obligatorio, único      |
| email      | TEXT    | Obligatorio, único      |
| password   | TEXT    | Obligatorio             |
| deleted_at | TEXT    | Nullable (soft delete)  |

### books
| Campo       | Tipo    | Detalles                |
|------------|---------|------------------------|
| id          | INTEGER | Clave primaria autoincremental |
| title       | TEXT    | Obligatorio            |
| isbn        | TEXT    | Obligatorio, único     |
| author      | TEXT    | Obligatorio            |
| category    | TEXT    | Obligatorio            |
| available   | INTEGER | 1 = disponible, 0 = prestado |
| deleted_at  | TEXT    | Nullable (soft delete) |

### loans
| Campo       | Tipo    | Detalles                |
|------------|---------|------------------------|
| id          | INTEGER | Clave primaria autoincremental |
| book_id     | INTEGER | FK a books(id)          |
| user_id     | INTEGER | FK a users(id)          |
| loan_date   | TEXT    | Obligatorio             |
| return_date | TEXT    | Nullable                |

## Explicación del Código

### Formularios
- **BookForm, UserForm, LoanForm:** Formularios modales para añadir libros, usuarios y préstamos.  
- **Cada formulario valida la entrada del usuario antes de guardar.**

### Views
- **BookView, UserView, LoanView, HistoryView, StatisticsView:** Pestañas principales que muestran los datos en Treeview y botones de acción.  

### Estadísticas
- Cada gráfica se abre en una ventana modal independiente con `Matplotlib` y `FigureCanvasTkAgg`.  
- Datos procesados con `Pandas` y cálculos con `NumPy`.  

### Base de Datos
- Clase `Database` maneja conexión y operaciones CRUD.  
- Uso de `with` y manejo de errores para seguridad y consistencia de datos.  

## Ejecución principal
- Se ejecuta `main.py`, que instancia la clase `App`.  
- Se crean las pestañas y se inicializa la base de datos si no existe.  
- La aplicación es totalmente interactiva mediante botones y formularios.

## Posibles mejoras
- Agregar búsqueda y filtrado de libros y usuarios.  
- Exportar reportes a PDF o Excel.  
- Mejorar los gráficos con más métricas y colores dinámicos.  
- Implementar login y roles de usuario.  

## Licencia
Este proyecto es libre para uso educativo y personal.
