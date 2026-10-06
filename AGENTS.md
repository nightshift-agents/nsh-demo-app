# Convenciones del repo

- Python 3.13, FastAPI, Pydantic v2. Dependencias con `uv` (`pyproject.toml`, `uv.lock`).
- Código y nombres en inglés; mensajes de error de la API, documentación y commits en español.
- Estilo: `ruff` (lint + formato, línea de 100). Antes de entregar: `make lint && make test`.
- Tests con `pytest` en `tests/`, usando `TestClient` y las fixtures de `tests/conftest.py`
  (`client`, `book`, `member`). El store se limpia solo entre tests.
- Cada endpoint nuevo lleva su test. Los pendientes del `README.md` tienen un test `xfail`
  con `strict=True`: al resolverlos, quitar el marcador.
- Almacenamiento en memoria (`app/storage.py`); no añadir base de datos ni dependencias
  nuevas sin que lo pida la tarea.
- Las ramas de agente se llaman `agent/<descripcion-corta>` y salen de `main`. Un PR por
  tarea, con descripción corta: qué se hizo y por qué.
- Nunca hacer `git push --force` sobre `main`.
