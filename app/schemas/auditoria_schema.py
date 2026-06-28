from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AuditoriaResponse(BaseModel):
    id: int
    usuario_id: int | None
    acao: str
    entidade: str
    entidade_id: int
    detalhes: str | None
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)