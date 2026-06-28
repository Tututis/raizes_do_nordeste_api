from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.security import gerar_hash_senha


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.post(
    "",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário cadastrado com este e-mail"
        )

    novo_usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
        perfil=dados.perfil,
        consentimento_lgpd=dados.consentimento_lgpd
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@router.get("", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    return usuario