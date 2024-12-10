# main.py
from pedidos import tomar_pedido
from rutas import cargar_pedidos, calcular_ruta

# Tomar un nuevo pedido
tomar_pedido()

# Cargar pedidos y calcular rutas
pedidos = cargar_pedidos()
if pedidos:
    ruta, distancia = calcular_ruta(pedidos)
    print(f"Ruta calculada: {ruta} | Distancia total: {distancia:.2f} km")