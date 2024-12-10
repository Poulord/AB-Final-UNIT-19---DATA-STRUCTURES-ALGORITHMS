# rutas.py
import json
import networkx as nx
from geopy.distance import geodesic
import folium
from pedidos import tomar_pedido, guardar_pedidos


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