import uuid
import datetime
import re

usuarios = {
    
}

paquetes = []
historial_estados = {}

def registrar_usuario():
    usuario = input("Ingrese un nuevo nombre de usuario: ")
    if usuario in usuarios:
        print("El usuario ya existe.")
        return
    contrasena = input("Ingrese una contrasena: ")
    rol = input("Rol (admin/cliente): ").strip().lower()
    if rol not in ["admin", "cliente"]:
        print("Rol no valido.")
        return
    usuarios[usuario] = {"password": contrasena, "rol": rol}
    print("Usuario registrado con exito.")

def autenticar_usuario():
    usuario = input("Usuario: ")
    contrasena = input("Contrasena: ")
    if usuario in usuarios and usuarios[usuario]["password"] == contrasena:
        print(f"Bienvenido, {usuario} ({usuarios[usuario]['rol']})")
        return usuarios[usuario]["rol"], usuario
    print("Autenticacion fallida.")
    return None, None

def registrar_paquete(usuario):
    destinatario = input("Nombre del destinatario: ")
    direccion = input("Direccion del destinatario: ")
    peso = float(input("Peso del paquete (kg): "))

    if peso <= 1:
        tipo, costo = "Basico", 5
    elif peso <= 5:
        tipo, costo = "Estandar", 10
    else:
        tipo, costo = "Dimensionado", 20

    id_paquete = str(uuid.uuid4())
    fecha_envio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    paquete = {
        "id": id_paquete, "destinatario": destinatario, "direccion": direccion,
        "peso": peso, "tipo": tipo, "estado": "Registrado", "cliente": usuario,
        "costo": costo, "fecha_envio": fecha_envio
    }

    paquetes.append(paquete)
    historial_estados[id_paquete] = [("Registrado", fecha_envio)]

    print(f"Paquete registrado con exito. ID: {id_paquete}")

def actualizar_estado():
    id_paquete = input("Ingrese el ID del paquete a actualizar: ")
    if id_paquete not in historial_estados:
        print("Paquete no encontrado.")
        return

    print("Seleccione el nuevo estado:")
    print("1. En transito")
    print("2. Entregado")
    opcion = input("Seleccione una opcion (1 o 2): ").strip()

    if opcion == "1":
        nuevo_estado = "En transito"
    elif opcion == "2":
        nuevo_estado = "Entregado"
    else:
        print("Opcion no valida.")
        return

    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historial_estados[id_paquete].append((nuevo_estado, fecha))

    for paquete in paquetes:
        if paquete["id"] == id_paquete:
            paquete["estado"] = nuevo_estado

    print("Estado actualizado con exito.")

def consultar_historial():
    id_paquete = input("Ingrese el ID del paquete: ").strip()
    if id_paquete in historial_estados:
        print("Historial del paquete:")
        for estado, fecha in historial_estados[id_paquete]:
            print(f"- {estado} en {fecha}")
    else:
        print("No se encontro historial para este paquete.")

def generar_factura_y_pagar():
    id_paquete = input("Ingrese el ID del paquete: ")
    for paquete in paquetes:
        if paquete["id"] == id_paquete:
            print(f"\n--- FACTURA ---\nID: {paquete['id']}\nDestinatario: {paquete['destinatario']}\nDireccion: {paquete['direccion']}\nTipo: {paquete['tipo']}\nCosto: ${paquete['costo']}\nEstado: {paquete['estado']}\nFecha de envio: {paquete['fecha_envio']}\n")
            metodo = input("Metodo de pago (tarjeta/efectivo): ").strip().lower()
            if metodo == "tarjeta":
                cuenta_nombre = input("Nombre de la cuenta: ").strip()
                cuenta_numero = input("Numero de cuenta (10 digitos): ").strip()
                
                if not re.match(r'^[a-zA-Z ]+$', cuenta_nombre):
                    print("Nombre de cuenta invalido.")
                    return
                
                if len(cuenta_numero) != 10 or not cuenta_numero.isdigit():
                    print("Numero de cuenta invalido.")
                    return

            print("Pago registrado con exito.")
            return
    print("Paquete no encontrado.")

def menu_usuario(usuario):
    while True:
        print("\n--- MENU CLIENTE ---")
        print("1. Registrar paquete")
        print("2. Consultar historial de un paquete")
        print("3. Generar factura y pagar")
        print("4. Cerrar sesion")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            registrar_paquete(usuario)
        elif opcion == "2":
            consultar_historial()
        elif opcion == "3":
            generar_factura_y_pagar()
        elif opcion == "4":
            break
        else:
            print("Opcion no valida.")

def menu_admin():
    while True:
        print("\n--- MENU ADMINISTRADOR ---")
        print("1. Consultar historial de un paquete")
        print("2. Actualizar estado de un paquete")
        print("3. Cerrar sesion")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            consultar_historial()
        elif opcion == "2":
            actualizar_estado()
        elif opcion == "3":
            break
        else:
            print("Opcion no valida.")

def menu():
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Iniciar sesion")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            rol, usuario = autenticar_usuario()
            if rol == "cliente":
                menu_usuario(usuario)
            elif rol == "admin":
                menu_admin()
        elif opcion == "2":
            registrar_usuario()
        elif opcion == "3":
            break
        else:
            print("Opcion no valida.")

menu()
