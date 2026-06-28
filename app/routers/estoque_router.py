from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.estoque import Estoque
from app.models.produto import Produto
from app.models.unidade import Unidade
from app.schemas.estoque_schema import EstoqueCreate, EstoqueMovimentacao, EstoqueResponse
from app.models.usuario import PerfilUsuario, Usuario
from app.security import exigir_perfis

router = APIRouter(
    prefix="/estoque",
    tags=["Estoque"]
)


@router.post("", response_model=EstoqueResponse, status_code=status.HTTP_201_CREATED)
def criar_estoque(
    dados: EstoqueCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfis(PerfilUsuario.ADMIN, PerfilUsuario.GERENTE))
):

    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada"
        )

    produto = db.query(Produto).filter(Produto.id == dados.produto_id).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    estoque_existente = db.query(Estoque).filter(
        Estoque.unidade_id == dados.unidade_id,
        Estoque.produto_id == dados.produto_id
    ).first()

    if estoque_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Estoque já cadastrado para esta unidade e produto"
        )

    novo_estoque = Estoque(
        unidade_id=dados.unidade_id,
        produto_id=dados.produto_id,
        quantidade=dados.quantidade,
        atualizado_em=datetime.utcnow()
    )

    db.add(novo_estoque)
    db.commit()
    db.refresh(novo_estoque)

    return novo_estoque


@router.get("/unidade/{unidade_id}", response_model=list[EstoqueResponse])
def listar_estoque_por_unidade(unidade_id: int, db: Session = Depends(get_db)):
    unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()

    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada"
        )

    return db.query(Estoque).filter(Estoque.unidade_id == unidade_id).all()


@router.patch("/{estoque_id}/entrada", response_model=EstoqueResponse)
def registrar_entrada(
    estoque_id: int,
    dados: EstoqueMovimentacao,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfis(PerfilUsuario.ADMIN, PerfilUsuario.GERENTE))
):
    estoque = db.query(Estoque).filter(Estoque.id == estoque_id).first()

    if not estoque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estoque não encontrado"
        )

    estoque.quantidade += dados.quantidade
    estoque.atualizado_em = datetime.utcnow()

    db.commit()
    db.refresh(estoque)

    return estoque


@router.patch("/{estoque_id}/saida", response_model=EstoqueResponse)
def registrar_saida(
    estoque_id: int,
    dados: EstoqueMovimentacao,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfis(PerfilUsuario.ADMIN, PerfilUsuario.GERENTE))
):
    estoque = db.query(Estoque).filter(Estoque.id == estoque_id).first()

    if not estoque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estoque não encontrado"
        )

    if estoque.quantidade < dados.quantidade:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Estoque insuficiente para realizar a saída"
        )

    estoque.quantidade -= dados.quantidade
    estoque.atualizado_em = datetime.utcnow()

    db.commit()
    db.refresh(estoque)

    return estoque