import folium
from geopy.distance import geodesic
import networkx as nx
import json
import os
import random
from colorama import Fore, Style, init

# Coordenadas base por código postal
postal_coordinates = {
    # Coslada
    "28821": (40.4238, -3.5611),
    "28822": (40.4215, -3.5650),
    "28823": (40.4265, -3.5620),
    # Torrejón de Ardoz
    "28850": (40.4566, -3.4697),
    "28851": (40.4520, -3.4750),
    # Alcalá de Henares
    "28801": (40.4820, -3.3630),
    "28802": (40.4815, -3.3690),
    "28803": (40.4810, -3.3740),
    "28804": (40.4780, -3.3800),
    "28805": (40.4790, -3.3850),
    "28806": (40.4800, -3.3900),
    "28807": (40.4810, -3.3950),
    # Mejorada del Campo
    "28840": (40.4022, -3.5101),
    # Vicálvaro
    "28032": (40.4078, -3.6026),
    # San Fernando de Henares
    "28830": (40.4242, -3.5321)
}



# Simular locales con pequeñas variaciones de las coordenadas base
def generar_locales(postal_coordinates, locales_por_postal):
    locales = {}
    for postal, coords in postal_coordinates.items():
        for idx in range(len(locales_por_postal[postal])):
            # Simular locales cercanos con desplazamientos aleatorios menores
            delta_lat = random.uniform(-0.005, 0.005)
            delta_lon = random.uniform(-0.005, 0.005)
            local_coords = (coords[0] + delta_lat, coords[1] + delta_lon)
            local_name = f"{postal}_Local{idx+1}"
            locales[local_name] = {"coords": local_coords, "postal": postal}
    return locales

# Locales por código postal
locales_por_postal = {
    "28821": ["Local A1", "Local A2"],
    "28822": ["Local B1", "Local B2"],
    "28823": ["Local C1", "Local C2"],
    "28850": ["Local D1", "Local D2"],
    "28851": ["Local E1", "Local E2"],
    "28801": ["Local F1", "Local F2"],
    "28802": ["Local G1", "Local G2"],
    "28803": ["Local H1", "Local H2"],
    "28804": ["Local I1", "Local I2"],
    "28805": ["Local J1", "Local J2"],
    "28806": ["Local K1", "Local K2"],
    "28807": ["Local L1", "Local L2"],
    "28840": ["Local M1", "Local M2"],
    "28032": ["Local N1", "Local N2"],
    "28830": ["Local O1", "Local O2"]
}

locales = generar_locales(postal_coordinates, locales_por_postal)

# Construir un grafo con distancias y tiempos
def construir_grafo(locales):
    grafo = nx.Graph()
    nodos = list(locales.keys())

    for i, nodo1 in enumerate(nodos):
        for j, nodo2 in enumerate(nodos):
            if i >= j:
                continue  # No repetir conexiones
            coords1 = locales[nodo1]["coords"]
            coords2 = locales[nodo2]["coords"]
            distancia = geodesic(coords1, coords2).kilometers
            tiempo = distancia / 40 * 60  # Tiempo en minutos, velocidad promedio 40 km/h
            grafo.add_edge(nodo1, nodo2, weight=distancia, tiempo=tiempo)
    return grafo

grafo_locales = construir_grafo(locales)

# Mostrar una muestra del grafo
grafo_locales.edges(data=True)

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


# Inicializar colorama
init(autoreset=True)

# Separador decorativo
def imprimir_encabezado(texto):
    print(f"\n{Fore.CYAN}{'=' * 50}")
    print(f"{Fore.GREEN}{texto.center(50)}")
    print(f"{Fore.CYAN}{'=' * 50}")

# Separador para secciones
def imprimir_separador():
    print(f"{Fore.CYAN}{'-' * 50}")

# Mejorar la estética de la función de toma de pedidos
def tomar_pedido():
    imprimir_encabezado("Sistema de Pedidos")

    print(f"{Fore.YELLOW}Ingrese el código postal del destino:")
    codigo_postal = input("> ").strip()

    if codigo_postal not in postal_coordinates:
        imprimir_separador()
        print(f"{Fore.RED}No realizamos envíos a este código postal.")
        imprimir_separador()
        return

    imprimir_separador()
    print(f"{Fore.YELLOW}Locales disponibles en {codigo_postal}:")
    for idx, local in enumerate(locales_por_postal[codigo_postal], 1):
        print(f"{Fore.CYAN}  {idx}. {local}")

    print(f"{Fore.YELLOW}Seleccione el número del local al que se debe entregar:")
    try:
        local_seleccion = int(input("> ")) - 1
        local = locales_por_postal[codigo_postal][local_seleccion]
    except (ValueError, IndexError):
        imprimir_separador()
        print(f"{Fore.RED}Opción inválida. Intente de nuevo.")
        imprimir_separador()
        return

    imprimir_separador()
    print(f"{Fore.YELLOW}Ingrese los datos del cliente:")
    nombre = input(f"{Fore.YELLOW}Nombre: > ").strip()
    apellido = input(f"{Fore.YELLOW}Apellido: > ").strip()
    receptor = input(f"{Fore.YELLOW}Nombre del receptor: > ").strip()
    receptor_apellido = input(f"{Fore.YELLOW}Apellido del receptor: > ").strip()
    receptor_dni = input(f"{Fore.YELLOW}DNI del receptor: > ").strip()

    imprimir_separador()
    print(f"{Fore.YELLOW}Ingrese el número de paquetes a enviar:")
    try:
        num_paquetes = int(input("> "))
    except ValueError:
        print(f"{Fore.RED}Número inválido. Intente de nuevo.")
        return

    paquetes = []
    peso_total = 0
    volumen_total = 0

    for i in range(num_paquetes):
        imprimir_encabezado(f"Datos del paquete {i + 1}")
        nombre_paquete = input(f"{Fore.YELLOW}Nombre del paquete: > ").strip()
        try:
            peso = float(input(f"{Fore.YELLOW}Peso (kg): > "))
            volumen = float(input(f"{Fore.YELLOW}Volumen (m³): > "))
        except ValueError:
            print(f"{Fore.RED}Datos inválidos. Intente de nuevo.")
            continue

        if peso_total + peso > 700:
            print(f"{Fore.RED}Excedería el límite de peso del camión (700 kg). Paquete no agregado.")
            continue

        if volumen_total + volumen > 9:
            print(f"{Fore.RED}Excedería el límite de volumen del camión (9 m³). Paquete no agregado.")
            continue

        paquetes.append({"nombre": nombre_paquete, "peso": peso, "volumen": volumen})
        peso_total += peso
        volumen_total += volumen

    pedidos.append({
        "codigo_postal": codigo_postal,
        "nombre": nombre,
        "apellido": apellido,
        "receptor": receptor,
        "receptor_apellido": receptor_apellido,
        "receptor_dni": receptor_dni,
        "local": local,
        "coordenadas": postal_coordinates[codigo_postal],
        "paquetes": paquetes,
        "peso_total": peso_total,
        "volumen_total": volumen_total
    })

    imprimir_encabezado("Pedido Registrado")
    print(f"{Fore.GREEN}Cliente: {nombre} {apellido}")
    print(f"Receptor: {receptor} {receptor_apellido} (DNI: {receptor_dni})")
    print(f"Local: {local}, Código Postal: {codigo_postal}")
    print(f"Peso Total: {peso_total} kg, Volumen Total: {volumen_total} m³")
    imprimir_separador()

    # Guardar pedidos en el archivo JSON
    guardar_pedidos(pedidos)
    print(f"{Fore.GREEN}Los pedidos han sido guardados correctamente.")
    imprimir_separador()
    
    # Menú principal
def menu_principal():
    while True:
        print(f"\n{Fore.CYAN}=== MENÚ PRINCIPAL ===")
        print("1. Hacer un pedido")
        print("2. Mostrar mapa de locales")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            tomar_pedido()
        elif opcion == "2":
            mostrar_mapa()
        elif opcion == "3":
            print(f"{Fore.GREEN}Gracias por usar el sistema.")
            break
        else:
            print(f"{Fore.RED}Opción inválida.")

# Ejecutar menú principal
menu_principal()
    
# Planificación y cálculo de rutas
def planificar_entregas(pedidos, capacidad_camion=3):
    rutas = []
    for i in range(0, len(pedidos), capacidad_camion):
        ruta_actual = pedidos[i:i + capacidad_camion]
        rutas.append(calcular_ruta(ruta_actual))
    return rutas

# Calcular la ruta óptima para un conjunto de entregas
def calcular_ruta (pedidos_ruta):
    graph = nx.Graph()
    nodos = [(pedido["local"], pedido["coordenadas"]) for pedido in pedidos_ruta]

    # Crear un grafo con distancias entre nodos
    for i, (local1, coord1) in enumerate(nodos):
        for j, (local2, coord2) in enumerate(nodos):
            if i != j:
                dist = geodesic(coord1, coord2).kilometers
                graph.add_edge(local1, local2, weight=dist)

    # Encontrar la ruta óptima usando el TSP (Nearest Neighbor)
    nodes = list(graph.nodes)
    ruta_optima = tsp_nearest_neighbor(graph, nodes[0])

    # Calcular distancia total
    distancia_total = sum(graph[u][v]['weight'] for u, v in zip(ruta_optima[:-1], ruta_optima[1:]))
    return ruta_optima, distancia_total

# Heurística TSP Nearest Neighbor
def tsp_nearest_neighbor(graph, start_node):
    visited = [start_node]
    current_node = start_node

    while len(visited) < len(graph.nodes):
        neighbors = graph[current_node]
        next_node = min((n for n in neighbors if n not in visited), key=lambda n: neighbors[n]['weight'])
        visited.append(next_node)
        current_node = next_node

    visited.append(start_node)  # Volver al punto inicial
    return visited

# Visualizar ruta en mapa
def visualizar_ruta(ruta, nombre="ruta"):
    mapa = folium.Map(location=list(postal_coordinates.values())[0], zoom_start=12)

    for local in ruta[0]:
        coord = next(pedido["coordenadas"] for pedido in pedidos if pedido["local"] == local)
        folium.Marker(location=coord, popup=local).add_to(mapa)

    # Crear polilínea para la ruta
    coords_ruta = [next(pedido["coordenadas"] for pedido in pedidos if pedido["local"] == local) for local in ruta[0]]
    folium.PolyLine(coords_ruta, color="blue", weight=2.5, opacity=1).add_to(mapa)

    mapa.save(f"{nombre}.html")
    print(f"Ruta guardada como {nombre}.html")

# Eliminar pedidos entregados
def eliminar_pedidos_entregados(rutas):
    global pedidos
    entregados = [pedido for ruta, _ in rutas for pedido in ruta[0]]  # Cambiado para acceder correctamente a los locales
    pedidos = [pedido for pedido in pedidos if pedido["local"] not in entregados]
    guardar_pedidos(pedidos)  # Guardar la lista actualizada de pedidos

# Prueba con datos simulados
for _ in range(12):  # 12 pedidos simulados
    tomar_pedido()

rutas = planificar_entregas(pedidos)
if rutas:
    print("Rutas calculadas:")
    for idx, (ruta, distancia) in enumerate(rutas, 1):
        print(f"Ruta {idx}: {ruta} | Distancia total: {distancia:.2f} km")
        visualizar_ruta((ruta, distancia), f"ruta_{idx}")

    eliminar_pedidos_entregados(rutas)  # Eliminar pedidos ya entregados 