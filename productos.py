'''
Desafío 1: Sistema de Gestión de Productos

Objetivo: Desarrollar un sistema para manejar productos en un inventario.

Requisitos:

    # Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
    # Definir al menos 2 clases derivadas para diferentes categorías de productos (por ejemplo, ProductoElectronico,
    ProductoAlimenticio) con atributos y métodos específicos.
    # Implementar operaciones CRUD para gestionar productos del inventario.
    # Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
    # Persistir los datos en archivo JSON.
'''


import json

import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


class Producto:
    def __init__(self, codigo, nombre, precio, cantidad):
        self.__codigo = self.validar_codigo(codigo)
        self.__nombre = nombre
        self.__precio = self.validar_precio(precio)
        self.__cantidad = self.validar_cantidad(cantidad)

    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def cantidad(self):
        return self.__cantidad

    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)

    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        self.__cantidad = self.validar_cantidad(nueva_cantidad)

    def validar_codigo(self, codigo):
        if not isinstance(codigo, str) or len(codigo) < 1:
            raise ValueError("El código del producto debe ser una cadena no vacía.")
        return codigo

    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num <= 0:
                raise ValueError("El precio debe ser un número positivo.")
            return precio_num
        except ValueError:
            raise ValueError("El precio debe ser un número válido.")

    def validar_cantidad(self, cantidad):
        try:
            cantidad_num = int(cantidad)
            if cantidad_num < 0:
                raise ValueError("La cantidad no puede ser negativa.")
            return cantidad_num
        except ValueError:
            raise ValueError("La cantidad debe ser un número entero válido.")

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad
        }

    def __str__(self):
        return f"{self.nombre} (Código: {self.codigo}) - Precio: {self.precio} - Cantidad: {self.cantidad}"

class ProductoElectronico(Producto):
    def __init__(self, codigo, nombre, precio, cantidad, garantia):
        super().__init__(codigo, nombre, precio, cantidad)
        self.__garantia = garantia

    @property
    def garantia(self):
        return self.__garantia
    
    @garantia.setter
    def garantia(self, nueva_garantia):
        self.__garantia = nueva_garantia

    def to_dict(self):
        data = super().to_dict()
        data["garantia"] = self.garantia
        return data

    def __str__(self):
        return f"{super().__str__()} - Garantía: {self.garantia} años"

class ProductoAlimenticio(Producto):
    def __init__(self, codigo, nombre, precio, cantidad, fecha_expiracion):
        super().__init__(codigo, nombre, precio, cantidad)
        self.__fecha_expiracion = fecha_expiracion

    @property
    def fecha_expiracion(self):
        return self.__fecha_expiracion
    
    @property
    def fecha_expiracion(self):
        return self.__fecha_expiracion

    def to_dict(self):
        data = super().to_dict()
        data["fecha_expiracion"] = self.fecha_expiracion
        return data

    def __str__(self):
        return f"{super().__str__()} - Fecha de Expiración: {self.fecha_expiracion}"

class GestionProductos:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            logging.error(f"El archivo {self.archivo} no fue encontrado")
            return {}
        except json.JSONDecodeError:
            logging.error(f"El archivo {self.archivo} no contiene un JSON válido")
            raise ValueError(f"El archivo {self.archivo} no contiene un JSON válido")
        except Exception as e:
            raise Exception(f'Error al leer datos del archivo: {e}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as e:
            logging.error(f"Error al intentar guardar los datos en {self.archivo}: {e}")
            raise IOError(f"No se pudo guardar los datos en {self.archivo}, verifique el archivo")
            #print(f'Error al intentar guardar los datos en {self.archivo}: {e}')
        except TypeError as e:
            logging.error(f"Datos inválidos para serializar en JSON: {e}")
        except Exception as e:
            logging.error(f"Error inesperado al guardar los datos en {self.archivo}: {e}")
            raise RuntimeError(f"Error inesperado: {e}")
            #print(f'Error inesperado: {e}')

    def crear_producto(self, producto):
        try:
            datos = self.leer_datos()
            codigo = producto.codigo
            if not codigo in datos.keys():
                datos[codigo] = producto.to_dict()
                self.guardar_datos(datos)
                print(f"Producto {producto.nombre} creado correctamente.")
            else:
                print(f"Ya existe producto con código '{codigo}'.")
        except Exception as e:
            print(f'Error inesperado al crear producto: {e}')

    def leer_producto(self, codigo):
        try:
            datos = self.leer_datos()
            if codigo in datos:
                producto_data = datos[codigo]
                if 'garantia' in producto_data:
                    producto = ProductoElectronico(**producto_data)
                elif 'fecha_expiracion' in producto_data:
                    producto = ProductoAlimenticio(**producto_data)
                else:
                    producto = Producto(**producto_data)
                print(f'Producto encontrado con código {codigo}')
                print(producto)
            else:
                print(f'No se encontró producto con código {codigo}')
        except Exception as e:
            print(f'Error al leer producto: {e}')

    def actualizar_producto(self, codigo, nuevo_precio, nueva_cantidad):
        try:
            datos = self.leer_datos()
            if codigo in datos:
                datos[codigo]['precio'] = nuevo_precio
                datos[codigo]['cantidad'] = nueva_cantidad
                self.guardar_datos(datos)
                print(f'Producto con código {codigo} actualizado.')
            else:
                print(f'No se encontró producto con código {codigo}')
        
        except FileNotFoundError:
            print(f"No se encontro el archivo {self.archivo}")
  
        except Exception as e:
            print(f'Error al actualizar el producto: {e}')

    def eliminar_producto(self, codigo):
        try:
            datos = self.leer_datos()
            if codigo in datos:
                del datos[codigo]
                self.guardar_datos(datos)
                print(f'Producto con código {codigo} eliminado correctamente.')
            else:
                print(f'No se encontró producto con código {codigo}')
        except FileNotFoundError:
            print(f"EL archivo {self.archivo} no se encontro!")
        
        except KeyError as e_key:
            print(f"Se produjo un error en la clave del diccionario: {e_key} ")

        except Exception as e:
            print(f'Error al eliminar el producto: {e}')