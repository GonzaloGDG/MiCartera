# Autenticación

## Propósito

Gestiona el acceso de usuarios al sistema. La API expone un endpoint de login y valida credenciales contra los datos almacenados.

## Ficheros clave

- [backend/app/routes/auth.py](../../../backend/app/routes/auth.py)
- [backend/app/repositories/auth_repository.py](../../../backend/app/repositories/auth_repository.py)
- [backend/app/schemas/auth.py](../../../backend/app/schemas/auth.py)
- [backend/app/data/usuarios.json](../../../backend/app/data/usuarios.json)
- [frontend/js/login.js](../../../frontend/js/login.js)
- [frontend/login.html](../../../frontend/login.html)

## Flujo principal

1. El frontend envía username y password.
2. La ruta `/api/login` recibe el payload.
3. El repository valida la combinación contra `usuarios.json`.
4. Si la credencial coincide, devuelve `ok: true` con nombre y rol.
5. En caso contrario, devuelve un error de credenciales.

## Regla de negocio

La lógica de validación se mantiene en el repository y no se debe duplicar en el frontend.

## Dependencias

- [architecture.md](architecture.md)
- [data.md](data.md)
- [frontend.md](frontend.md)

## Cuándo leer este nodo

Cuando se toque:

- login
- manejo de roles
- validación de usuarios
- renovación o ampliación de la autenticación

## Riesgos

- la validación actual es muy básica y depende de un JSON local
- no hay control de sesión persistente ni JWT en la implementación actual

## Pruebas de regresión

- [test_auth.py](../../../backend/app/tests/test_auth.py): comprueba el login válido (incluidos espacios exteriores) y el rechazo de credenciales incorrectas mediante la API.
- [conftest.py](../../../backend/app/tests/conftest.py): proporciona usuarios aislados para cada prueba, sin leer ni modificar los datos reales.

Ejecutar con `cd backend && python -m pytest -q app/tests/test_auth.py`.
