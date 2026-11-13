#Punto de entrada: API REST de la tienda online con FastAPI.
#Creado por Gonzalo Tome Gomez
#Ejecutar con:  python -m uvicorn main:app --reload   y abrir http://127.0.0.1:8000/docs
from __future__ import annotations
from fastapi import FastAPI, HTTPException, Response, status
from models import Cliente
from schemas import (PedidoCreate, PedidoRead, ProductoCreate, ProductoRead, UsuarioCreate, UsuarioRead)
from Services import TiendaService

app = FastAPI(title="Tienda online", version="2.0",
              description="API REST de la tienda online (Práctica 2).")

#Única instancia del servicio: los datos viven en memoria mientras corre el servidor
tienda = TiendaService()

#Usuarios
@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED,
          tags=["Usuarios"])
def crear_usuario(datos: UsuarioCreate) -> UsuarioRead:
    #Crea un nuevo usuario (cliente o administrador)
    if any(u.email.lower() == datos.email.lower() for u in tienda.listar_usuarios()):
        raise HTTPException(status.HTTP_409_CONFLICT,
                            f"Ya existe un usuario con el email '{datos.email}'.")
    try:
        usuario = tienda.registrar_usuario(datos.tipo, datos.nombre,
                                           datos.email, datos.direccion)
    except ValueError as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(error))
    return UsuarioRead.desde_modelo(usuario)
@app.get("/usuarios", response_model=list[UsuarioRead], tags=["Usuarios"])
def listar_usuarios() -> list[UsuarioRead]:
    #Devuelve todos los usuarios registrados
    return [UsuarioRead.desde_modelo(u) for u in tienda.listar_usuarios()]
@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead, tags=["Usuarios"])
def obtener_usuario(usuario_id: str) -> UsuarioRead:
    #Devuelve un usuario concreto
    usuario = tienda.obtener_usuario(usuario_id)
    if usuario is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"El usuario '{usuario_id}' no existe.")
    return UsuarioRead.desde_modelo(usuario)
#Productos
@app.post("/productos", response_model=ProductoRead, status_code=status.HTTP_201_CREATED,
          tags=["Productos"])
def crear_producto(datos: ProductoCreate) -> ProductoRead:
    #Crea un producto genérico, electrónico o de ropa
    try:
        producto = tienda.agregar_producto(datos.a_modelo())
    except (ValueError, TypeError) as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(error))
    return ProductoRead.desde_modelo(producto)


@app.get("/productos", response_model=list[ProductoRead], tags=["Productos"])
def listar_productos() -> list[ProductoRead]:
    #Devuelve todos los productos del inventario
    return [ProductoRead.desde_modelo(p) for p in tienda.listar_productos()]


@app.get("/productos/{producto_id}", response_model=ProductoRead, tags=["Productos"])
def obtener_producto(producto_id: str) -> ProductoRead:
    #Devuelve un producto concreto
    producto = tienda.obtener_producto(producto_id)
    if producto is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"El producto '{producto_id}' no existe.")
    return ProductoRead.desde_modelo(producto)


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT,
            tags=["Productos"])
def eliminar_producto(producto_id: str) -> Response:
    #Elimina un producto del inventario
    if not tienda.eliminar_producto(producto_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"El producto '{producto_id}' no existe.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#Pedidos
@app.post("/pedidos", response_model=PedidoRead, status_code=status.HTTP_201_CREATED,
          tags=["Pedidos"])
def crear_pedido(datos: PedidoCreate) -> PedidoRead:
    #Crea un pedido comprobando cliente, productos y stock
    usuario = tienda.obtener_usuario(datos.cliente_id)
    if usuario is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"El cliente '{datos.cliente_id}' no existe.")
    if not isinstance(usuario, Cliente):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            f"'{usuario.nombre}' no es un cliente y no puede hacer pedidos.")

    #Agrupa las líneas por producto (si se repite un producto se suman cantidades)
    productos: dict[str, int] = {}
    for item in datos.items:
        if tienda.obtener_producto(item.producto_id) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                f"El producto '{item.producto_id}' no existe.")
        productos[item.producto_id] = productos.get(item.producto_id, 0) + item.cantidad

    try:
        pedido = tienda.realizar_pedido(datos.cliente_id, productos)
    except ValueError as error:
        #Por ejemplo, stock insuficiente
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(error))
    return PedidoRead.desde_modelo(pedido)


@app.get("/usuarios/{cliente_id}/pedidos", response_model=list[PedidoRead],
         tags=["Pedidos"])
def listar_pedidos_cliente(cliente_id: str) -> list[PedidoRead]:
    #Devuelve el historial de pedidos de un cliente
    if tienda.obtener_usuario(cliente_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"El cliente '{cliente_id}' no existe.")
    return [PedidoRead.desde_modelo(p) for p in tienda.listar_pedidos_usuario(cliente_id)]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
