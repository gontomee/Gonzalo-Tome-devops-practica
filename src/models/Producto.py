##Clases que representan los productos de la tienda
from __future__ import annotations

import uuid


class Producto:
    #Producto genérico de la tienda. Clase padre del resto de productos

    def __init__(self, nombre: str, precio: float, stock: int) -> None:
        #Crea un producto con un identificador único generado automáticamente.
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.precio: float = precio
        self.stock: int = stock

    def hay_stock(self, cantidad: int) -> bool:
        #Indica si hay stock suficiente para servir la cantidad solicitada
        return cantidad > 0 and self.stock >= cantidad

    def actualizar_stock(self, cantidad: int) -> None:
        #Actualiza el stock sumando la cantidad indicada.
        if self.stock + cantidad < 0:
            raise ValueError(
                f"Stock insuficiente de '{self.nombre}': "
                f"disponible {self.stock}, solicitado {-cantidad}."
            )
        self.stock += cantidad

    def __str__(self) -> str:
        #Devuelve las características principales del producto.
        return (f"[{self.id[:8]}] {self.nombre} - {self.precio:.2f} € "
                f"(stock: {self.stock})")


class ProductoElectronico(Producto):
    #Producto electrónico con meses de garantía.

    def __init__(self, nombre: str, precio: float, stock: int,
                 meses_garantia: int) -> None:
        #Crea un producto electrónico.
        super().__init__(nombre, precio, stock)
        self.meses_garantia: int = meses_garantia

    def __str__(self) -> str:
        #Descripción del producto incluyendo la garantía
        return f"{super().__str__()} | Electrónica - garantía: {self.meses_garantia} meses"


class ProductoRopa(Producto):
    #Prenda de ropa con talla y color.

    def __init__(self, nombre: str, precio: float, stock: int,
                 talla: str, color: str) -> None:
        #Crea una prenda de ropa
        super().__init__(nombre, precio, stock)
        self.talla: str = talla
        self.color: str = color

    def __str__(self) -> str:
        #Descripción del producto incluyendo talla y color
        return f"{super().__str__()} | Ropa - talla: {self.talla}, color: {self.color}"
