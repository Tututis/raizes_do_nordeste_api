from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EstoqueCreate(BaseModel):
    unidade_id: int
    produto_id: int
    quantidade: int = Field(ge=0)


class EstoqueMovimentacao(BaseModel):
    quantidade: int = Field(gt=0)


class EstoqueResponse(BaseModel):
    id: int
    unidade_id: int
    produto_id: int
    quantidade: int
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)