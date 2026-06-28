from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.pagamento import StatusPagamento


class PagamentoMockCreate(BaseModel):
    pedido_id: int
    aprovado: bool = True


class PagamentoResponse(BaseModel):
    id: int
    pedido_id: int
    status: StatusPagamento
    valor: Decimal
    transacao_mock_id: str | None
    mensagem: str | None
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)