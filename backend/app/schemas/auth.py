from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    ok: bool
    username: str | None = None
    nombre: str | None = None
    rol: str | None = None
    mensaje: str | None = None