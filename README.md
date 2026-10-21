# Sistema de Inventario y Ventas

## Descripción
Aplicación de consola desarrollada en Python para administrar productos y registrar ventas utilizando SQLite. El sistema permite controlar las existencias y mantener un historial de ventas.

## Tecnologías
- Python 3
- SQLite
- Módulo `sqlite3`

## Funcionalidades
- Registrar, consultar, actualizar y eliminar productos.
- Registrar ventas y descontar existencias.
- Consultar el historial de ventas mediante `JOIN`.
- Validar productos y cantidades disponibles.
- Utilizar `commit()` y `rollback()` para garantizar la integridad de las transacciones.

## Requisitos
Tener Python 3 instalado.

## Cómo ejecutar
1. Descargar o clonar este repositorio.
2. Abrir una terminal en la carpeta del proyecto.
3. Ejecutar:

```bash
python main.py
```

La base de datos y las tablas se crean automáticamente al iniciar el programa.

## Estructura del proyecto
- `main.py`: menú, operaciones CRUD y lógica de ventas.
- `database.py`: conexión y configuración de SQLite.
- `docs/`: documentación, modelo de datos, arquitectura y evidencias.
- `inventario.db`: base de datos creada al ejecutar el programa, si aplica.

## Transacciones
Cada venta se registra dentro de una transacción. Primero se valida el producto y el stock, después se registra la venta y se actualiza el inventario. Si ocurre un error, `rollback()` cancela los cambios; si todo funciona correctamente, `commit()` los confirma.

## Autor
Santiago Mosquera
