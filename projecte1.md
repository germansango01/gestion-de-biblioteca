# **Ficha Proyecto 1 – Gestión de Biblioteca**

## **Objetivo**

Crear una aplicación para gestionar libros, autores y préstamos en una biblioteca.

## **Instrucciones por partes**

### **Parte 1 – Fundamentos (hasta 75%)**

* **Clases:** `Libro`, `Autor`, `Prestamo`
* **Interfaz Tkinter:** añadir/modificar libros y autores, registrar préstamos, mostrar lista de libros disponibles
* **Persistencia:** CSV o SQLite para libros, autores y préstamos
* **Validación:** campos obligatorios, fechas correctas, ISBN válido, evitar duplicados

### **Parte 2 – Datos y estadísticas (hasta 90%)**

* **Numpy:** estadísticas sobre libros prestados (media de préstamos por mes, máximo, mínimo)
* **Pandas:** DataFrame de libros por categoría, autores con más préstamos, filtrado por disponibilidad
* **Matplotlib:** gráficas de libros más prestados, préstamos por mes

### **Parte 3 – Funcionalidades avanzadas (hasta 100%)**

* Exportación a PDF con listados de libros o préstamos
* **Gestión de usuarios con contraseñas seguras:**
  * Los usuarios que acceden al sistema deben tener contraseña.
  * Las contraseñas deben almacenarse **mediante hash seguro** (por ejemplo, usando `hashlib` o `bcrypt`).
  * Al iniciar sesión, la contraseña introducida debe compararse con el hash almacenado para permitir el acceso.
* Posible importación/exportación de CSV

### **Entrega final**

* Código completo
* Archivos de datos o base de datos
* README.md siguiendo el modelo presentado
* PROMPTS.md con las consultas a IA y modelo usado
* Capturas de pantalla opcionales

---


### 📄 Créditos

![1757054093039](img/1756889537400.png)

Última revisión: Noviembre 2025

Este dosier forma parte del curso "Algoritmia y Programación con Python", por Manu Plaza Salas para CIFO Barcelona La Violeta.

Esta obra está bajo una [licencia de Creative Commons Reconeixement-NoComercial-CompartirIgual 4.0 Internacional](http://creativecommons.org/licenses/by-nc-sa/4.0/).
