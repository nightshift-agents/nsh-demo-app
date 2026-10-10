# PROGRESS

## Hecho
- Implementada validación en POST /loans para verificar que el libro no esté ya prestado
- Agregada comprobación de préstamos activos por book_id antes de crear un nuevo préstamo
- Removido el marcador xfail del test test_cannot_loan_book_already_on_loan
- Ejecutada suite completa de tests: 20 passed, 4 xfailed (otros bugs pendientes)

## Pendiente
- Ninguno para este issue

## Siguiente paso
Issue #2 resuelto. El endpoint POST /loans ahora valida correctamente que un libro no tenga un préstamo activo antes de permitir un nuevo préstamo, respondiendo 409 Conflict cuando corresponde.
