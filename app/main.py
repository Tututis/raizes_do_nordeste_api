from fastapi import FastAPI

from app.database import Base, engine
import app.models

from app.routers.unidades_router import routers as unidades_router
from app.routers.produtos_router import routers as produtos_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API Raízes do Nordeste",
    description="API para gestão de pedidos, estoque, unidades e pagamentos mock.",
    version="1.0.0"
)


app.include_router(unidades_router)
app.include_router(produtos_router)


@app.get("/")
def health_check():
    return {
        "status": "online",
        "mensagem": "API Raízes do Nordeste em execução"
    }