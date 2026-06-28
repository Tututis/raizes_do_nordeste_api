from pydantic import BaseModel, ConfigDict


class UnidadeCreate(BaseModel):
    nome: str
    cidade: str
    estado: str
    ativa: bool = True


class UnidadeResponse(BaseModel):
    id: int
    nome: str
    cidade: str
    estado: str
    ativa: bool

    model_config = ConfigDict(from_attributes=True)