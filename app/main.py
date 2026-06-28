from fastapi import FastAPI

from app.database import Base, engine
import app.models

from app.routers.unidades_router import router as unidades_router
from app.routers.produtos_router import router as produtos_router
from app.routers.estoque_router import router as estoque_router
from app.routers.pedidos_router import router as pedidos_router
from app.routers.usuarios_router import router as usuarios_router
from app.routers.pagamentos_router import router as pagamentos_router
from app.routers.auth_router import router as auth_router
from app.routers.auditoria_router import router as auditoria_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API Raízes do Nordeste",
    description="API para gestão de pedidos, estoque, unidades e pagamentos mock.",
    version="1.0.0"
)


app.include_router(unidades_router)
app.include_router(produtos_router)
app.include_router(estoque_router)
app.include_router(pedidos_router)
app.include_router(usuarios_router)
app.include_router(pagamentos_router)
app.include_router(auth_router)
app.include_router(auditoria_router)

@app.get("/")
def health_check():
    return {
        "status": "online",
        "mensagem": "API Raízes do Nordeste em execução"
    }