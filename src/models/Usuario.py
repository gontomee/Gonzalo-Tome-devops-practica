#Clases que representan a los usuarios de la tienda
from __future__ import annotations

import uuid


class Usuario:
    #Cualquier persona que interactúa con la tienda

    def __init__(self, nombre: str, email: str) -> None:
        #Crea un usuario con un identificador único
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.email: str = email

    def is_admin(self) -> bool:
        #Indica si el usuario es administrador
        return False

    def __str__(self) -> str:
        #Representación legible del usuario.
        return f"[{self.id[:8]}] {self.nombre} <{self.email}>"


class Cliente(Usuario):
    #Usuario que realiza compras en la tienda

    def __init__(self, nombre: str, email: str, direccion: str) -> None:
        #Crea un cliente.
        super().__init__(nombre, email)
        self.direccion: str = direccion

    def __str__(self) -> str:
        #Representación legible del cliente
        return f"{super().__str__()} - Cliente | Dirección: {self.direccion}"


class Administrador(Usuario):
    #Gestor de la tienda.

    def is_admin(self) -> bool:
        #Los administradores siempre devuelven True
        return True

    def __str__(self) -> str:
        #Representación legible del administrador
        return f"{super().__str__()} - Administrador"
