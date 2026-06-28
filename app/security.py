import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import PerfilUsuario, Usuario


SECRET_KEY = os.getenv("SECRET_KEY", "chave-dev-altere-em-producao")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()


def gerar_hash_senha(senha: str) -> str:
    if len(senha.encode("utf-8")) > 72:
        raise ValueError("A senha não pode ter mais de 72 bytes.")

    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    if len(senha.encode("utf-8")) > 72:
        return False

    return pwd_context.verify(senha, senha_hash)


def criar_token_acesso(dados: dict) -> str:
    dados_token = dados.copy()

    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados_token.update({"exp": expiracao})

    token = jwt.encode(
        dados_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    token = credenciais.credentials

    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email: str | None = payload.get("sub")

        if email is None:
            raise credenciais_invalidas

    except JWTError:
        raise credenciais_invalidas

    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        raise credenciais_invalidas

    return usuario


def exigir_perfis(*perfis_permitidos: PerfilUsuario):
    def verificar_perfil(usuario: Usuario = Depends(obter_usuario_atual)) -> Usuario:
        if usuario.perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário não possui permissão para esta operação"
            )

        return usuario

    return verificar_perfil