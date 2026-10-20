Transacciones — Sistema de inventario y ventas
1. ¿Qué es una transacción?

Una transacción es un conjunto de operaciones sobre una base de datos que deben ejecutarse como una unidad. En este sistema, registrar una venta y descontar las unidades del inventario son operaciones relacionadas que deben confirmarse juntas.

2. Proceso para registrar una venta

El procedimiento es el siguiente:

Recibir el identificador del producto y la cantidad que se desea vender.
Verificar que el producto exista.
Comprobar que haya suficientes unidades disponibles.
Iniciar una transacción.
Insertar el registro en la tabla ventas.
Descontar las unidades vendidas de la tabla productos.
Ejecutar commit() para confirmar las dos operaciones.

Si ocurre un error antes de confirmar la transacción, el programa ejecuta rollback() para cancelar los cambios pendientes.

3. Uso de commit()

El método commit() confirma los cambios realizados en la transacción.

En este sistema, se ejecuta después de insertar la venta y actualizar el inventario.

De esta forma, ambas operaciones quedan guardadas en la base de datos.

4. Uso de rollback()

El método rollback() cancela los cambios pendientes de la transacción actual.

Por ejemplo, si se registra una venta, pero ocurre un error antes de descontar las unidades del inventario, rollback() permite deshacer el registro de la venta.

Así se evita que el historial muestre una venta que no se refleje correctamente en las existencias.

5. Ejemplo de funcionamiento

Estado inicial:

Producto: Memoria RAM.
Existencias: 10 unidades.
Ventas nuevas: 0.

Operación solicitada:

Vender 3 unidades.

Si todo funciona correctamente:

La tabla ventas recibe un nuevo registro.
El inventario pasa de 10 a 7 unidades.
commit() confirma los cambios.

Si ocurre un error después de insertar la venta y antes de actualizar el inventario:

Se ejecuta rollback().
La venta nueva no queda registrada.
El inventario permanece en 10 unidades.
6. Importancia de las validaciones

Antes de registrar una venta, el sistema debe comprobar que el producto exista y que la cantidad solicitada sea un entero positivo y no supere las existencias disponibles.

Estas validaciones previenen operaciones inválidas y ayudan a mantener la consistencia de la información.

7. Prueba de error control