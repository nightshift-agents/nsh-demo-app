# PROGRESS

## Hecho
- Implementada validación en POST /loans para verificar que el libro no esté ya prestado
- Agregada comprobación de préstamos activos por book_id antes de crear un nuevo préstamo
- Removido el marcador xfail del test test_cannot_loan_book_already_on_loan
- Corregido formato de app/routers/loans.py con ruff format
- Validación completa exitosa: make lint && make test en verde (20 passed, 4 xfailed)

## Pendiente
- Ninguno

## Siguiente paso
Issue #2 completamente resuelto y validado. El endpoint POST /loans valida correctamente que un libro no tenga un préstamo activo, respondiendo 409 Conflict cuando corresponde. Código formateado y CI en verde.
