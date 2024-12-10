# pedidos.py
import json
import os

# Coordenadas aproximadas para los códigos postales
postal_coordinates = {
    "28821": (40.4238, -3.5611),  # Coslada
    "28822": (40.4215, -3.5650),
    "28823": (40.4265, -3.5620),
    "28850": (40.4566, -3.4697),  # Torrejón de Ardoz
    "28851": (40.4520, -3.4750),
    "28801": (40.4820, -3.3630),  # Alcalá de Henares
    "28802": (40.4815, -3.3690),
    "28803": (40.4810, -3.3740),
    "28840": (40.4022, -3.5101),  # Mejorada del Campo
    "28032": (40.4078, -3.6026),  # Vicálvaro
    "28830": (40.4242, -3.5321)   # San Fernando de Henares
}

# Locales en cada código postal (10 locales como ejemplo)
locales_por_postal = {
    "28821": ["Local A1", "Local A2"],
    "28822": ["Local B1", "Local B2"],
    "28823": ["Local C1", "Local C2"],
    "28850": ["Local D1", "Local D2"],
    "28851": ["Local E1", "Local E2"],
    "28801": ["Local F1", "Local F2"],
    "28802": ["Local G1", "Local G2"],
    "28803": ["Local H1", "Local H2"],
    "28840": ["Local I1", "Local I2"],
    "28032": ["Local J1", "Local J2"],
    "28830": ["Local K1", "Local K2"]
}

# Ruta del archivo JSON
archivo_pedidos = 'pedidos.json'

# Cargar pedidos desde el archivo JSON
def cargar_pedidos():
    if os.path.exists(archivo_pedidos):
        with open(archivo_pedidos, 'r') as f:
            return json.load(f)
    return []

# Guardar pedidos en el archivo JSON
def guardar_pedidos(pedidos):
    with open(archivo_pedidos, 'w') as f:
        json.dump(pedidos, f)

# Pedidos almacenados
pedidos = cargar_pedidos()

# Solicitar información de pedidos
def tomar_pedido():
    print("Bienvenido al sistema de pedidos.")
    codigo_postal = input("Ingrese el código postal del destino: ")

    if codigo_postal not in postal_coordinates:
        print("Lo sentimos, no realizamos envíos a este código postal.")
        return

    print(f"Locales disponibles en {codigo_postal}: {', '.join(locales_por_postal[codigo_postal])}")
    nombre = input("Ingrese su nombre: ")
    apellido = input("Ingrese su apellido: ")
    receptor = input("Ingrese el nombre del receptor: ")
    local = input("Seleccione el local al que se debe entregar: ")

    if local not in locales_por_postal[codigo_postal]:
        print("El local seleccionado no es válido para este código postal.")
        return

    nuevo_pedido = {
        "codigo_postal": codigo_postal,
        "nombre": nombre,
        "apellido": apellido,
        "receptor": receptor,
        "local": local,
        "coordenadas": postal_coordinates[codigo_postal]
    }

    pedidos.append(nuevo_pedido)
    guardar_pedidos(pedidos)  # Guardar pedidos en el archivo JSON

    print(f"Pedido registrado para {receptor} en {local}, código postal {codigo_postal}.")