from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.estoque import Estoque
from app.models.pedido import CanalPedido, ItemPedido, Pedido, StatusPedido
from app.models.produto import Produto
from app.models.unidade import Unidade
from app.models.usuario import PerfilUsuario, Usuario
from app.security import obter_usuario_atual, exigir_perfis
from app.schemas.pedido_schema import PedidoCreate, PedidoResponse


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.post(
    "",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_pedido(
    dados: PedidoCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):

    if (
        usuario_atual.perfil == PerfilUsuario.CLIENTE
        and usuario_atual.id != dados.cliente_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cliente só pode criar pedido para si mesmo"
        )

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    unidade = db.query(Unidade).filter(Unidade.id == dados.unidade_id).first()

    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada"
        )

    if not dados.itens:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="O pedido deve possuir pelo menos um item"
        )

    valor_total = Decimal("0.00")
    itens_processados = []

    for item in dados.itens:
        produto = db.query(Produto).filter(Produto.id == item.produto_id).first()

        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto {item.produto_id} não encontrado"
            )

        if not produto.ativo:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Produto {produto.nome} está inativo"
            )

        estoque = db.query(Estoque).filter(
            Estoque.unidade_id == dados.unidade_id,
            Estoque.produto_id == item.produto_id
        ).first()

        if not estoque:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto {produto.nome} não possui estoque cadastrado nesta unidade"
            )

        if estoque.quantidade < item.quantidade:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Estoque insuficiente para o produto {produto.nome}"
            )

        preco_unitario = Decimal(str(produto.preco))
        subtotal = preco_unitario * item.quantidade
        valor_total += subtotal

        itens_processados.append({
            "produto": produto,
            "estoque": estoque,
            "quantidade": item.quantidade,
            "preco_unitario": preco_unitario,
            "subtotal": subtotal
        })

    novo_pedido = Pedido(
        cliente_id=dados.cliente_id,
        unidade_id=dados.unidade_id,
        canal_pedido=dados.canalPedido,
        status=StatusPedido.AGUARDANDO_PAGAMENTO,
        valor_total=valor_total
    )

    db.add(novo_pedido)
    db.flush()

    for item in itens_processados:
        item["estoque"].quantidade -= item["quantidade"]

        novo_item = ItemPedido(
            pedido_id=novo_pedido.id,
            produto_id=item["produto"].id,
            quantidade=item["quantidade"],
            preco_unitario=item["preco_unitario"],
            subtotal=item["subtotal"]
        )

        db.add(novo_item)

    db.commit()
    db.refresh(novo_pedido)

    return novo_pedido


@router.get("", response_model=list[PedidoResponse])
def listar_pedidos(
    canalPedido: CanalPedido | None = Query(default=None),
    status_pedido: StatusPedido | None = Query(default=None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(
        exigir_perfis(
            PerfilUsuario.ADMIN,
            PerfilUsuario.GERENTE,
            PerfilUsuario.ATENDENTE,
            PerfilUsuario.COZINHA
        )
    )
):
    consulta = db.query(Pedido)

    if canalPedido:
        consulta = consulta.filter(Pedido.canal_pedido == canalPedido)

    if status_pedido:
        consulta = consulta.filter(Pedido.status == status_pedido)

    return consulta.all()


@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado"
        )

    if (
        usuario_atual.perfil == PerfilUsuario.CLIENTE
        and pedido.cliente_id != usuario_atual.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cliente só pode consultar seus próprios pedidos"
        )

    return pedido

    return pedido