import os
import mysql.connector

os.system('cls')

try:
    # Connect to the MySQL database
    print("Intentando conectar...")
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='taller_mecanico',
        port='3306',  
        ssl_disabled=True 
    )
    if connection.is_connected():
        print("Conexión exitosa a la base de datos.")
        cursor= connection.cursor()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit()

class Persona:
    def __init__(self):
        while True:
            self.dni = input("Ingrese el DNI de la persona: ")
            if self.dni.isdigit():
                break
            else:
                print("El DNI debe contener solo números. Inténtalo de nuevo.")
        self.nombre = input("Ingrese el nombre de la persona: ")
        self.apellido = input("Ingrese el apellido de la persona:")
                              

        self.direccion = input("Ingrese el direccion de la persona: ")

        while True:
            self.telefono = input("Ingrese el telefono de la persona: ")
            if self.telefono.isdigit():
                break
            else:
                print("El telefono debe contener solo números. Inténtalo de nuevo.")
        while True:
            self.tele_contac = input("Ingrese el telefono de contacto de la persona: ")
            if self.tele_contac.isdigit():
                break
            else:
                print("El telefono de contacto debe contener solo números. Inténtalo de nuevo.")

class Cliente(Persona):
    def __init__(self):
        super().__init__()
        self.alta()

    def alta(self):
        insert_query = "INSERT INTO persona (dni, apellido, nombre, direccion, tele_contac) VALUES (%s, %s, %s, %s, %s)"
        insert_query1 = "INSERT INTO cliente (cod_cliente, dni) VALUES (%s, %s)"

        self.cod_cliente = input("Ingrese el código del cliente: ")
        data = (self.dni, self.apellido, self.nombre, self.direccion, self.telefono)
        data1 = (self.cod_cliente, self.dni)

        cursor.execute(insert_query, data)
        cursor.execute(insert_query1, data1)
        connection.commit()
        print("Cliente agregado correctamente.")

cliente = Cliente()

cursor.close()
connection.close()  
print("Conexión a la base de datos cerrada.")