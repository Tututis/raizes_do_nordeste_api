from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProdutoCreate(BaseModel):
    nome: str
    descricao: str | None = None
    preco: Decimal = Field(gt=0)
    ativo: bool = True
    sazonal: bool = False


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None
    preco: Decimal
    ativo: bool
    sazonal: bool

    model_config = ConfigDict(from_attributes=True)