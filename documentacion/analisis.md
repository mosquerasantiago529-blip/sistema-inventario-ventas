Análisis del sistema de inventario y ventas
1. Descripción del problema

Una tienda de componentes electrónicos necesita una aplicación de consola que permita administrar sus productos y registrar las ventas realizadas.

El problema principal consiste en evitar inconsistencias entre las ventas registradas y las cantidades disponibles en el inventario. Para solucionarlo, se utilizará Python junto con SQLite, que permitirá almacenar y consultar los datos de forma persistente.

2. Objetivo general

Desarrollar una aplicación de consola en Python que permita gestionar productos, controlar las existencias y registrar ventas de forma segura mediante operaciones CRUD y transacciones SQL.

3. Objetivos específicos
Registrar productos con nombre, precio y cantidad disponible.
Consultar todos los productos almacenados.
Actualizar el precio y la cantidad de los productos.
Eliminar productos respetando las relaciones de la base de datos.
Registrar ventas y descontar las unidades vendidas del inventario.
Consultar el historial de ventas utilizando JOIN.
Utilizar commit() y rollback() para mantener la integridad de los datos.
4. Entidades principales
Producto

Representa los componentes electrónicos disponibles en la tienda.

Atributos:

id_producto: identificador único del producto.
nombre: nombre del producto.
precio: precio de venta.
cantidad: unidades disponibles.
Venta

Representa una operación de venta realizada.

Atributos:

id_venta: identificador único de la venta.
id_producto: referencia al producto vendido.
cantidad: unidades vendidas.
precio_unitario: precio del producto al momento de la venta.
fecha: fecha y hora del registro.
5. Relación entre las entidades

La relación entre Producto y Venta es de uno a muchos (1:N). Un producto puede aparecer en múltiples ventas, pero cada registro de venta corresponde a un producto.

La relación se implementa mediante la clave foránea id_producto de la tabla ventas, que referencia a id_producto de la tabla productos.

6. Arquitectura del sistema

El sistema se organiza en tres componentes:

Usuario: interactúa con el menú de la aplicación e introduce los datos.
Python: procesa las opciones, valida los datos y ejecuta las operaciones CRUD y la lógica de ventas.
SQLite: almacena los productos y las ventas, y garantiza las restricciones definidas en las tablas.
7. Seguridad e integridad de los datos

Las consultas SQL utilizan parámetros (?) para separar las instrucciones SQL de los valores introducidos por el usuario.

Al registrar una venta, el sistema comprueba que el producto exista y que haya suficientes unidades disponibles. La inserción de la venta y la actualización del inventario deben confirmarse dentro de una misma transacción.

Si ocurre un error, se utiliza rollback() para cancelar los cambios pendientes y evitar inconsistencias.

8. Tecnologías utilizadas
Python: lenguaje de programación.
sqlite3: módulo de Python para trabajar con SQLite.
SQLite: sistema de gestión de base de datos.
Visual Studio Code: editor de código.
GitHub: plataforma para publicar y entregar el proyecto.