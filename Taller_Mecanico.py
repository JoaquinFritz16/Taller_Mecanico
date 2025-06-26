import os
import mysql.connector


def conectar():
    try:
        print("Intentando conectar…")
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='taller_mecanico',
            port='3306',
            ssl_disabled=True
        )
        if conn.is_connected():
            print("Conexión exitosa.")
            return conn, conn.cursor()
    except Exception as e:
        print(f"Error al conectar: {e}")
        exit()


class Persona:
    def __init__(self):
        self.dni = self._leer_num("DNI")
        self.nombre = input("Nombre: ")
        self.apellido = input("Apellido: ")
        self.direccion = input("Dirección: ")
        self.telefono = self._leer_num("Teléfono")
        self.tele_contac = self._leer_num("Teléfono de contacto")

    def _leer_num(self, campo):
        while True:
            dato = input(f"{campo}: ")
            if dato.isdigit():
                return dato
            print(f"{campo} debe ser numérico. Intente de nuevo.")

class Cliente(Persona):
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def alta(self):
        print("\n=== Alta de Cliente ===")
        super().__init__()
        cod_cliente = input("Codigo del cliente: ")
        self.cursor.execute("SELECT * FROM cliente WHERE cod_cliente = %s", (cod_cliente,))
        if self.cursor.fetchone():
            print("Ya existe un cliente con ese código.")
            return
        self.cursor.execute(
            "INSERT INTO persona (dni, apellido, nombre, direccion, tele_contac) VALUES (%s, %s, %s, %s, %s)",
            (self.dni, self.apellido, self.nombre, self.direccion, self.telefono)
        )
        self.cursor.execute(
            "INSERT INTO cliente (cod_cliente, dni) VALUES (%s, %s)",
            (cod_cliente, self.dni)
        )
        self.conn.commit()
        print("Cliente agregado correctamente.")
    def baja(self):
        print("\n=== Baja de Cliente ===")
        cod_cliente = input("Ingrese Codigo del cliente a eliminar: ")
        self.cursor.execute("DELETE FROM empleado WHERE legajo = %s", (cod_cliente,))
        self.conn.commit()
        print("Cliente eliminado.")

    def modificar(self):
        print("\n=== Modificar Empleado ===")
        dni = input("Ingrese DNI del empleado a modificar: ")
        
        
        self.cursor.execute("SELECT * FROM persona WHERE dni = %s", (dni,))
        if not self.cursor.fetchone():
            print("No se encontró el cliente con ese DNI.")
            return


        print("Ingrese nuevos datos (dejar vacío para no modificar):")
        nuevo_nombre = input("Nuevo nombre: ")
        nuevo_apellido = input("Nuevo apellido: ")
        nueva_direccion = input("Nueva dirección: ")
        nuevo_telefono = input("Nuevo teléfono de contacto: ")

        if nuevo_nombre:
            self.cursor.execute("UPDATE persona SET nombre = %s WHERE dni = %s", (nuevo_nombre, dni))
        if nuevo_apellido:
            self.cursor.execute("UPDATE persona SET apellido = %s WHERE dni = %s", (nuevo_apellido, dni))
        if nueva_direccion:
            self.cursor.execute("UPDATE persona SET direccion = %s WHERE dni = %s", (nueva_direccion, dni))
        if nuevo_telefono:
            self.cursor.execute("UPDATE persona SET tele_contac = %s WHERE dni = %s", (nuevo_telefono, dni))

        self.conn.commit()
        print("Cliente modificado correctamente.")

    def listar(self):
        print("\n=== Lista de Clientes ===")
        self.cursor.execute("""
            SELECT c.cod_cliente, p.dni, p.nombre, p.apellido, p.direccion, p.tele_contac
            FROM cliente c
            JOIN persona p ON c.dni = p.dni
        """)
        resultados = self.cursor.fetchall()
        for fila in resultados:
            print(f"Código: {fila[0]} | DNI: {fila[1]} | Nombre: {fila[2]} {fila[3]} | Dirección: {fila[4]} | Tel: {fila[5]}")



class Empleado(Persona):
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def alta(self):
        print("\n=== Alta de Empleado ===")
        super().__init__()
        legajo = input("Legajo del empleado: ")
        self.cursor.execute(
            "INSERT INTO persona (dni, apellido, nombre, direccion, tele_contac) VALUES (%s, %s, %s, %s, %s)",
            (self.dni, self.apellido, self.nombre, self.direccion, self.telefono)
        )
        self.cursor.execute(
            "INSERT INTO empleado (legajo, dni) VALUES (%s, %s)",
            (legajo, self.dni)
        )
        self.conn.commit()
        print("Empleado agregado correctamente.")

    def baja(self):
        print("\n=== Baja de Empleado ===")
        legajo = input("Ingrese legajo del empleado a eliminar: ")
        self.cursor.execute("DELETE FROM empleado WHERE legajo = %s", (legajo,))
        self.conn.commit()
        print("Empleado eliminado.")

    def modificar(self):
        print("\n=== Modificar Empleado ===")
        dni = input("Ingrese DNI del empleado a modificar: ")

        print("Ingrese nuevos datos (dejar vacío para no modificar):")
        nuevo_nombre = input("Nuevo nombre: ")
        nuevo_apellido = input("Nuevo apellido: ")
        nueva_direccion = input("Nueva dirección: ")
        nuevo_telefono = input("Nuevo teléfono de contacto: ")

        if nuevo_nombre:
            self.cursor.execute("UPDATE persona SET nombre = %s WHERE dni = %s", (nuevo_nombre, dni))
        if nuevo_apellido:
            self.cursor.execute("UPDATE persona SET apellido = %s WHERE dni = %s", (nuevo_apellido, dni))
        if nueva_direccion:
            self.cursor.execute("UPDATE persona SET direccion = %s WHERE dni = %s", (nueva_direccion, dni))
        if nuevo_telefono:
            self.cursor.execute("UPDATE persona SET tele_contac = %s WHERE dni = %s", (nuevo_telefono, dni))

        self.conn.commit()
        print("Empleado modificado correctamente.")

    def listar(self):
        print("\n=== Lista de Empleados ===")
        self.cursor.execute("""
            SELECT e.legajo, p.dni, p.nombre, p.apellido, p.direccion, p.tele_contac
            FROM empleado e
            JOIN persona p ON e.dni = p.dni
        """)
        resultados = self.cursor.fetchall()
        for fila in resultados:
            print(f"Legajo: {fila[0]} | DNI: {fila[1]} | Nombre: {fila[2]} {fila[3]} | Dirección: {fila[4]} | Tel: {fila[5]}")


class Rodado:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def alta(self):
        print("\n=== Alta de Rodado ===")
        patente = input("Patente: ").upper()
        marca = input("Marca: ")
        modelo = input("Modelo: ")
        anio = input("Año: ")
        cod_cliente = input("Código del cliente propietario: ")


        self.cursor.execute("SELECT * FROM cliente WHERE cod_cliente = %s", (cod_cliente,))
        if not self.cursor.fetchone():
            print("El cliente no existe.")
            return

        self.cursor.execute("SELECT * FROM rodado WHERE patente = %s", (patente,))
        if self.cursor.fetchone():
            print("Ya existe un rodado con esa patente.")
            return

        self.cursor.execute(
            "INSERT INTO rodado (patente, marca, modelo, anio, cod_cliente) VALUES (%s, %s, %s, %s, %s)",
            (patente, marca, modelo, anio, cod_cliente)
        )
        self.conn.commit()
        print("Rodado registrado correctamente.")

    def baja(self):
        print("\n=== Baja de Rodado ===")
        patente = input("Ingrese la patente del rodado a eliminar: ").upper()
        self.cursor.execute("DELETE FROM rodado WHERE patente = %s", (patente,))
        self.conn.commit()
        print("Rodado eliminado.")

    def modificar(self):
        print("\n=== Modificar Rodado ===")
        patente = input("Ingrese la patente del rodado a modificar: ").upper()

        self.cursor.execute("SELECT * FROM rodado WHERE patente = %s", (patente,))
        if not self.cursor.fetchone():
            print("No se encontró un rodado con esa patente.")
            return

        nueva_marca = input("Nueva marca: ")
        nuevo_modelo = input("Nuevo modelo: ")
        nuevo_anio = input("Nuevo año: ")
        nuevo_cod_cliente = input("Nuevo código de cliente: ")

        if nueva_marca:
            self.cursor.execute("UPDATE rodado SET marca = %s WHERE patente = %s", (nueva_marca, patente))
        if nuevo_modelo:
            self.cursor.execute("UPDATE rodado SET modelo = %s WHERE patente = %s", (nuevo_modelo, patente))
        if nuevo_anio:
            self.cursor.execute("UPDATE rodado SET anio = %s WHERE patente = %s", (nuevo_anio, patente))
        if nuevo_cod_cliente:
            self.cursor.execute("SELECT * FROM cliente WHERE cod_cliente = %s", (nuevo_cod_cliente,))
            if not self.cursor.fetchone():
                print(" El nuevo cliente no existe. Cliente no cambiado.")
            else:
                self.cursor.execute("UPDATE rodado SET cod_cliente = %s WHERE patente = %s", (nuevo_cod_cliente, patente))

        self.conn.commit()
        print("Rodado modificado correctamente.")

    def listar(self):
        print("\n=== Lista de Rodados ===")
        self.cursor.execute("""
            SELECT r.patente, r.marca, r.modelo, r.anio, r.cod_cliente, p.nombre, p.apellido
            FROM rodado r
            JOIN cliente c ON r.cod_cliente = c.cod_cliente
            JOIN persona p ON c.dni = p.dni
        """)
        resultados = self.cursor.fetchall()
        for fila in resultados:
            print(f"Patente: {fila[0]} | Marca: {fila[1]} | Modelo: {fila[2]} | Año: {fila[3]} | Cliente: {fila[5]} {fila[6]} ({fila[4]})")
class FichaTecnica:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def crear(self):
        print("\n=== Crear Ficha Técnica ===")
        try:
            nro_ficha = int(input("Número de ficha: "))
            cod_cliente = input("Código de cliente: ")
            vehiculo = input("Patente del vehículo: ").upper()

  
            self.cursor.execute("SELECT * FROM cliente WHERE cod_cliente = %s", (cod_cliente,))
            if not self.cursor.fetchone():
                print("❌ Cliente no encontrado.")
                return

  
            self.cursor.execute("SELECT * FROM customer_detalle WHERE patente = %s", (vehiculo,))
            if not self.cursor.fetchone():
                print("❌ Vehículo no encontrado.")
                return


            subtotal = float(input("Subtotal de repuestos: "))
            mano_obra = float(input("Costo mano de obra: "))
            total_general = subtotal + mano_obra


            self.cursor.execute("""
                INSERT INTO ficha_tecnica (nro_ficha, cod_cliente, vehiculo, subtotal, mano_obra, total_general)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nro_ficha, cod_cliente, vehiculo, subtotal, mano_obra, total_general))

            self.conn.commit()
            print("✅ Ficha técnica creada correctamente.")

        except Exception as e:
            print(f"Error al crear ficha técnica: {e}")

def menu_principal(cursor, conn):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== MENÚ PRINCIPAL ===")
        print("1. Alta de Cliente")
        print("2. Alta de Empleado")
        print("3. Rodado")
        print("4. Facturacion      (pendiente)")
        print("5. Ficha Tecnica        (pendiente)")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            client = Cliente(cursor, conn)
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Gestión de Clientes ===")
                print("1. Alta")
                print("2. Baja")
                print("3. Modificar")
                print("4. Listar")
                print("5. Volver al menú principal")
                subop = input("Seleccione una opción: ")

                if subop == "1":
                    client.alta()
                elif subop == "2":
                    client.baja()
                elif subop == "3":
                    client.modificar()
                elif subop == "4":
                    client.listar()
                elif subop == "5":
                    break
                else:
                    print("Opción inválida.")

                input("\nPresione Enter para continuar…")

        elif opcion == "2":
            emp = Empleado(cursor, conn)
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Gestión de Empleados ===")
                print("1. Alta")
                print("2. Baja")
                print("3. Modificar")
                print("4. Listar")
                print("5. Volver al menú principal")
                subop = input("Seleccione una opción: ")

                if subop == "1":
                    emp.alta()
                elif subop == "2":
                    emp.baja()
                elif subop == "3":
                    emp.modificar()
                elif subop == "4":
                    emp.listar()
                elif subop == "5":
                    break
                else:
                    print("Opción inválida.")

                input("\nPresione Enter para continuar…")

        elif opcion == "3":
            rodado = Rodado(cursor, conn)
            while True:
                os.system('cls' if os.name == 'nt'   else 'clear')
                print("=== Gestión de Rodados ===")
                print("1. Alta")
                print("2. Baja")
                print("3. Modificar")
                print("4. Listar")
                print("5. Volver al menú principal")
                subop = input("Seleccione una opción: ")

                if subop == "1":
                    rodado.alta()
                elif subop == "2":
                    rodado.baja()
                elif subop == "3":
                    rodado.modificar()
                elif subop == "4":
                    rodado.listar()
                elif subop == "5":
                    break
                else:
                    print("Opción inválida.")

                input("\nPresione Enter para continuar…")


        elif opcion == "4":
            print("⚙️  Módulo Facturacion aún no implementado.")

        elif opcion == "5":
            ficha = FichaTecnica(cursor, conn)
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== Gestión de Fichas Técnicas ===")
                print("1. Crear ficha técnica")
                print("2. Volver al menú principal")
                subop = input("Seleccione una opción: ")

                if subop == "1":
                    ficha.crear()
                elif subop == "2":
                    break
                else:
                    print("Opción inválida.")

                input("\nPresione Enter para continuar…")


        elif opcion == "6":
            print("Saliendo del sistema…")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

        input("\nPresione Enter para continuar…")

if __name__ == "__main__":
    connection, cursor = conectar()
    try:
        menu_principal(cursor, connection)
    finally:
        cursor.close()
        connection.close()
        print("Conexión cerrada.")
