
import sqlite3
from datetime import datetime

DB_NAME = "inventario.db"


# CONEXION Y CREACION DE TABLAS
def conectar():
    conexion = sqlite3.connect(DB_NAME)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    conexion = conectar()
    try:
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
                precio REAL NOT NULL CHECK(precio >= 0)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER NOT NULL,
                cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                precio_unitario REAL NOT NULL,
                total REAL NOT NULL,
                fecha TEXT NOT NULL,
                FOREIGN KEY (id_producto)
                    REFERENCES productos(id_producto)
                    ON DELETE RESTRICT
            )
        """)

        conexion.commit()

    except sqlite3.Error as error:
        conexion.rollback()
        print(f"Error al crear las tablas: {error}")

    finally:
        conexion.close()


# VALIDACION DE DATOS
def leer_entero(mensaje, minimo=None):
    while True:
        try:
            valor = int(input(mensaje))

            if minimo is not None and valor < minimo:
                print(f"El valor debe ser minimo {minimo}.")
                continue

            return valor

        except ValueError:
            print("Error: debes ingresar un numero entero.")


def leer_decimal(mensaje, minimo=0):
    while True:
        try:
            valor = float(input(mensaje).replace(",", "."))

            if valor < minimo:
                print(f"El valor debe ser minimo {minimo}.")
                continue

            return valor

        except ValueError:
            print("Error: debes ingresar un numero valido.")


def leer_texto(mensaje):
    while True:
        valor = input(mensaje).strip()

        if valor:
            return valor

        print("El texto no puede estar vacio.")


# 1. REGISTRAR PRODUCTO
def registrar_producto():
    nombre = leer_texto("Nombre del producto: ")
    cantidad = leer_entero("Cantidad inicial: ", minimo=0)
    precio = leer_decimal("Precio unitario: ")

    conexion = conectar()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, cantidad, precio)
            VALUES (?, ?, ?)
        """, (nombre, cantidad, precio))

        conexion.commit()
        print("Producto registrado correctamente.")

    except sqlite3.Error as error:
        conexion.rollback()
        print(f"Error al registrar el producto: {error}")

    finally:
        conexion.close()


# 2. CONSULTAR PRODUCTOS
def consultar_productos():
    conexion = conectar()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_producto, nombre, cantidad, precio
            FROM productos
            ORDER BY id_producto
        """)

        productos = cursor.fetchall()

        if not productos:
            print("No hay productos registrados.")
            return

        print("\n===== INVENTARIO DE PRODUCTOS =====")

        for producto in productos:
            print(
                f"ID: {producto[0]} | "
                f"Nombre: {producto[1]} | "
                f"Stock: {producto[2]} | "
                f"Precio: ${producto[3]:.2f}"
            )

    except sqlite3.Error as error:
        print(f"Error al consultar los productos: {error}")

    finally:
        conexion.close()


# 3. ACTUALIZAR PRODUCTO
def actualizar_producto():
    consultar_productos()

    id_producto = leer_entero(
        "ID del producto que deseas actualizar: ", minimo=1
    )

    nombre = leer_texto("Nuevo nombre: ")
    cantidad = leer_entero("Nueva cantidad: ", minimo=0)
    precio = leer_decimal("Nuevo precio: ")

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE productos
            SET nombre = ?, cantidad = ?, precio = ?
            WHERE id_producto = ?
        """, (nombre, cantidad, precio, id_producto))

        if cursor.rowcount == 0:
            print("El producto no existe.")
            conexion.rollback()
            return

        conexion.commit()
        print("Producto actualizado correctamente.")

    except sqlite3.Error as error:
        conexion.rollback()
        print(f"Error al actualizar el producto: {error}")

    finally:
        conexion.close()


# 4. ELIMINAR PRODUCTO
def eliminar_producto():
    consultar_productos()

    id_producto = leer_entero(
        "ID del producto que deseas eliminar: ", minimo=1
    )

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            DELETE FROM productos
            WHERE id_producto = ?
        """, (id_producto,))

        if cursor.rowcount == 0:
            print("El producto no existe.")
            conexion.rollback()
            return

        conexion.commit()
        print("Producto eliminado correctamente.")

    except sqlite3.IntegrityError:
        conexion.rollback()
        print(
            "No se puede eliminar: el producto tiene ventas "
            "registradas."
        )

    except sqlite3.Error as error:
        conexion.rollback()
        print(f"Error al eliminar el producto: {error}")

    finally:
        conexion.close()


# PROCESAR VENTA CON TRANSACCION
def procesar_venta(id_producto, cantidad, simular_error=False):
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        # Consultar el producto y su stock.
        cursor.execute("""
            SELECT nombre, cantidad, precio
            FROM productos
            WHERE id_producto = ?
        """, (id_producto,))

        producto = cursor.fetchone()

        if producto is None:
            print("El producto no existe.")
            return False

        nombre, stock, precio = producto

        if cantidad <= 0:
            print("La cantidad debe ser mayor que cero.")
            return False

        if cantidad > stock:
            print(f"Stock insuficiente. Existencias: {stock}")
            return False

        total = round(precio * cantidad, 2)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Iniciar una transaccion.
        cursor.execute("BEGIN")

        # Descontar existencias.
        cursor.execute("""
            UPDATE productos
            SET cantidad = cantidad - ?
            WHERE id_producto = ?
        """, (cantidad, id_producto))

        # Registrar la venta.
        cursor.execute("""
            INSERT INTO ventas (
                id_producto, cantidad, precio_unitario,
                total, fecha
            )
            VALUES (?, ?, ?, ?, ?)
        """, (id_producto, cantidad, precio, total, fecha))

        # Provocar un error controlado para probar ROLLBACK.
        if simular_error:
            raise RuntimeError("Error simulado para probar rollback")

        # Confirmar todos los cambios.
        conexion.commit()

        print("\nVenta registrada correctamente.")
        print(f"Producto: {nombre}")
        print(f"Cantidad vendida: {cantidad}")
        print(f"Precio unitario: ${precio:.2f}")
        print(f"Total de la venta: ${total:.2f}")

        return True

    except (sqlite3.Error, RuntimeError) as error:
        conexion.rollback()
        print(f"Error al procesar la venta: {error}")
        print("ROLLBACK ejecutado: los cambios fueron cancelados.")
        return False

    finally:
        conexion.close()


# 5. REGISTRAR VENTA
def registrar_venta():
    consultar_productos()

    id_producto = leer_entero("ID del producto: ", minimo=1)
    cantidad = leer_entero("Cantidad que deseas vender: ", minimo=1)

    procesar_venta(id_producto, cantidad)


# 6. HISTORIAL DE VENTAS
def historial_ventas():
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                ventas.id_venta,
                productos.nombre,
                ventas.cantidad,
                ventas.precio_unitario,
                ventas.total,
                ventas.fecha
            FROM ventas
            INNER JOIN productos
                ON ventas.id_producto = productos.id_producto
            ORDER BY ventas.id_venta DESC
        """)

        ventas = cursor.fetchall()

        if not ventas:
            print("No hay ventas registradas.")
            return

        print("\n===== HISTORIAL DE VENTAS =====")

        for venta in ventas:
            print(
                f"Venta #{venta[0]} | Producto: {venta[1]} | "
                f"Cantidad: {venta[2]} | "
                f"Precio: ${venta[3]:.2f} | "
                f"Total: ${venta[4]:.2f} | "
                f"Fecha: {venta[5]}"
            )

    except sqlite3.Error as error:
        print(f"Error al consultar las ventas: {error}")

    finally:
        conexion.close()


# 7. PRUEBA CONTROLADA DE ROLLBACK
def probar_rollback():
    consultar_productos()

    id_producto = leer_entero(
        "ID del producto para la prueba: ", minimo=1
    )

    cantidad = leer_entero(
        "Cantidad que se intentara vender: ", minimo=1
    )

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT nombre, cantidad
            FROM productos
            WHERE id_producto = ?
        """, (id_producto,))

        producto = cursor.fetchone()

        if producto is None:
            print("El producto no existe.")
            return

        nombre, stock_antes = producto

        cursor.execute("""
            SELECT COUNT(*)
            FROM ventas
            WHERE id_producto = ?
        """, (id_producto,))

        ventas_antes = cursor.fetchone()[0]

    except sqlite3.Error as error:
        print(f"Error al preparar la prueba: {error}")
        return

    finally:
        conexion.close()

    print("\n--- INICIO DE PRUEBA DE ROLLBACK ---")

    procesar_venta(
        id_producto,
        cantidad,
        simular_error=True
    )

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT cantidad
            FROM productos
            WHERE id_producto = ?
        """, (id_producto,))

        fila = cursor.fetchone()
        stock_despues = fila[0] if fila else None

        cursor.execute("""
            SELECT COUNT(*)
            FROM ventas
            WHERE id_producto = ?
        """, (id_producto,))

        ventas_despues = cursor.fetchone()[0]

        print("\n--- RESULTADO DE LA PRUEBA ---")
        print(f"Producto: {nombre}")
        print(f"Stock antes: {stock_antes}")
        print(f"Stock despues: {stock_despues}")
        print(f"Ventas antes: {ventas_antes}")
        print(f"Ventas despues: {ventas_despues}")

        if (
            stock_antes == stock_despues
            and ventas_antes == ventas_despues
        ):
            print(
                "PRUEBA CORRECTA: rollback mantuvo "
                "los datos intactos."
            )
        else:
            print(
                "ATENCION: los datos cambiaron; "
                "revisa la transaccion."
            )

    except sqlite3.Error as error:
        print(f"Error al verificar la prueba: {error}")

    finally:
        conexion.close()


# MENU PRINCIPAL
def menu():
    while True:
        print("\n===== SISTEMA DE INVENTARIO Y VENTAS =====")
        print("1. Registrar producto")
        print("2. Consultar productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Registrar venta")
        print("6. Historial de ventas")
        print("7. Probar rollback (error controlado)")
        print("0. Salir")

        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            consultar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            registrar_venta()
        elif opcion == "6":
            historial_ventas()
        elif opcion == "7":
            probar_rollback()
        elif opcion == "0":
            print("Programa finalizado.")
            break
        else:
            print("Opcion no valida. Intenta nuevamente.")


# INICIO DEL PROGRAMA
if __name__ == "__main__":
    crear_tablas()
    menu()
