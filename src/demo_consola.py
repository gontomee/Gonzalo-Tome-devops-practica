#Punto de entrada: prueba manual del funcionamiento de la tienda online.
#Creado por Gonzalo Tome Gomez
from __future__ import annotations

from models import ProductoElectronico, ProductoRopa
from Services import TiendaService


def separador(titulo: str) -> None:
    #Imprime un título
    print(f"\n{'=' * 60}\n{titulo}\n{'=' * 60}")


def mostrar_inventario(tienda: TiendaService) -> None:
    #Muestra todos los productos
    for producto in tienda.listar_productos():
        print(f"  {producto}")


def main() -> None:
    #Crea la tienda, registra usuarios y productos y simula pedidos.
    tienda = TiendaService()

    #Usuarios
    separador("REGISTRO DE USUARIOS")
    ana = tienda.registrar_usuario("cliente", "Ana García", "ana@mail.com",
                                   "C/ Mayor 1, Madrid")
    luis = tienda.registrar_usuario("cliente", "Luis Pérez", "luis@mail.com",
                                    "Av. Diagonal 100, Barcelona")
    marta = tienda.registrar_usuario("cliente", "Marta López", "marta@mail.com",
                                     "C/ Colón 5, Valencia")
    admin = tienda.registrar_usuario("administrador", "Admin", "admin@tienda.com")
    for usuario in (ana, luis, marta, admin):
        print(f"  {usuario}  (is_admin={usuario.is_admin()})")

    #Productos
    separador("ALTA DE PRODUCTOS")
    portatil = tienda.agregar_producto(ProductoElectronico("Portátil", 899.99, 10, 24))
    auriculares = tienda.agregar_producto(ProductoElectronico("Auriculares", 59.90, 25, 12))
    movil = tienda.agregar_producto(ProductoElectronico("Smartphone", 499.00, 8, 36))
    camiseta = tienda.agregar_producto(ProductoRopa("Camiseta", 19.95, 50, "M", "Azul"))
    pantalon = tienda.agregar_producto(ProductoRopa("Vaquero", 45.50, 30, "42", "Negro"))
    mostrar_inventario(tienda)

    # Pedidos
    separador("PEDIDOS")
    pedido1 = tienda.realizar_pedido(ana.id, {portatil.id: 1, auriculares.id: 2})
    print(pedido1, "\n")
    pedido2 = tienda.realizar_pedido(luis.id, {camiseta.id: 3, pantalon.id: 2})
    print(pedido2, "\n")
    pedido3 = tienda.realizar_pedido(marta.id, {movil.id: 1, camiseta.id: 1,
                                                auriculares.id: 1})
    print(pedido3, "\n")
    pedido4 = tienda.realizar_pedido(ana.id, {pantalon.id: 1})
    print(pedido4)

    #Casos de error
    separador("VALIDACIONES")
    intentos = [
        ("Stock insuficiente", lambda: tienda.realizar_pedido(luis.id, {movil.id: 100})),
        ("Usuario inexistente", lambda: tienda.realizar_pedido("id-falso", {movil.id: 1})),
        ("Pedido de un administrador", lambda: tienda.realizar_pedido(admin.id, {movil.id: 1})),
    ]
    for descripcion, accion in intentos:
        try:
            accion()
        except ValueError as error:
            print(f"  {descripcion}: {error}")

    #Histórico
    separador(f"HISTÓRICO DE PEDIDOS DE {ana.nombre.upper()}")
    for pedido in tienda.listar_pedidos_usuario(ana.id):
        print(pedido, "\n")

    #Stock actualizado
    separador("STOCK ACTUALIZADO")
    mostrar_inventario(tienda)

    #Eliminación de producto
    separador("ELIMINAR PRODUCTO")
    print(f"  Eliminando '{pantalon.nombre}': {tienda.eliminar_producto(pantalon.id)}")
    mostrar_inventario(tienda)


if __name__ == "__main__":
    main()
