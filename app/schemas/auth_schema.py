from pydantic import BaseModel, Field

from app.models.usuario import PerfilUsuario


class LoginRequest(BaseModel):
    email: str
    senha: str = Field(min_length=6, max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario_id: int
    nome: str
    perfil: PerfilUsuario