#Capa de servicios: gestiona de forma centralizada las operaciones de la tienda.
from __future__ import annotations

from models.Pedido import Pedido
from models.Producto import Producto
from models.Usuario import Administrador, Cliente, Usuario


class TiendaService:
    #Intermediario entre usuarios, productos y pedidos

    def __init__(self) -> None:
        #Inicializa la tienda con inventario, usuarios y pedidos vacíos.
        self.usuarios: dict[str, Usuario] = {}
        self.inventario: dict[str, Producto] = {}
        self.pedidos: list[Pedido] = []

    #Usuarios
    def registrar_usuario(self, tipo: str, nombre: str, email: str,
                          direccion: str | None = None) -> Usuario:
        #Registra un usuario y lo añade al diccionario de usuarios.
        tipo = tipo.strip().lower()
        if tipo == "cliente":
            if not direccion:
                raise ValueError("Un cliente necesita una dirección postal.")
            usuario: Usuario = Cliente(nombre, email, direccion)
        elif tipo in ("administrador", "admin"):
            usuario = Administrador(nombre, email)
        else:
            raise ValueError(f"Tipo de usuario no válido: '{tipo}'.")
        self.usuarios[usuario.id] = usuario
        return usuario

    def obtener_usuario(self, usuario_id: str) -> Usuario | None:
        #Devuelve el usuario con ese id o None si no existe
        return self.usuarios.get(usuario_id)

    def listar_usuarios(self) -> list[Usuario]:
        #Devuelve la lista de usuarios registrados
        return list(self.usuarios.values())

    #Productos
    def agregar_producto(self, producto: Producto) -> Producto:
        #Añade un producto 
        if not isinstance(producto, Producto):
            raise TypeError("Solo se pueden añadir objetos de tipo Producto.")
        self.inventario[producto.id] = producto
        return producto

    def obtener_producto(self, producto_id: str) -> Producto | None:
        #Devuelve el producto con ese id o None si no existe
        return self.inventario.get(producto_id)

    def eliminar_producto(self, producto_id: str) -> bool:
        #Elimina un producto del inventario. True si existía
        return self.inventario.pop(producto_id, None) is not None

    def listar_productos(self) -> list[Producto]:
        """Devuelve la lista de productos del inventario."""
        return list(self.inventario.values())

    #Pedidos
    def realizar_pedido(self, usuario_id: str,
                        productos: dict[str, int]) -> Pedido:
        #Crea un pedido para un usuario con los productos y cantidades indicadas.
        usuario = self.obtener_usuario(usuario_id)
        if usuario is None:
            raise ValueError(f"El usuario '{usuario_id}' no existe.")
        if not isinstance(usuario, Cliente):
            raise ValueError(f"'{usuario.nombre}' no es un cliente y no puede hacer pedidos.")
        if not productos:
            raise ValueError("El pedido no contiene productos.")

        # 1) Validar todo antes de modificar nada
        lineas: list[tuple[Producto, int]] = []
        for producto_id, cantidad in productos.items():
            producto = self.inventario.get(producto_id)
            if producto is None:
                raise ValueError(f"El producto '{producto_id}' no existe.")
            if not producto.hay_stock(cantidad):
                raise ValueError(
                    f"Stock insuficiente de '{producto.nombre}': "
                    f"disponible {producto.stock}, solicitado {cantidad}."
                )
            lineas.append((producto, cantidad))

        # 2) Descontar stock y crear el pedido
        for producto, cantidad in lineas:
            producto.actualizar_stock(-cantidad)
        pedido = Pedido(usuario, lineas)
        self.pedidos.append(pedido)
        return pedido

    def listar_pedidos_usuario(self, usuario_id: str) -> list[Pedido]:
        #Devuelve los pedidos de un usuario ordenados por fecha 
        return sorted(
            (p for p in self.pedidos if p.cliente.id == usuario_id),
            key=lambda p: p.fecha,
        )
