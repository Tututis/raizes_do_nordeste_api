from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def gerar_hash_senha(senha: str) -> str:
    if len(senha.encode("utf-8")) > 72:
        raise ValueError("A senha não pode ter mais de 72 bytes.")

    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    if len(senha.encode("utf-8")) > 72:
        return False

    return pwd_context.verify(senha, senha_hash)