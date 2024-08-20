import os
import platform
from productos import ProductoElectronico, ProductoAlimenticio, GestionProductos

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo'''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear') # Para Linux/Unix/MacOs

def mostrar_menu():
    print("========== Menú de Gestión de Productos ==========")
    print('1. Agregar Producto Electrónico')
    print('2. Agregar Producto Alimenticio')
    print('3. Buscar Producto por Código')
    print('4. Actualizar Producto')
    print('5. Eliminar Producto por Código')
    print('6. Mostrar Todos los Productos')
    print('7. Salir')
    print('==================================================')

def agregar_producto(gestion, tipo_producto):
    try:
        codigo = input('Ingrese código del producto: ')
        nombre = input('Ingrese nombre del producto: ')
        precio = float(input('Ingrese precio del producto: '))
        cantidad = int(input('Ingrese cantidad en stock: '))

        if tipo_producto == '1':
            garantia = int(input('Ingrese garantía en años: '))
            producto = ProductoElectronico(codigo, nombre, precio, cantidad, garantia)
        elif tipo_producto == '2':
            fecha_expiracion = input('Ingrese fecha de expiración (AAAA-MM-DD): ')
            producto = ProductoAlimenticio(codigo, nombre, precio, cantidad, fecha_expiracion)
        else:
            print('Opción inválida')
            return

        gestion.crear_producto(producto)
        input('Presione enter para continuar...')

    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_producto_por_codigo(gestion):
    codigo = input('Ingrese el código del producto a buscar: ')
    gestion.leer_producto(codigo)
    input('Presione enter para continuar...')

def actualizar_producto(gestion):
    codigo = input('Ingrese el código del producto para actualizar: ')
    precio = float(input('Ingrese el nuevo precio del producto: '))
    cantidad = int(input('Ingrese la nueva cantidad en stock: '))
    gestion.actualizar_producto(codigo, precio, cantidad)
    input('Presione enter para continuar...')

def eliminar_producto_por_codigo(gestion):
    codigo = input('Ingrese el código del producto a eliminar: ')
    gestion.eliminar_producto(codigo)
    input('Presione enter para continuar...')

def mostrar_todos_los_productos(gestion):
    print('=============== Listado completo de los Productos ==============')
    for producto in gestion.leer_datos().values():
        if 'garantia' in producto:
            print(f"Producto Electrónico: {producto['nombre']} - con Garantía de: {producto['garantia']} años")
        elif 'fecha_expiracion' in producto:
            print(f"Producto Alimenticio: {producto['nombre']} - Fecha de Expiración: {producto['fecha_expiracion']}")
        else:
            print(f"{producto['nombre']} - Precio: {producto['precio']} - Cantidad: {producto['cantidad']}")
    print('=================================================================')
    input('Presione enter para continuar...')

if __name__ == "__main__":
    archivo_productos = 'productos_db.json'
    gestion = GestionProductos(archivo_productos)

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion == '1' or opcion == '2':
            agregar_producto(gestion, opcion)
        
        elif opcion == '3':
            buscar_producto_por_codigo(gestion)

        elif opcion == '4':
            actualizar_producto(gestion)

        elif opcion == '5':
            eliminar_producto_por_codigo(gestion)

        elif opcion == '6':
            mostrar_todos_los_productos(gestion)

        elif opcion == '7':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida. Por favor, seleccione una opción válida (1-7)')