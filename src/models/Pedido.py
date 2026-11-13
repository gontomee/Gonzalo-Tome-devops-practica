"""Clase que representa un pedido de la tienda."""
from __future__ import annotations

import uuid
from datetime import datetime

from .Producto import Producto
from .Usuario import Cliente


class Pedido:
    #Pedido realizado por un cliente con una lista de productos y cantidades

    def __init__(self, cliente: Cliente,
                 lineas: list[tuple[Producto, int]],
                 fecha: datetime | None = None) -> None:
        #Crea un pedido.
        if not isinstance(cliente, Cliente):
            raise TypeError("Un pedido debe estar vinculado a un Cliente.")
        if not lineas:
            raise ValueError("Un pedido debe contener al menos un producto.")
        self.id: str = str(uuid.uuid4())
        self.cliente: Cliente = cliente
        self.lineas: list[tuple[Producto, int]] = list(lineas)
        self.fecha: datetime = fecha or datetime.now()

    def calcular_total(self) -> float:
        #Calcula el importe total del pedido
        return sum(producto.precio * cantidad for producto, cantidad in self.lineas)

    def __str__(self) -> str:
        #Resumen
        detalle = "\n".join(
            f"    - {producto.nombre} x{cantidad} "
            f"({producto.precio:.2f} €/ud) = {producto.precio * cantidad:.2f} €"
            for producto, cantidad in self.lineas
        )
        return (f"Pedido [{self.id[:8]}] - {self.fecha:%d/%m/%Y %H:%M:%S}\n"
                f"  Cliente: {self.cliente.nombre}\n"
                f"{detalle}\n"
                f"  TOTAL: {self.calcular_total():.2f} €")
