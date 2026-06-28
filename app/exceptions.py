from datetime import datetime, timezone

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def montar_resposta_erro(
    status_code: int,
    codigo: str,
    mensagem: str,
    path: str,
    detalhes=None
):
    resposta = {
        "erro": True,
        "codigo": codigo,
        "mensagem": mensagem,
        "status": status_code,
        "path": path,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    if detalhes is not None:
        resposta["detalhes"] = detalhes

    return resposta


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail

    if isinstance(detail, str):
        mensagem = detail
        detalhes = None
    else:
        mensagem = "Erro na requisição"
        detalhes = detail

    return JSONResponse(
        status_code=exc.status_code,
        content=montar_resposta_erro(
            status_code=exc.status_code,
            codigo="HTTP_ERROR",
            mensagem=mensagem,
            path=str(request.url.path),
            detalhes=detalhes
        )
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    detalhes = []

    for erro in exc.errors():
        detalhes.append({
            "campo": ".".join(str(local) for local in erro.get("loc", [])),
            "mensagem": erro.get("msg"),
            "tipo": erro.get("type")
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=montar_resposta_erro(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            codigo="VALIDATION_ERROR",
            mensagem="Erro de validação dos dados enviados",
            path=str(request.url.path),
            detalhes=detalhes
        )
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=montar_resposta_erro(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            codigo="INTERNAL_SERVER_ERROR",
            mensagem="Erro interno no servidor",
            path=str(request.url.path)
        )
    )


def registrar_exception_handlers(app):
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)