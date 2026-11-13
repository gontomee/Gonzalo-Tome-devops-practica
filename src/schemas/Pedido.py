#Esquemas Pydantic de pedidos (peticiones y respuestas de la API)
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from models.Pedido import Pedido


class PedidoItemCreate(BaseModel):
    #Una línea del pedido: qué producto y cuántas unidades
    producto_id: str
    cantidad: int = Field(..., gt=0, examples=[1])


class PedidoCreate(BaseModel):
    #Datos que envía el cliente para crear un pedido
    cliente_id: str
    items: list[PedidoItemCreate] = Field(..., min_length=1)


class PedidoItemRead(BaseModel):
    #Línea del pedido que se devuelve al cliente
    producto_id: str
    nombre: str
    precio_unitario: float
    cantidad: int
    subtotal: float


class PedidoRead(BaseModel):
    #Pedido completo que se devuelve al cliente
    id: str
    fecha: datetime
    cliente_id: str
    cliente_nombre: str
    total: float
    items: list[PedidoItemRead]

    @classmethod
    def desde_modelo(cls, pedido: Pedido) -> "PedidoRead":
        #Convierte un objeto Pedido del dominio en el esquema de salida
        items = [
            PedidoItemRead(producto_id=producto.id, nombre=producto.nombre,
                           precio_unitario=producto.precio, cantidad=cantidad,
                           subtotal=round(producto.precio * cantidad, 2))
            for producto, cantidad in pedido.lineas
        ]
        return cls(id=pedido.id, fecha=pedido.fecha, cliente_id=pedido.cliente.id,
                   cliente_nombre=pedido.cliente.nombre,
                   total=round(pedido.calcular_total(), 2), items=items)
