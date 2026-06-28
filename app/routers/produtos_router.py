from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.produto import Produto
from app.schemas.produto_schema import ProdutoCreate, ProdutoResponse
from app.models.usuario import PerfilUsuario, Usuario
from app.security import exigir_perfis

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


@router.post(
    "",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_produto(
    dados: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfis(PerfilUsuario.ADMIN, PerfilUsuario.GERENTE))
):
    novo_produto = Produto(
        nome=dados.nome,
        descricao=dados.descricao,
        preco=dados.preco,
        ativo=dados.ativo,
        sazonal=dados.sazonal
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@router.get("", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    return produto