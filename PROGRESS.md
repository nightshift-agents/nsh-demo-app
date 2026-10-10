# PROGRESS

## Hecho
- Agregada dependencia `email-validator>=2.0` en pyproject.toml
- Modificado modelo `MemberCreate` para usar `EmailStr` (con validación automática de formato)
- Eliminado marcador `xfail` del test `test_create_member_rejects_invalid_email`
- Validación completa: make lint && make test pasan (22 passed, 2 xfail de otros issues)

## Pendiente
Ninguna tarea pendiente para este issue.

## Siguiente paso
Issue resuelto. El endpoint POST /members ahora rechaza emails con formato inválido con código 422.
