from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.pagamento import Pagamento, StatusPagamento
from app.models.pedido import Pedido, StatusPedido
from app.schemas.pagamento_schema import PagamentoMockCreate, PagamentoResponse
from app.models.usuario import PerfilUsuario, Usuario
from app.security import exigir_perfis

router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)


@router.post(
    "/mock",
    response_model=PagamentoResponse,
    status_code=status.HTTP_201_CREATED
)
def processar_pagamento_mock(
    dados: PagamentoMockCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(
        exigir_perfis(
            PerfilUsuario.ADMIN,
            PerfilUsuario.GERENTE,
            PerfilUsuario.ATENDENTE,
            PerfilUsuario.CLIENTE
        )
    )
):
    pedido = db.query(Pedido).filter(Pedido.id == dados.pedido_id).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado"
        )

    if pedido.status not in [
        StatusPedido.AGUARDANDO_PAGAMENTO,
        StatusPedido.PAGAMENTO_RECUSADO
    ]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pedido não está em status válido para pagamento"
        )

    pagamento_existente = db.query(Pagamento).filter(
        Pagamento.pedido_id == dados.pedido_id
    ).first()

    if pagamento_existente and pagamento_existente.status == StatusPagamento.APROVADO:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Pedido já possui pagamento aprovado"
        )

    if dados.aprovado:
        status_pagamento = StatusPagamento.APROVADO
        novo_status_pedido = StatusPedido.PAGO
        mensagem = "Pagamento mock aprovado"
    else:
        status_pagamento = StatusPagamento.RECUSADO
        novo_status_pedido = StatusPedido.PAGAMENTO_RECUSADO
        mensagem = "Pagamento mock recusado"

    novo_pagamento = Pagamento(
        pedido_id=pedido.id,
        status=status_pagamento,
        valor=pedido.valor_total,
        transacao_mock_id=str(uuid4()),
        mensagem=mensagem
    )

    pedido.status = novo_status_pedido

    db.add(novo_pagamento)
    db.commit()
    db.refresh(novo_pagamento)

    return novo_pagamento


@router.get("/{pagamento_id}", response_model=PagamentoResponse)
def buscar_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    pagamento = db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()

    if not pagamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pagamento não encontrado"
        )

    return pagamento