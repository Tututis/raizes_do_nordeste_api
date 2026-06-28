from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.pedido import CanalPedido, StatusPedido


class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)


class PedidoCreate(BaseModel):
    cliente_id: int
    unidade_id: int
    canalPedido: CanalPedido
    itens: list[ItemPedidoCreate]


class ItemPedidoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)


class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    unidade_id: int
    canal_pedido: CanalPedido
    status: StatusPedido
    valor_total: Decimal
    criado_em: datetime
    itens: list[ItemPedidoResponse]

    model_config = ConfigDict(from_attributes=True)