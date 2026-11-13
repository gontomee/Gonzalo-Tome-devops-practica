#Esquemas Pydantic de productos (peticiones y respuestas de la API)
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator

from models.Producto import Producto, ProductoElectronico, ProductoRopa

TipoProducto = Literal["generico", "electronico", "ropa"]


class ProductoCreate(BaseModel):
    #Datos que envía el cliente para crear un producto
    tipo: TipoProducto = Field(..., examples=["electronico"])
    nombre: str = Field(..., min_length=1, examples=["Portátil"])
    precio: float = Field(..., ge=0, examples=[899.99])
    stock: int = Field(..., ge=0, examples=[10])
    #Electrónica
    meses_garantia: Optional[int] = Field(None, ge=0, examples=[24])
    #Ropa
    talla: Optional[str] = Field(None, min_length=1, examples=[None])
    color: Optional[str] = Field(None, min_length=1, examples=[None])

    @model_validator(mode="after")
    def comprobar_atributos(self) -> "ProductoCreate":
        #Cada tipo de producto exige sus atributos propios
        if self.tipo == "electronico" and self.meses_garantia is None:
            raise ValueError("Un producto electrónico necesita 'meses_garantia'.")
        if self.tipo == "ropa" and (not self.talla or not self.color):
            raise ValueError("Un producto de ropa necesita 'talla' y 'color'.")
        return self

    def a_modelo(self) -> Producto:
        #Crea el objeto del dominio correspondiente al tipo
        if self.tipo == "electronico":
            return ProductoElectronico(self.nombre, self.precio, self.stock,
                                       self.meses_garantia)
        if self.tipo == "ropa":
            return ProductoRopa(self.nombre, self.precio, self.stock,
                                self.talla, self.color)
        return Producto(self.nombre, self.precio, self.stock)


class ProductoRead(BaseModel):
    #Datos del producto que se devuelven al cliente
    id: str
    tipo: TipoProducto
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None

    @classmethod
    def desde_modelo(cls, producto: Producto) -> "ProductoRead":
        #Convierte un objeto Producto del dominio en el esquema de salida
        datos = dict(id=producto.id, nombre=producto.nombre,
                     precio=producto.precio, stock=producto.stock)
        if isinstance(producto, ProductoElectronico):
            return cls(tipo="electronico", meses_garantia=producto.meses_garantia, **datos)
        if isinstance(producto, ProductoRopa):
            return cls(tipo="ropa", talla=producto.talla, color=producto.color, **datos)
        return cls(tipo="generico", **datos)
