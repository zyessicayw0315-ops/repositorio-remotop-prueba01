import json
from datetime import datetime
from pathlib import Path

# -----------------------------
# Archivos JSON
# -----------------------------
RUTA_CATALOGO = Path(__file__).with_name("catalogo_productos.json")
RUTA_VENTAS = Path(__file__).with_name("ventas.json")


# -----------------------------
# Catálogo inicial (10 productos)
# -----------------------------
def crear_catalogo_inicial():
    catalogo = [
        {"id": 1, "nombre": "Cama Queen Size", "categoria": "Cama", "marca": "DormiLux", "tamaño": "Queen", "precio": 3500, "stock": 5},
        {"id": 2, "nombre": "Cama King Size", "categoria": "Cama", "marca": "Matrimoon", "tamaño": "King", "precio": 4200, "stock": 4},
        {"id": 3, "nombre": "Cama Individual", "categoria": "Cama", "marca": "SleepEasy", "tamaño": "Individual", "precio": 2200, "stock": 7},
        {"id": 4, "nombre": "Colchón Memory Foam", "categoria": "Colchón", "marca": "RestFlex", "tamaño": "Queen", "precio": 1800, "stock": 8},
        {"id": 5, "nombre": "Colchón Ortopédico", "categoria": "Colchón", "marca": "SpineCare", "tamaño": "King", "precio": 2400, "stock": 6},
        {"id": 6, "nombre": "Colchón de Muelles", "categoria": "Colchón", "marca": "SleepWell", "tamaño": "Matrimonial", "precio": 1500, "stock": 9},
        {"id": 7, "nombre": "Mesa de Noche", "categoria": "Mesa de noche", "marca": "HomeLine", "tamaño": "Mediana", "precio": 650, "stock": 10},
        {"id": 8, "nombre": "Mesa de Noche con Cajón", "categoria": "Mesa de noche", "marca": "WoodStyle", "tamaño": "Grande", "precio": 820, "stock": 8},
        {"id": 9, "nombre": "Tocador de Madera", "categoria": "Tocador", "marca": "Elegance", "tamaño": "Mediano", "precio": 1100, "stock": 5},
        {"id": 10, "nombre": "Tocador Moderno", "categoria": "Tocador", "marca": "LuxHome", "tamaño": "Grande", "precio": 1350, "stock": 4},
    ]

    with RUTA_CATALOGO.open("w", encoding="utf-8") as archivo:
        json.dump(catalogo, archivo, ensure_ascii=False, indent=4)

    print("Catálogo inicial creado.")


def cargar_catalogo():
    # Si no existe el archivo, se crea automáticamente
    if not RUTA_CATALOGO.exists():
        crear_catalogo_inicial()

    with RUTA_CATALOGO.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_catalogo(catalogo):
    with RUTA_CATALOGO.open("w", encoding="utf-8") as archivo:
        json.dump(catalogo, archivo, ensure_ascii=False, indent=4)


def cargar_ventas():
    if not RUTA_VENTAS.exists():
        return []

    with RUTA_VENTAS.open("r", encoding="utf-8") as archivo:
        try:
            datos = json.load(archivo)
            if isinstance(datos, list):
                return datos
            return []
        except json.JSONDecodeError:
            return []


def guardar_ventas(ventas):
    with RUTA_VENTAS.open("w", encoding="utf-8") as archivo:
        json.dump(ventas, archivo, ensure_ascii=False, indent=4)


# -----------------------------
# Mostrar catálogo
# -----------------------------
def mostrar_catalogo():
    catalogo = cargar_catalogo()

    print("\n====================================")
    print("         CATÁLOGO DE PRODUCTOS")
    print("====================================")
    print("ID | Nombre                     | Categoria       | Marca       | Tamaño    | Precio     | Stock")
    print("---------------------------------------------------------------------------------------------")

    for producto in catalogo:
        print(
            f"{producto['id']:>2} | {producto['nombre']:<25} | {producto['categoria']:<15} | "
            f"{producto['marca']:<12} | {producto['tamaño']:<10} | "
            f"${producto['precio']:>8,.2f} | {producto['stock']:>5}"
        )

    print("---------------------------------------------------------------------------------------------")


# -----------------------------
# Datos del cliente
# -----------------------------
def pedir_datos_cliente():
    print("\n====================================")
    print("        DATOS DEL CLIENTE")
    print("====================================")

    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()

    edad_valida = False
    while not edad_valida:
        edad = input("Edad: ").strip()
        if edad.isdigit() and int(edad) > 0:
            edad_valida = True
        else:
            print("La edad debe ser un número válido mayor que 0.")

    return {
        "nombre": nombre,
        "apellido": apellido,
        "edad": int(edad)
    }


# -----------------------------
# Selección de productos
# -----------------------------
def seleccionar_productos():
    catalogo = cargar_catalogo()
    carrito = []

    while True:
        print("\nIngrese el ID del producto que desea comprar.")
        print("Escriba 0 para terminar.")
        opcion = input("ID del producto: ").strip()

        if opcion == "0":
            break

        if not opcion.isdigit():
            print("Debe ingresar un número válido.")
            continue

        id_producto = int(opcion)

        producto = None
        for item in catalogo:
            if item["id"] == id_producto:
                producto = item
                break

        if producto is None:
            print("Ese producto no existe en el catálogo.")
            continue

        if producto["stock"] <= 0:
            print("No hay stock disponible para este producto.")
            continue

        cantidad = input(f"Cantidad de '{producto['nombre']}': ").strip()

        while not cantidad.isdigit() or int(cantidad) <= 0:
            print("La cantidad debe ser un número entero mayor a 0.")
            cantidad = input(f"Cantidad de '{producto['nombre']}': ").strip()

        cantidad = int(cantidad)

        if cantidad > producto["stock"]:
            print(f"Solo quedan {producto['stock']} unidades en stock.")
            continue

        # Descontamos el stock solo en la compra actual
        producto["stock"] -= cantidad

        subtotal_item = producto["precio"] * cantidad

        carrito.append({
            "id": producto["id"],
            "nombre": producto["nombre"],
            "categoria": producto["categoria"],
            "marca": producto["marca"],
            "tamaño": producto["tamaño"],
            "precio_unitario": producto["precio"],
            "cantidad": cantidad,
            "subtotal": subtotal_item
        })

        print(f"Se agregaron {cantidad} unidad(es) de {producto['nombre']} al carrito.")

    # Guardamos el catálogo actualizado después de haber restado stock
    guardar_catalogo(catalogo)

    return carrito


# -----------------------------
# Cálculo del total
# -----------------------------
def calcular_total(carrito):
    total = 0
    for item in carrito:
        total += item["subtotal"]
    return total


# -----------------------------
# Factura
# -----------------------------
def mostrar_factura(cliente, carrito, total):
    print("\n====================================")
    print("             FACTURA DE COMPRA")
    print("====================================")
    print(f"Cliente: {cliente['nombre']} {cliente['apellido']}")
    print(f"Edad: {cliente['edad']} años")
    print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("------------------------------------")
    print("Producto                     | Cantidad | Precio U. | Subtotal")
    print("------------------------------------")

    for item in carrito:
        print(
            f"{item['nombre']:<27} | {item['cantidad']:>7} | "
            f"${item['precio_unitario']:>9,.2f} | ${item['subtotal']:>10,.2f}"
        )

    print("------------------------------------")
    print(f"TOTAL: ${total:>18,.2f}")
    print("====================================")


# -----------------------------
# Guardar venta en JSON
# -----------------------------
def guardar_venta(cliente, carrito, total):
    ventas = cargar_ventas()

    venta = {
        "cliente": {
            "nombre": cliente["nombre"],
            "apellido": cliente["apellido"],
            "edad": cliente["edad"]
        },
        "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "articulos": carrito,
        "total": total
    }

    ventas.append(venta)
    guardar_ventas(ventas)


# -----------------------------
# Métricas del sistema
# -----------------------------
def mostrar_estadisticas():
    ventas = cargar_ventas()

    print("\n====================================")
    print("       ESTADÍSTICAS DE VENTAS")
    print("====================================")

    if not ventas:
        print("Aún no hay ventas registradas.")
        return

    cantidad_ventas = len(ventas)
    ingresos_acumulados = 0
    productos_vendidos = 0
    conteo_productos = {}

    for venta in ventas:
        ingresos_acumulados += venta["total"]

        for articulo in venta["articulos"]:
            productos_vendidos += articulo["cantidad"]
            nombre = articulo["nombre"]
            if nombre in conteo_productos:
                conteo_productos[nombre] += articulo["cantidad"]
            else:
                conteo_productos[nombre] = articulo["cantidad"]

    producto_mas_vendido = ""
    mayor_cantidad = 0

    for nombre, cantidad in conteo_productos.items():
        if cantidad > mayor_cantidad:
            mayor_cantidad = cantidad
            producto_mas_vendido = nombre

    print(f"Cantidad de ventas realizadas: {cantidad_ventas}")
    print(f"Ingresos acumulados: ${ingresos_acumulados:,.2f}")
    print(f"Productos vendidos: {productos_vendidos}")
    print(f"Producto con mayor cantidad de ventas: {producto_mas_vendido}")

    print("====================================")


# -----------------------------
# Menú principal
# -----------------------------
def menu_principal():
    while True:
        print("\n====================================")
        print("   Muebleria Belleza y Glamour - Menú Principal")
        print("====================================")
        print("1. Ver catálogo")
        print("2. Realizar compra")
        print("3. Ver estadísticas")
        print("4. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            mostrar_catalogo()

        elif opcion == "2":
            cliente = pedir_datos_cliente()
            mostrar_catalogo()
            carrito = seleccionar_productos()

            if not carrito:
                print("No agregaste ningún producto. La compra se canceló.")
                continue

            total = calcular_total(carrito)
            mostrar_factura(cliente, carrito, total)
            guardar_venta(cliente, carrito, total)
            print("Compra registrada correctamente.")

        elif opcion == "3":
            mostrar_estadisticas()

        elif opcion == "4":
            print("Gracias por visitar nuestra tienda.")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


# -----------------------------
# Inicio del programa
# -----------------------------
def main():
    print("Bienvenido a Muebleria Belleza y Glamour.")
    menu_principal()


if __name__ == "__main__":
    main()