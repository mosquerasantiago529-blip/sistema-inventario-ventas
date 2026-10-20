Modelo de datos — Sistema de inventario y ventas
1. Descripción

La base de datos del sistema se llama inventario.db y utiliza SQLite para almacenar la información de los productos y las ventas.

Está compuesta por dos tablas principales: productos y ventas.

2. Tabla productos

Almacena los productos disponibles en la tienda.

Campo	Tipo de dato	Restricciones	Descripción
id_producto	INTEGER	PRIMARY KEY, AUTOINCREMENT	Identificador único
nombre	TEXT	NOT NULL	Nombre del producto
precio	REAL	NOT NULL, CHECK (precio >= 0)	Precio del producto
cantidad	INTEGER	NOT NULL, CHECK (cantidad >= 0)	Unidades disponibles
3. Tabla ventas

Almacena las ventas realizadas.

Campo	Tipo de dato	Restricciones	Descripción
id_venta	INTEGER	PRIMARY KEY, AUTOINCREMENT	Identificador de la venta
id_producto	INTEGER	FOREIGN KEY, NOT NULL	Producto vendido
cantidad	INTEGER	NOT NULL, CHECK (cantidad > 0)	Unidades vendidas
precio_unitario	REAL	NOT NULL, CHECK (precio_unitario >= 0)	Precio al realizar la venta
fecha	TEXT	NOT NULL	Fecha y hora del registro
4. Diagrama de relación
+-------------------------+
|        PRODUCTOS        |
+-------------------------+
| PK id_producto          |
|    nombre               |
|    precio               |
|    cantidad             |
+-------------------------+
             |
             | 1
             |
             | N
+-------------------------+
|          VENTAS         |
+-------------------------+
| PK id_venta             |
| FK id_producto          |
|    cantidad             |
|    precio_unitario       |
|    fecha                |
+-------------------------+


La relación es de uno a muchos (1:N). Un producto puede tener varias ventas registradas.

La clave foránea ventas.id_producto referencia productos.id_producto.

5. Integridad referencial

La relación utiliza una clave foránea para impedir que se registren ventas de productos inexistentes.

Además, se establece ON DELETE RESTRICT, que impide eliminar un producto que tenga ventas relacionadas. Esto permite conservar el historial de ventas.

La conexión de SQLite activa las claves foráneas mediante:

PRAGMA foreign_keys = ON;

6. Consultas parametrizadas

El programa utiliza consultas parametrizadas para insertar, consultar, actualizar y eliminar registros.

Ejemplo:

INSERT INTO productos (nombre, precio, cantidad)
VALUES (?, ?, ?);


Los signos ? se sustituyen por los valores proporcionados por Python, evitando concatenar directamente los datos del usuario en la consulta.

7. Consulta del historial

Para mostrar el nombre del producto en cada venta se utiliza INNER JOIN.

SELECT
    v.id_venta,
    p.nombre,
    v.cantidad,
    v.precio_unit