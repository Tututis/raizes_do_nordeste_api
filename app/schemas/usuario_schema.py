from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.usuario import PerfilUsuario


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=3)
    email: str
    senha: str = Field(min_length=6, max_length=72)
    perfil: PerfilUsuario = PerfilUsuario.CLIENTE
    consentimento_lgpd: bool = False


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    perfil: PerfilUsuario
    consentimento_lgpd: bool
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)