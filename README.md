# nsh-demo-app

API de biblioteca de préstamos: libros, socios y préstamos, con almacenamiento en memoria.
Es la aplicación piloto sobre la que trabaja un agente de código desatendido, así que es
deliberadamente pequeña y sus tests corren en segundos.

## Stack

- Python 3.13, FastAPI, Pydantic v2
- `uv` para dependencias y entorno virtual
- `pytest` para tests, `ruff` para lint y formato

## Cómo correrlo

```sh
make install   # uv sync: crea .venv e instala dependencias (incluye grupo dev)
make run       # uvicorn en http://localhost:8000 (docs en /docs)
make test      # pytest
make lint      # ruff check + ruff format --check
make format    # ruff --fix + ruff format
```

Si `uv` no está instalado: <https://docs.astral.sh/uv/getting-started/installation/>.

## Endpoints

| Método | Ruta                        | Descripción                                      |
|--------|-----------------------------|--------------------------------------------------|
| GET    | `/health`                   | Estado del servicio                              |
| POST   | `/books`                    | Crea un libro (ISBN único)                       |
| GET    | `/books?author=`            | Lista libros, filtro opcional por autor          |
| GET    | `/books/{id}`               | Detalle de un libro                              |
| DELETE | `/books/{id}`               | Elimina un libro                                 |
| POST   | `/members`                  | Crea un socio (correo único, normalizado)        |
| GET    | `/members`                  | Lista socios                                     |
| GET    | `/members/{id}`             | Detalle de un socio                              |
| POST   | `/loans`                    | Crea un préstamo (vence en 14 días por defecto)  |
| GET    | `/loans?member_id=&active=` | Lista préstamos con filtros opcionales           |
| GET    | `/loans/{id}`               | Detalle de un préstamo                           |
| POST   | `/loans/{id}/return`        | Registra la devolución                           |

Reglas vigentes: un socio no puede tener más de 3 préstamos activos; un préstamo devuelto no se
puede devolver dos veces.

Ejemplo rápido:

```sh
curl -s -X POST localhost:8000/books -H 'content-type: application/json' \
  -d '{"title":"Rayuela","author":"Cortázar","isbn":"9788437604572"}'
curl -s -X POST localhost:8000/members -H 'content-type: application/json' \
  -d '{"name":"Ana","email":"ana@example.com"}'
curl -s -X POST localhost:8000/loans -H 'content-type: application/json' \
  -d '{"book_id":1,"member_id":1}'
```

## Pendientes conocidos

Cada pendiente tiene un test marcado `xfail(strict=True)` que lo demuestra. Al resolverlo hay
que quitar el marcador para que el test pase en verde.

1. **Bug: `POST /loans` permite prestar un libro que ya está prestado.** No se valida que el
   libro no tenga un préstamo activo. Debe responder `409 Conflict`.
   Test: `tests/test_loans.py::test_cannot_loan_book_already_on_loan`.
2. **Feature: falta `GET /loans/overdue`.** Debe devolver los préstamos activos cuyo `due_date`
   es anterior a hoy. Test: `tests/test_loans.py::test_list_overdue_loans`.
3. **Validación: `member.email` acepta cualquier texto.** Debe rechazar con `422` los correos
   con formato inválido. Test: `tests/test_members.py::test_create_member_rejects_invalid_email`.
