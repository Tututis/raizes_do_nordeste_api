from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.auditoria import Auditoria
from app.models.usuario import PerfilUsuario, Usuario
from app.schemas.auditoria_schema import AuditoriaResponse
from app.security import exigir_perfis


router = APIRouter(
    prefix="/auditoria",
    tags=["Auditoria"]
)


@router.get("", response_model=list[AuditoriaResponse])
def listar_auditoria(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(
        exigir_perfis(
            PerfilUsuario.ADMIN,
            PerfilUsuario.GERENTE
        )
    )
):
    return db.query(Auditoria).order_by(Auditoria.criado_em.desc()).all()