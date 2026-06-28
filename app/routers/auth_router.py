from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.schemas.usuario_schema import UsuarioResponse
from app.security import criar_token_acesso, obter_usuario_atual, verificar_senha


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post("/login", response_model=TokenResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos"
        )

    senha_valida = verificar_senha(dados.senha, usuario.senha_hash)

    if not senha_valida:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos"
        )

    token = criar_token_acesso({
        "sub": usuario.email,
        "usuario_id": usuario.id,
        "perfil": usuario.perfil.value
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario_id": usuario.id,
        "nome": usuario.nome,
        "perfil": usuario.perfil
    }


@router.get("/me", response_model=UsuarioResponse)
def dados_usuario_logado(
    usuario: Usuario = Depends(obter_usuario_atual)
):
    return usuario