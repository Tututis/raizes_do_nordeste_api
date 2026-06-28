from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.unidade import Unidade
from app.schemas.unidade_schema import UnidadeCreate, UnidadeResponse
from app.models.usuario import PerfilUsuario, Usuario
from app.security import exigir_perfis

router = APIRouter(
    prefix="/unidades",
    tags=["Unidades"]
)


@router.post(
    "",
    response_model=UnidadeResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_unidade(
    dados: UnidadeCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfis(PerfilUsuario.ADMIN, PerfilUsuario.GERENTE))
):
    nova_unidade = Unidade(
        nome=dados.nome,
        cidade=dados.cidade,
        estado=dados.estado.upper(),
        ativa=dados.ativa
    )

    db.add(nova_unidade)
    db.commit()
    db.refresh(nova_unidade)

    return nova_unidade


@router.get("", response_model=list[UnidadeResponse])
def listar_unidades(db: Session = Depends(get_db)):
    return db.query(Unidade).all()


@router.get("/{unidade_id}", response_model=UnidadeResponse)
def buscar_unidade(unidade_id: int, db: Session = Depends(get_db)):
    unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()

    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada"
        )

    return unidade