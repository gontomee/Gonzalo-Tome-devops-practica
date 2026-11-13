# gonzalo-devops-practica

**Proyecto:** Tienda online – API REST con FastAPI
**Autor:** Gonzalo Tomé Gómez

## Descripción

API REST en Python (FastAPI) para gestionar una tienda online: usuarios (clientes y administradores), productos (genéricos, electrónicos y ropa) y pedidos con validación de stock. Los datos se guardan en memoria (se pierden al reiniciar). Es el desarrollo de la Práctica 2, contenerizado con Docker en las Prácticas 3.1 y 3.2.

## Estructura

```
.
├── src/                 # Código de la Práctica 2 (main.py, models/, schemas/, Services/)
├── Dockerfile
├── .dockerignore
├── requirements.txt     # Dependencias con versiones fijadas
└── README.md
```

## Ejecución local (sin Docker)

```bash
pip install -r requirements.txt
cd src
python -m uvicorn main:app --reload
```

Swagger: http://127.0.0.1:8000/docs

## Docker

### Construir la imagen

```bash
docker build -t practica-devops:v1 .
```

### Ejecutar el contenedor

```bash
docker run --rm -p 8000:8000 practica-devops:v1
```

En segundo plano y con otro puerto del anfitrión:

```bash
docker run -d --name tienda -p 9000:8000 practica-devops:v1
docker logs tienda
docker stop tienda
docker rm tienda
```

Cambiando el puerto interno con la variable de entorno:

```bash
docker run --rm -p 8080:8000 practica-devops:v1
```

### Variables de entorno

| Variable | Por defecto | Descripción |
|---|---|---|
| `PORT` | `8000` | Puerto en el que escucha uvicorn dentro del contenedor |

No se usan secretos ni claves.

### Pruebas / salida esperada

Al arrancar, los logs muestran:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Pruebas (con el contenedor en marcha):

```bash
curl -X POST http://localhost:8000/usuarios -H "Content-Type: application/json" \
  -d '{"nombre":"Ana García","email":"ana@mail.com","tipo":"cliente","direccion":"C/ Mayor 1, Madrid"}'
# -> 201 con el usuario creado

curl http://localhost:8000/productos
# -> 200 []
```

También se puede abrir http://localhost:8000/docs y probar los endpoints desde Swagger.

### Publicar / descargar la imagen (registry)

```bash
docker tag practica-devops:v1 <usuario_dockerhub>/practica-devops:v1
docker login
docker push <usuario_dockerhub>/practica-devops:v1

# Descargar:
docker pull <usuario_dockerhub>/practica-devops:v1
```

## Endpoints

| Método | Ruta | Descripción | Códigos |
|---|---|---|---|
| POST | /usuarios | Crea un usuario (`cliente` o `administrador`) | 201, 409, 422 |
| GET | /usuarios | Lista los usuarios | 200 |
| GET | /usuarios/{usuario_id} | Devuelve un usuario | 200, 404 |
| POST | /productos | Crea un producto (`generico`, `electronico`, `ropa`) | 201, 422 |
| GET | /productos | Lista los productos | 200 |
| GET | /productos/{producto_id} | Devuelve un producto | 200, 404 |
| DELETE | /productos/{producto_id} | Elimina un producto | 204, 404 |
| POST | /pedidos | Crea un pedido (valida cliente, productos y stock) | 201, 400, 404, 422 |
| GET | /usuarios/{cliente_id}/pedidos | Historial de pedidos del cliente | 200, 404 |

## Flujo de ramas

`main` (estable) ← Pull Request ← `feature/docker`.
